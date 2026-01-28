-- Supabase (PostgreSQL) 테이블. Dashboard > SQL Editor에서 실행.

-- 뉴스 검색 로그
create table if not exists news_searches (
  id         uuid primary key default gen_random_uuid(),
  keyword    text not null,
  sort       text not null,
  total      int  not null,
  created_at timestamptz default now()
);

-- 채팅 메시지 로그
create table if not exists chat_messages (
  id         uuid primary key default gen_random_uuid(),
  keyword    text not null default '',
  role       text not null,
  message    text not null,
  created_at timestamptz default now()
);

-- RLS 활성화 후 anon으로 insert 허용 (Supabase anon key 사용 시)
ALTER TABLE news_searches ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_messages ENABLE ROW LEVEL SECURITY;

-- 기존 정책 삭제
DROP POLICY IF EXISTS "Allow anon insert news_searches" ON news_searches;
DROP POLICY IF EXISTS "Allow anon insert chat_messages" ON chat_messages;

-- INSERT 정책 생성 (anon 사용자가 데이터 삽입 가능)
CREATE POLICY "Allow anon insert news_searches"
  ON news_searches
  FOR INSERT
  TO anon
  WITH CHECK (true);

CREATE POLICY "Allow anon insert chat_messages"
  ON chat_messages
  FOR INSERT
  TO anon
  WITH CHECK (true);
