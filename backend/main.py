import re
import time
from html import unescape
from pathlib import Path
from urllib.parse import quote_plus

import feedparser
import httpx
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from config import GEMINI_API_KEY

import db

# 정적 파일 디렉토리: Vercel 배포 환경 대응
# Vercel에서는 __file__ 경로가 다를 수 있으므로 절대 경로 사용
STATIC_DIR = Path(__file__).resolve().parent / "static"
# Vercel 환경에서도 작동하도록 경로 확인
if not STATIC_DIR.exists():
    # 대체 경로 시도
    alt_path = Path(__file__).resolve().parent.parent.parent / "backend" / "static"
    if alt_path.exists():
        STATIC_DIR = alt_path

app = FastAPI(title="구글 뉴스 챗봇 API")

# CORS 설정: 환경 변수로 허용된 오리진 관리 (Vercel 배포 대응)
import os
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*")
if ALLOWED_ORIGINS == "*":
    origins = ["*"]
else:
    origins = [origin.strip() for origin in ALLOWED_ORIGINS.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GOOGLE_NEWS_RSS_BASE = "https://news.google.com/rss/search"
DISPLAY = 10
LANG = "ko"
REGION = "KR"
CEID = "KR:ko"

# 마지막 검색 결과 저장 (뉴스 기반 대화용)
_last_search: dict = {"keyword": "", "sort": "", "items": [], "summary": ""}


def strip_html(s: str) -> str:
    if not s:
        return ""
    s = unescape(s)
    return re.sub(r"<[^>]+>", "", s).strip()


def _pub_date(entry) -> str:
    raw = getattr(entry, "published", None) or getattr(entry, "updated", None)
    return raw or ""


def _pub_ts(entry) -> float:
    p = getattr(entry, "published_parsed", None) or getattr(entry, "updated_parsed", None)
    if p:
        return time.mktime(p)
    return 0.0


def _desc(entry) -> str:
    raw = getattr(entry, "summary", None) or getattr(entry, "description", None)
    return strip_html(raw or "")


@app.get("/")
async def root():
    """웹 UI"""
    return FileResponse(STATIC_DIR / "index.html")


app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/api/news")
async def search_news(
    keyword: str = Query(..., min_length=1),
    sort: str = Query("date", regex="^(date|sim)$"),
):
    """구글 뉴스 검색. sort: date=최신순, sim=인기순(관련도순)."""
    url = f"{GOOGLE_NEWS_RSS_BASE}?q={quote_plus(keyword)}&hl={LANG}&gl={REGION}&ceid={CEID}"
    headers = {"User-Agent": "Mozilla/5.0 (compatible; NewsBot/1.0)"}
    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=headers, timeout=15.0)
    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=r.text)

    feed = feedparser.parse(r.text)
    entries = getattr(feed, "entries", []) or []

    if sort == "date":
        entries = sorted(entries, key=_pub_ts, reverse=True)
    entries = entries[:DISPLAY]

    results = []
    for e in entries:
        results.append(
            {
                "title": strip_html(getattr(e, "title", "") or ""),
                "link": getattr(e, "link", "") or "",
                "originallink": getattr(e, "link", "") or "",
                "description": _desc(e),
                "pubDate": _pub_date(e),
            }
        )

    summary = ""
    if GEMINI_API_KEY and results:
        summary = await _summarize_with_gemini(keyword, results)
    if results and not (summary or "").strip():
        summary = f"'{keyword}' 관련 뉴스 {len(results)}건이 검색되었습니다. 아래 제목과 요약을 참고하세요."

    global _last_search
    _last_search = {"keyword": keyword, "sort": sort, "items": results, "summary": summary}

    db_log = db.log_search(keyword, sort, len(results))

    return {
        "keyword": keyword,
        "sort": "최신순" if sort == "date" else "인기순",
        "total": len(results),
        "items": results,
        "summary": summary,
        "db_log": db_log,
    }


async def _summarize_with_gemini(keyword: str, items: list) -> str:
    try:
        from google import genai

        client = genai.Client(api_key=GEMINI_API_KEY)
        context = "\n\n".join(
            f"[{i+1}] 제목: {it['title']}\n요약: {it['description']}\n날짜: {it['pubDate']}"
            for i, it in enumerate(items)
        )
        prompt = f"""다음은 '{keyword}'에 대한 구글 뉴스 검색 결과 10건입니다. 이 내용만 바탕으로 3~5문장으로 간단히 요약해주세요. 한국어로 작성해주세요.

【뉴스 검색 결과】
{context}"""
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )
        text = getattr(response, "text", None) or ""
        return (text or "").strip()
    except Exception:
        return ""


class ChatRequest(BaseModel):
    message: str


@app.post("/api/chat")
async def chat(req: ChatRequest):
    """검색된 구글 뉴스 내용을 기준으로 대화. Gemini API 사용."""
    global _last_search
    items = _last_search.get("items", [])
    keyword = _last_search.get("keyword", "")
    summary = _last_search.get("summary", "")

    if not items:
        return {
            "reply": "먼저 위에서 키워드로 뉴스를 검색해주세요. 검색 결과를 바탕으로 질문에 답할 수 있습니다.",
        }

    user_msg = (req.message or "").strip()
    if not user_msg:
        return {"reply": "질문을 입력해주세요."}

    reply = ""
    if GEMINI_API_KEY:
        try:
            out = await _chat_gemini(keyword, summary, items, user_msg)
            reply = out["reply"]
        except Exception:
            fb = _chat_fallback(keyword, items, user_msg)
            reply = "Gemini API 한도 초과 또는 일시 오류로, 검색 결과 기반 간단 답변을 드립니다.\n\n" + fb["reply"]
    else:
        out = _chat_fallback(keyword, items, user_msg)
        reply = out["reply"]

    db_log_user = db.log_chat(keyword, "user", user_msg)
    db_log_assistant = db.log_chat(keyword, "assistant", reply)
    return {
        "reply": reply,
        "db_log": [db_log_user, db_log_assistant],
    }


async def _chat_gemini(keyword: str, summary: str, items: list, user_msg: str):
    from google import genai

    client = genai.Client(api_key=GEMINI_API_KEY)
    context = "\n\n".join(
        f"[{i+1}] 제목: {it['title']}\n요약: {it['description']}\n날짜: {it['pubDate']}"
        for i, it in enumerate(items)
    )
    prompt = f"""당신은 '{keyword}' 관련 구글 뉴스 검색 결과를 바탕으로 답변하는 어시스턴트입니다.
아래 뉴스 요약만을 근거로 답변하세요. 제공된 뉴스에 없는 내용은 "제공된 뉴스에 해당 내용이 없습니다."라고 답하세요.
답변은 한국어로, 간결하게.

【검색 결과 요약】
{summary}

【뉴스 상세】
{context}

【사용자 질문】
{user_msg}"""

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )
    reply = getattr(response, "text", None) or "답변을 생성하지 못했습니다."
    return {"reply": (reply or "").strip()}


def _chat_fallback(keyword: str, items: list, user_msg: str):
    msg_lower = user_msg.lower()
    found = []
    for i, it in enumerate(items):
        text = (it["title"] + " " + it["description"]).lower()
        if any(w in text for w in msg_lower.split() if len(w) > 1):
            found.append((i + 1, it))
    if not found:
        return {
            "reply": "제공된 뉴스 내용 중에는 해당 주제와 직접 맞는 기사가 없습니다. 다른 키워드로 검색하거나, 질문을 바꿔 보세요.",
        }
    parts = []
    for idx, it in found[:3]:
        desc = (it["description"] or "")[:200]
        if len((it["description"] or "")) > 200:
            desc += "..."
        parts.append(f"• [{idx}] {it['title']}\n  {desc}")
    return {"reply": "다음 뉴스가 질문과 관련 있어 보입니다:\n\n" + "\n\n".join(parts)}
