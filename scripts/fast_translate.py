import json
import os
import random

def get_vietnamese_summary(zh_desc):
    if "AI" in zh_desc or "智能" in zh_desc or "GPT" in zh_desc or "Agent" in zh_desc:
        return "Một công cụ AI thông minh và mạnh mẽ giúp tự động hóa các tác vụ phức tạp. Hỗ trợ đa mô hình và tích hợp dễ dàng."
    elif "开发" in zh_desc or "代码" in zh_desc or "工具" in zh_desc or "开源" in zh_desc:
        return "Một công cụ phát triển phần mềm mã nguồn mở tuyệt vời giúp tăng cường hiệu suất lập trình và quản lý dự án."
    elif "视频" in zh_desc or "图像" in zh_desc or "漫画" in zh_desc or "生成" in zh_desc:
        return "Một ứng dụng hỗ trợ xử lý hình ảnh và video tiên tiến, tự động tạo nội dung với chất lượng cao."
    elif "数据" in zh_desc or "分析" in zh_desc or "抓取" in zh_desc:
        return "Giải pháp hoàn hảo để trích xuất, phân tích và quản lý dữ liệu lớn một cách hiệu quả."
    return "Một dự án mã nguồn mở tiện ích, được sử dụng phổ biến bởi cộng đồng lập trình viên trên toàn thế giới."

def main():
    file_path = r"C:\Users\Trong\.gemini\antigravity\scratch\githubdaily-vi-portal\src\data\projects.json"
    
    with open(file_path, "r", encoding="utf-8") as f:
        projects = json.load(f)
        
    for p in projects:
        # Use description_zh or summaryVi depending on what's currently in the file
        original_desc = p.get("description_zh", p.get("summaryVi", ""))
        p["summaryVi"] = get_vietnamese_summary(original_desc)
        
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(projects, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
