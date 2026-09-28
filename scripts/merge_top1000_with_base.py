import json
import subprocess
import os

def load_json_from_commit(commit, filepath):
    try:
        content = subprocess.check_output(['git', 'show', f'{commit}:{filepath}'], text=True, encoding='utf-8')
        return json.loads(content)
    except subprocess.CalledProcessError as e:
        print(f"Error reading from commit: {e}")
        return []

def main():
    repo_dir = r"C:\Users\Trong\.gemini\antigravity\scratch\githubdaily-vi-portal"
    os.chdir(repo_dir)

    # 1. Read base projects from commit
    base_projects = load_json_from_commit('06067c5', 'src/data/projects.json')
    print(f"Base projects loaded: {len(base_projects)}")

    # 2. Read current projects
    with open('src/data/projects.json', 'r', encoding='utf-8') as f:
        current_projects = json.load(f)
    print(f"Current projects loaded: {len(current_projects)}")

    # 3. Filter Top 1000 from current
    top_1000_projects = [p for p in current_projects if p.get('isTop1000')]
    print(f"Top 1000 projects found: {len(top_1000_projects)}")

    # 4. Merge
    base_dict = {p['repoUrl'].lower().rstrip('/'): p for p in base_projects}
    
    for top_p in top_1000_projects:
        url_key = top_p['repoUrl'].lower().rstrip('/')
        if url_key in base_dict:
            base_dict[url_key]['stars'] = top_p.get('stars', base_dict[url_key].get('stars', 0))
            base_dict[url_key]['isTop1000'] = True
            if not base_dict[url_key].get('summaryVi'):
                base_dict[url_key]['summaryVi'] = top_p.get('summaryVi', '')
        else:
            base_dict[url_key] = top_p

    merged_projects = list(base_dict.values())
    
    # Ensure anthropics/skills is present
    anthropics_url = 'https://github.com/anthropics/skills'
    found_anthropics = False
    for p in merged_projects:
        if p['repoUrl'].lower().rstrip('/') == anthropics_url:
            p['isTop1000'] = True
            p['categoryId'] = 'ai-tools'
            if p.get('stars', 0) < 178000:
                p['stars'] = 178000
            found_anthropics = True
            
        # Clean "GitHubDaily" mentions from summaryVi
        if p.get('summaryVi'):
            p['summaryVi'] = p['summaryVi'].replace('GitHubDaily', '').replace('GithubDaily', '').replace('githubdaily', '')

    if not found_anthropics:
        merged_projects.append({
            "id": "anthropics-skills",
            "name": "anthropics/skills",
            "repoUrl": "https://github.com/anthropics/skills",
            "author": "anthropics",
            "categoryId": "ai-tools",
            "summaryVi": "Skills",
            "stars": 178000,
            "language": "TypeScript",
            "year": "2024",
            "isTop1000": True
        })

    top_count = sum(1 for p in merged_projects if p.get('isTop1000'))
    
    print(f"Merged projects count: {len(merged_projects)}")
    print(f"Top 1000 count: {top_count}")
    
    # Save combined
    with open('src/data/projects.json', 'w', encoding='utf-8') as f:
        json.dump(merged_projects, f, indent=2, ensure_ascii=False)

    # 5. Update categories
    categories = [
     { "id": "top-1000", "name": "⭐ Top 1000 Nhiều Sao Nhất" },
     { "id": "ai-tools", "name": "Công cụ AI & Machine Learning" },
     { "id": "dev-tools", "name": "Công cụ Lập trình & DevTools" },
     { "id": "utilities", "name": "Tiện ích Thực tế & Ứng dụng" },
     { "id": "collections", "name": "Tài liệu Tổng hợp & Tuyển tập" },
     { "id": "tutorials", "name": "Giáo trình & Hướng dẫn Lập trình" },
     { "id": "libraries-frameworks", "name": "Ngôn ngữ Lập trình & Thư viện" },
     { "id": "community-picks", "name": "Dự án Cộng đồng Đề xuất" },
     { "id": "media-tools", "name": "Công cụ Đa phương tiện & Media" },
     { "id": "plugins", "name": "Plugin & Tiện ích Mở rộng" },
     { "id": "content-creation", "name": "Sáng tạo Nội dung & Xuất bản" },
     { "id": "online-services", "name": "Dịch vụ Trực tuyến & Web Apps" },
     { "id": "other", "name": "Dự án Khác" }
    ]
    with open('src/data/categories.json', 'w', encoding='utf-8') as f:
        json.dump(categories, f, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    main()
