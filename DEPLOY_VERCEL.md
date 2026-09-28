# Hướng dẫn Triển khai GitHubDaily Vietnamese Discovery Portal

Dự án này được thiết kế để dễ dàng triển khai lên Vercel.

## Yêu cầu
- Tài khoản [Vercel](https://vercel.com)
- Tài khoản GitHub (để lưu trữ mã nguồn)

## Triển khai lên Vercel
1. Đẩy (push) mã nguồn này lên một repository trên GitHub.
2. Đăng nhập vào Vercel, chọn **Add New... > Project**.
3. Import repository GitHub mà bạn vừa tạo.
4. Cấu hình Framework Preset là **Next.js**.
5. Nhấn **Deploy** và chờ Vercel hoàn thành.

## Đồng bộ dữ liệu hằng ngày (Daily Sync)
Dự án sử dụng GitHub Actions để tự động cập nhật dữ liệu từ repository `GitHubDaily/GitHubDaily` mỗi ngày.

Workflow đã được cấu hình trong file `.github/workflows/daily-sync.yml`. 
Nó sẽ:
1. Chạy lúc 00:00 UTC mỗi ngày (thông qua `schedule: cron`).
2. Tải về file `README.md` mới nhất.
3. Chạy script Python để phân tích và dịch các dự án mới (cần thiết lập Google Translator hoặc LLM API).
4. Commit và push dữ liệu mới vào file `src/data/projects.json`.
5. Vercel sẽ tự động trigger deploy mới khi có commit đẩy lên nhánh `main`.

Lưu ý: Nếu sử dụng API dịch thuật có key (như OpenAI, Gemini), hãy thêm API Key vào GitHub repository **Secrets** và cấu hình trong workflow.
