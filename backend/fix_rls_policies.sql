-- RLS 정책 수정/생성 스크립트
-- Supabase Dashboard > SQL Editor에서 실행

-- 기존 정책 삭제
DROP POLICY IF EXISTS "Allow anon insert news_searches" ON news_searches;
DROP POLICY IF EXISTS "Allow anon insert chat_messages" ON chat_messages;
DROP POLICY IF EXISTS "Allow anon select news_searches" ON news_searches;
DROP POLICY IF EXISTS "Allow anon select chat_messages" ON chat_messages;

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

-- SELECT 정책 생성 (anon 사용자가 데이터 조회 가능 - 선택사항)
CREATE POLICY "Allow anon select news_searches"
  ON news_searches
  FOR SELECT
  TO anon
  USING (true);

CREATE POLICY "Allow anon select chat_messages"
  ON chat_messages
  FOR SELECT
  TO anon
  USING (true);

-- 정책 확인
SELECT 
  schemaname,
  tablename,
  policyname,
  permissive,
  roles,
  cmd,
  qual,
  with_check
FROM pg_policies
WHERE tablename IN ('news_searches', 'chat_messages')
ORDER BY tablename, policyname;
