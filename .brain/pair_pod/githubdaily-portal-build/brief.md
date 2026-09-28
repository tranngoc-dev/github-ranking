# TASK BRIEF: GitHubDaily Vietnamese Discovery Portal
SIGN_OFF: approved


## CONTEXT
Xây dựng một web portal hiện đại bằng Next.js 15 (App Router, Tailwind CSS, TypeScript) đóng gói dữ liệu từ repo GitHubDaily/GitHubDaily, chuyển ngữ mô tả sang Tiếng Việt chuẩn mực, hỗ trợ tìm kiếm tức thì với Fuse.js, có bộ lọc theo năm/thể loại, sẵn sàng deploy lên Vercel.

## SCOPE
- Workspace: C:\Users\Trong\.gemini\antigravity\scratch\githubdaily-vi-portal
- Scripts:
  - `scripts/extract_data.js`: Bóc tách dữ liệu từ các tệp markdown của GitHubDaily (hoặc API/raw markdown đã fetch), dịch mô tả sang Tiếng Việt chất lượng cao, chuẩn hóa danh mục.
- Data:
  - `src/data/projects.json`: Chứa các project đã được chuẩn hóa với các trường (id, name, repoUrl, author, categoryVi, summaryVi, stars, language, year).
  - `src/data/categories.json`: Danh sách danh mục thể loại Tiếng Việt.
- App Structure:
  - Next.js 15 App Router (`src/app/layout.tsx`, `src/app/page.tsx`, `src/app/globals.css`).
  - Components: `Header.tsx`, `Hero.tsx`, `SearchFilter.tsx`, `ProjectCard.tsx`, `ProjectModal.tsx`.
- Configuration:
  - `package.json`, `tsconfig.json`, `next.config.ts`, `tailwind.config.ts` (hoặc Tailwind v4 css).
- Deployment:
  - `README.md` & `DEPLOY_VERCEL.md` hướng dẫn deploy lên Vercel và GitHub Actions cron sync.

## ACCEPTANCE
1. Dữ liệu: Ít nhất 100+ dự án tiêu biểu từ 2025/2024 được trích xuất và dịch Tiếng Việt chuẩn xác.
2. Tìm kiếm: Gõ từ khóa vào ô search nảy kết quả tức thì (< 10ms) với Fuse.js.
3. Bộ lọc: Lọc mượt mà theo năm (2025, 2024...), theo danh mục (Công cụ AI, DevTools, Frameworks, v.v.), sắp xếp theo Stars.
4. Giao diện: Thiết kế đẹp mắt phong cách ProductHunt, hỗ trợ Dark/Light mode, responsive 100% trên Mobile & Desktop.
5. Build: Chạy `npm run build` thành công không có lỗi TypeScript hay Linter.

## EDGE
1. Xử lý trường hợp không có kết quả tìm kiếm (Empty state thân thiện).
2. Xử lý hiển thị an toàn khi URL repo hoặc logo không khả dụng.
3. Xử lý dự án có mô tả dài, cắt gọn và hiển thị modal chi tiết khi click.
4. Tương thích Vercel Static Site Generation (SSG).
