import json
import re
import urllib.request
import urllib.parse
import time
from concurrent.futures import ThreadPoolExecutor

# List of files to fetch
files = ['README.md', '2024.md', '2023.md', '2022.md', '2021.md', '2020.md', '2019.md', '2018.md']
base_url = 'https://raw.githubusercontent.com/GitHubDaily/GitHubDaily/master/'

url_to_raw_desc = {}

print("Fetching raw markdown files...")
for file in files:
    try:
        req = urllib.request.Request(base_url + file, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as res:
            content = res.read().decode('utf-8')
            # Parse links
            lines = content.split('\n')
            for line in lines:
                match = re.search(r'\[([^\]]+)\]\((https?://github\.com/[^\)]+)\)(.*)', line)
                if match:
                    name = match.group(1)
                    url = match.group(2).lower().rstrip('/')
                    rest = match.group(3).strip()
                    rest = re.sub(r'^[\s\|\-\:]+', '', rest).strip()
                    if rest:
                        url_to_raw_desc[url] = rest
    except Exception as e:
        print(f"Failed to fetch {file}: {e}")

print(f"Extracted {len(url_to_raw_desc)} raw descriptions from GitHubDaily.")

projects_path = 'src/data/projects.json'
with open(projects_path, 'r', encoding='utf-8') as f:
    projects = json.load(f)

def translate_text(text):
    if not text or len(text.strip()) < 3:
        return text
    url = 'https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=vi&dt=t&q=' + urllib.parse.quote(text)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    for _ in range(3):
        try:
            with urllib.request.urlopen(req, timeout=8) as res:
                data = json.loads(res.read().decode('utf-8'))
                return ''.join(part[0] for part in data[0] if part and part[0])
        except Exception as e:
            time.sleep(0.5)
    return text

def clean_summary(text):
    if not text:
        return text
    
    text = re.sub(r'(?i)đại lý AI', 'AI Agent', text)
    text = re.sub(r'(?i)của đại lý', 'của AI Agent', text)
    text = re.sub(r'(?i)đại lý', 'AI Agent', text)
    text = re.sub(r'(?i)cơ sở mã', 'Mã nguồn', text)
    text = re.sub(r'(?i)kéo yêu cầu', 'Pull Request', text)
    text = re.sub(r'(?i)GitHubDaily', '', text)
    text = re.sub(r'(?i)GitHub Daily', '', text)
    
    prefix_pattern1 = r'^(Một\s+(công\s+cụ|ứng\s+dụng|dự\s+án|thư\s+viện|nền\s+tảng|giải\s+pháp|kho\s+lưu\s+trữ|tiện\s+ích|hệ\s+thống|framework)\s*(mã\s+nguồn\s+mở|nguồn\s+mở|trực\s+tuyến|tuyệt\s+vời|mạnh\s+mẽ|tiên\s+tiến|hàng\s+đầu|phổ\s+biến)*\s*(giúp|cho\s+phép|hỗ\s+trợ|dùng\s+để)?\s*)'
    prefix_pattern2 = r'^(Đây\s+là\s+(một\s+)?(công\s+cụ|ứng\s+dụng|dự\s+án|thư\s+viện|nền\s+tảng)\s*)'
    prefix_pattern3 = r'^(Thu\s+thập\s+số\s+lượng\s+lớn\s+|Thu\s+thập\s+)'
    
    text = re.sub(prefix_pattern1, '', text, flags=re.IGNORECASE).strip()
    text = re.sub(prefix_pattern2, '', text, flags=re.IGNORECASE).strip()
    text = re.sub(prefix_pattern3, '', text, flags=re.IGNORECASE).strip()
    
    text = re.sub(r'^giúp\s+', '', text, flags=re.IGNORECASE).strip()
    
    if text:
        text = text[0].upper() + text[1:]
    
    if len(text) > 200:
        text = text[:197] + '...'
        
    return text.strip()

track_repos = ['build-your-own-x', 'awesome', 'public-apis', 'freeCodeCamp', 'anthropics/skills']
before_after = {}

def process_project(project):
    url = project.get('repoUrl', '').lower().rstrip('/')
    raw_desc = None
    
    if url in url_to_raw_desc:
        raw_desc = url_to_raw_desc[url]
    else:
        raw_desc = project.get('summaryVi', '')
    
    current_summary = project.get('summaryVi', '')
    
    repo_name = project.get('name', '')
    is_tracked = False
    if url and any(tr.lower() in url for tr in track_repos):
        is_tracked = True
        
    translated = translate_text(raw_desc)
    cleaned = clean_summary(translated)
    
    if is_tracked:
        before_after[repo_name] = {'before': current_summary, 'after': cleaned}
        
    project['summaryVi'] = cleaned
    return project

print("Processing projects...")
with ThreadPoolExecutor(max_workers=12) as executor:
    results = list(executor.map(process_project, projects))

with open(projects_path, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"Total projects processed: {len(results)}")

boilerplate_count = 0
for p in results:
    s = p.get('summaryVi', '')
    if re.search(r'^(Một công cụ|Đây là một|Ứng dụng mã nguồn mở)', s, flags=re.IGNORECASE):
        boilerplate_count += 1
print(f"Boilerplate count remaining: {boilerplate_count}")
print("Before/After examples:")
print(json.dumps(before_after, ensure_ascii=False, indent=2))
