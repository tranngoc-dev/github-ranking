import subprocess, json, urllib.request, re, sys, os

sys.stdout.reconfigure(encoding='utf-8')

raw_base = 'https://raw.githubusercontent.com/GitHubDaily/GitHubDaily/master/'
files = ['README.md', '2024.md', '2023.md', '2022.md', '2021.md', '2020.md', '2019.md', '2018.md']

ordered_rules = [
    ('utilities', ['实用工具', '有趣 / 实用开源工具', '非开源的实用工具', '趣味工具']),
    ('plugins', ['实用插件', 'Chrome 插件', 'VSCode 插件', '插件']),
    ('ai-tools', ['AI 工具', 'AI 技术', '机器学习/人工智能', '机器学习 / 人工智能', 'AI 绘画', 'AIGC', 'AI']),
    ('media-tools', ['媒体工具', '开源字体', '图标库', '字体']),
    ('content-creation', ['内容创作']),
    ('tutorials', ['学习教程', '开源书籍/教程', '书籍/教程', '开源书籍', '免费书籍', '教程']),
    ('collections', ['资料集合', '面试资料', '资料']),
    ('libraries-frameworks', ['编程语言/库', 'Java', 'Python', 'Go', '前端', '移动端', 'C++', 'C', 'PHP', 'Ruby', 'Swift', 'JavaScript', 'Rust']),
    ('online-services', ['在线服务', '有趣/实用网站', '有趣网站']),
    ('dev-tools', ['开发工具', '命令行工具', '工具']),
    ('other', ['其他', '其它'])
]

def get_cat(h):
    h = h.strip()
    for cid, list_h in ordered_rules:
        for lh in list_h:
            if lh in h:
                return cid
    return 'other'

url_to_cat = {}
for f in files:
    try:
        req = urllib.request.Request(raw_base + f, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as res:
            content = res.read().decode('utf-8')
            cur_cat = 'other'
            for line in content.split('\n'):
                line_str = line.strip()
                if line_str.startswith('#'):
                    h_text = line_str.lstrip('#').strip()
                    cur_cat = get_cat(h_text)
                urls = re.findall(r'https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', line)
                for u in urls:
                    clean_u = u.rstrip('.)/|')
                    if clean_u not in url_to_cat:
                        url_to_cat[clean_u.lower()] = cur_cat
    except Exception as e:
        print(f'Error fetching {f}: {e}')

output = subprocess.check_output(['git', 'show', '47faed3:src/data/projects.json'], encoding='utf-8')
all_projects = json.loads(output)

final_projects = []
for p in all_projects:
    u = p.get('repoUrl', '').lower().rstrip('/')
    if 'github.com/githubdaily/githubdaily' in u:
        continue  # filter out self reference
    
    y = int(p.get('year', 0))
    if y == 2026:
        cat = 'community-picks'
    else:
        cat = url_to_cat.get(u, 'other')
    
    p['categoryVi'] = cat
    p['year'] = y
    # Clean any GitHubDaily strings from summary
    if p.get('summaryVi'):
        p['summaryVi'] = p['summaryVi'].replace('GitHubDaily', '').replace('GitHub Daily', '').strip()
    final_projects.append(p)

with open('src/data/projects.json', 'w', encoding='utf-8') as f:
    json.dump(final_projects, f, ensure_ascii=False, indent=2)

categories = [
    {"id": "ai-tools", "name": "Công cụ AI & Machine Learning"},
    {"id": "dev-tools", "name": "Công cụ Lập trình & DevTools"},
    {"id": "utilities", "name": "Tiện ích Thực tế & Ứng dụng"},
    {"id": "collections", "name": "Tài liệu Tổng hợp & Tuyển tập"},
    {"id": "tutorials", "name": "Giáo trình & Hướng dẫn Lập trình"},
    {"id": "libraries-frameworks", "name": "Ngôn ngữ Lập trình & Thư viện"},
    {"id": "community-picks", "name": "Dự án Cộng đồng Đề xuất"},
    {"id": "media-tools", "name": "Công cụ Đa phương tiện & Media"},
    {"id": "plugins", "name": "Plugin & Tiện ích Mở rộng"},
    {"id": "content-creation", "name": "Sáng tạo Nội dung & Xuất bản"},
    {"id": "online-services", "name": "Dịch vụ Trực tuyến & Web Apps"},
    {"id": "other", "name": "Dự án Khác"}
]

with open('src/data/categories.json', 'w', encoding='utf-8') as f:
    json.dump(categories, f, ensure_ascii=False, indent=2)

print(f'Done! Saved {len(final_projects)} projects with 12 standardized categories.')
