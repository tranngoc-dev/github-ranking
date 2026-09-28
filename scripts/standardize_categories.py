import json
import urllib.request
import re
import os

repo_raw_url = "https://raw.githubusercontent.com/GitHubDaily/GitHubDaily/master/"
files_to_process = ["README.md", "2024.md", "2023.md", "2022.md", "2021.md", "2020.md", "2019.md", "2018.md"]

category_mapping = {
    'ai-tools': ['AI 工具', 'AI 技术', '机器学习/人工智能', 'AIGC', 'AI 绘画', 'AI'],
    'dev-tools': ['开发工具', '工具', '命令行工具'],
    'tutorials': ['学习教程', '书籍/教程', '开源书籍/教程', '教程', '免费书籍', '开源书籍'],
    'collections': ['资料集合', '面试资料', '资料'],
    'utilities': ['实用工具', '有趣 / 实用开源工具', '非开源的实用工具', '趣味工具'],
    'plugins': ['实用插件', '插件', 'Chrome 插件', 'VSCode 插件'],
    'media-tools': ['媒体工具', '开源字体', '图标库', '字体'],
    'content-creation': ['内容创作'],
    'libraries-frameworks': ['编程语言/库', 'Java', 'Python', 'Go', '前端', '移动端', 'C++', 'C', 'PHP', 'Ruby', 'Swift', 'Objective-C', 'JavaScript', 'CSS', 'HTML', 'Rust', 'C#'],
    'online-services': ['在线服务', '有趣网站', '有趣/实用网站'],
    'community-picks': [],
    'other': ['其他', '其它', '企业']
}

cat_ids = {
    'ai-tools': 'Công cụ AI & Machine Learning',
    'dev-tools': 'Công cụ Lập trình & DevTools',
    'tutorials': 'Giáo trình & Hướng dẫn Lập trình',
    'collections': 'Tài liệu Tổng hợp & Tuyển tập',
    'utilities': 'Tiện ích Thực tế & Ứng dụng',
    'plugins': 'Plugin & Tiện ích Mở rộng',
    'media-tools': 'Công cụ Đa phương tiện & Media',
    'content-creation': 'Sáng tạo Nội dung & Xuất bản',
    'libraries-frameworks': 'Ngôn ngữ Lập trình & Thư viện',
    'online-services': 'Dịch vụ Trực tuyến & Web Apps',
    'community-picks': 'Dự án Cộng đồng Đề xuất',
    'other': 'Dự án Khác'
}

def map_heading_to_cat(heading):
    heading = heading.strip()
    for cat_id, matches in category_mapping.items():
        if heading in matches:
            return cat_id
    return 'other'

projects = []
proj_id = 1

def process_file(filename):
    global proj_id
    year = "2025"
    if filename != "README.md":
        year = filename.replace(".md", "")
    
    try:
        url = repo_raw_url + filename
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req)
        content = response.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching {filename}: {e}")
        return

    current_cat_id = 'other'
    
    for line in content.split('\n'):
        if line.startswith('### '):
            heading = line.replace('### ', '').strip()
            current_cat_id = map_heading_to_cat(heading)
        
        # Matches markdown table row: [name](url)|summary
        m_table = re.match(r'^\[(.+?)\]\((.+?)\)\|(.+)', line.strip())
        # Matches list item: - [name](url): summary
        m_list = re.match(r'^- \[(.+?)\]\((.+?)\)[:：]\s*(.+)', line.strip())
        
        m = m_table or m_list
        if m:
            name, url, summary = m.groups()
            
            # Clean up summary
            summary = summary.replace('GitHubDaily', '').replace('GitHub Daily', '').strip()
            
            if 'github.com/GitHubDaily' in url:
                continue
                
            projects.append({
                'id': str(proj_id),
                'name': name,
                'repoUrl': url,
                'author': url.split('/')[-2] if 'github.com' in url else '',
                'categoryVi': current_cat_id,
                'summaryVi': summary,
                'stars': 0,
                'language': 'N/A',
                'year': year
            })
            proj_id += 1

for f in files_to_process:
    process_file(f)

# Keep existing 2026 projects if they exist in projects.json
existing_projects = []
if os.path.exists('src/data/projects.json'):
    with open('src/data/projects.json', 'r', encoding='utf-8') as f:
        existing_projects = json.load(f)
    for p in existing_projects:
        if p.get('year') == '2026':
            p['categoryVi'] = 'community-picks'
            # fix id
            p['id'] = str(proj_id)
            proj_id += 1
            if p['repoUrl'] != 'https://github.com/GitHubDaily/GitHubDaily':
                # Check for dup
                dup = False
                for ep in projects:
                    if ep['repoUrl'] == p['repoUrl']:
                        dup = True
                        break
                if not dup:
                    projects.append(p)

with open('src/data/projects.json', 'w', encoding='utf-8') as f:
    json.dump(projects, f, ensure_ascii=False, indent=2)

categories = [{"id": k, "name": v} for k, v in cat_ids.items()]
with open('src/data/categories.json', 'w', encoding='utf-8') as f:
    json.dump(categories, f, ensure_ascii=False, indent=2)

print(f"Total projects: {len(projects)}")
