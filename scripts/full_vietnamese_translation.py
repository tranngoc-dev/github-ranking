import os
import json
import re
import time
import urllib.request
import urllib.parse
from concurrent.futures import ThreadPoolExecutor

try:
    from deep_translator import MyMemoryTranslator
except ImportError:
    os.system('pip install deep_translator')
    from deep_translator import MyMemoryTranslator

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'src', 'data', 'projects.json')
CACHE_PATH = os.path.join(os.path.dirname(__file__), 'translation_cache.json')

my_memory_en = MyMemoryTranslator(source='en-US', target='vi-VN')
my_memory_zh = MyMemoryTranslator(source='zh-CN', target='vi-VN')

cache = {}
if os.path.exists(CACHE_PATH):
    try:
        with open(CACHE_PATH, 'r', encoding='utf-8') as f:
            cache = json.load(f)
    except:
        pass

def save_cache():
    with open(CACHE_PATH, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

def clean_summary(text):
    if not text:
        return ''
    t = text.strip()
    t = re.sub(r'đại lý AI|của đại lý|đại lý', 'AI Agent', t, flags=re.IGNORECASE)
    t = re.sub(r'\bcơ sở mã\b', 'Mã nguồn', t, flags=re.IGNORECASE)
    t = re.sub(r'kéo yêu cầu', 'Pull Request', t, flags=re.IGNORECASE)
    t = re.sub(r'GitHubDaily|GitHub Daily', '', t, flags=re.IGNORECASE)
    
    prefixes = [
        r'^(Một\s+(công\s+cụ|ứng\s+dụng|dự\s+án|thư\s+viện|nền\s+tảng|giải\s+pháp|kho\s+lưu\s+trữ|tiện\s+ích|hệ\s+thống|framework)\s*(mã\s+nguồn\s+mở|nguồn\s+mở|trực\s+tuyến|tuyệt\s+vời|mạnh\s+mẽ|tiên\s+tiến|hàng\s+đầu|phổ\s+biến)*\s*(giúp|cho\s+phép|hỗ\s+trợ|dùng\s+để)?\s*)',
        r'^(Đây\s+là\s+(một\s+)?(công\s+cụ|ứng\s+dụng|dự\s+án|thư\s+viện|nền\s+tảng)\s*)',
        r'^(Thu\s+thập\s+số\s+lượng\s+lớn\s+|Thu\s+thập\s+)',
        r'^(Nắm\s+vững\s+lập\s+trình\s+bằng\s+cách\s+)'
    ]
    for p in prefixes:
        t = re.sub(p, '', t, flags=re.IGNORECASE).strip()
    
    t = re.sub(r'^giúp\s+', '', t, flags=re.IGNORECASE).strip()
    if t.startswith('tái tạo lại '):
        t = 'Hướng dẫn tự xây dựng lại ' + t[12:]
    elif t.startswith('tạo lại '):
        t = 'Hướng dẫn tự xây dựng lại ' + t[8:]
    elif t.startswith('các API công khai') or t.startswith('public API'):
        t = 'Tổng hợp ' + t
    
    if t:
        t = t[0].upper() + t[1:]
    if len(t) > 200:
        t = t[:197] + '...'
    return t

def translate_text(text):
    if not text or len(text.strip()) < 2:
        return text
    text_clean = re.sub(r'\[\!\[.*?\]\(.*?\)\].*', '', text).split('|')[0].strip()
    text_clean = re.sub(r'\[NOTE:.*?\]', '', text_clean).strip()
    text_clean = re.sub(r'GitHubDaily|GitHub Daily', '', text_clean, flags=re.IGNORECASE).strip()
    
    if text_clean in cache:
        return clean_summary(cache[text_clean])

    # 1. Primary: Google dict-chrome-ex
    try:
        url = 'https://translate.googleapis.com/translate_a/single?client=dict-chrome-ex&sl=auto&tl=vi&dt=t&q=' + urllib.parse.quote(text_clean)
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=6) as res:
            data = json.loads(res.read().decode('utf-8'))
            res_text = ''.join(part[0] for part in data[0] if part and part[0])
            if res_text and not re.search(r'[\u4e00-\u9fff]', res_text):
                cache[text_clean] = res_text
                return clean_summary(res_text)
    except Exception:
        pass

    # 2. Secondary Fallback: MyMemory
    try:
        if re.search(r'[\u4e00-\u9fff]', text_clean):
            res_text = my_memory_zh.translate(text_clean)
        else:
            res_text = my_memory_en.translate(text_clean)
        if res_text:
            cache[text_clean] = res_text
            return clean_summary(res_text)
    except Exception:
        pass

    return clean_summary(text_clean)

def fetch_raw_descriptions():
    url_to_raw_desc = {}
    files = ['README.md'] + [f'{y}.md' for y in range(2017, 2026)]
    base_url = 'https://raw.githubusercontent.com/GitHubDaily/GitHubDaily/master/'
    
    for f in files:
        try:
            req = urllib.request.Request(base_url + f, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as res:
                content = res.read().decode('utf-8')
                for line in content.split('\n'):
                    # Match [name](url) | desc or - [name](url): desc
                    match1 = re.search(r'\[([^\]]+)\]\((https?://github\.com/[^\)]+)\)\s*\|\s*(.*)', line)
                    match2 = re.search(r'-\s*\[([^\]]+)\]\((https?://github\.com/[^\)]+)\)[：:\s]+(.*)', line)
                    
                    if match1:
                        url = match1.group(2).lower().rstrip('/')
                        desc = match1.group(3)
                        url_to_raw_desc[url] = desc
                    elif match2:
                        url = match2.group(2).lower().rstrip('/')
                        desc = match2.group(3)
                        url_to_raw_desc[url] = desc
        except Exception as e:
            print(f"Failed to fetch {f}: {e}")
            
    return url_to_raw_desc

def needs_translation(text):
    if not text: return False
    if re.search(r'[\u4e00-\u9fff]', text): return True
    # English check is harder, but we can rely on url_to_raw_desc translation anyway
    return True # We'll just run it on everything, cache will handle it quickly

def process_project(proj, url_to_raw_desc):
    url = proj.get('repoUrl', '').lower().rstrip('/')
    
    if url in url_to_raw_desc:
        raw_desc = url_to_raw_desc[url]
    else:
        raw_desc = proj.get('summaryVi', '')
        
    # Translate & Clean
    vi_desc = translate_text(raw_desc)
    proj['summaryVi'] = vi_desc
    return proj

def main():
    print("Fetching raw descriptions...")
    url_to_raw_desc = fetch_raw_descriptions()
    
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        projects = json.load(f)
        
    print(f"Loaded {len(projects)} projects.")
    
    processed = 0
    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = []
        for p in projects:
            futures.append(executor.submit(process_project, p, url_to_raw_desc))
            
        for i, fut in enumerate(futures):
            projects[i] = fut.result()
            processed += 1
            if processed % 100 == 0:
                print(f"Processed {processed}/{len(projects)}")
                save_cache()
                
    save_cache()
    
    with open(DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(projects, f, ensure_ascii=False, indent=2)
        
    # Analyze
    cn_count = 0
    en_count = 0 # Rough heuristic
    vi_count = 0
    
    for p in projects:
        t = p.get('summaryVi', '')
        if re.search(r'[\u4e00-\u9fff]', t):
            cn_count += 1
        elif re.search(r'\b(the|and|is|for|with|this|that)\b', t, re.IGNORECASE):
            en_count += 1
        else:
            vi_count += 1
            
    print(f"\nFinal breakdown:\nChinese: {cn_count}\nEnglish: {en_count}\nVietnamese: {vi_count}")
    
    # Spot checks
    spot_checks = ['build-your-own-x', 'awesome', 'public-apis', 'freeCodeCamp', 'anthropics/skills']
    print("\nSpot Checks:")
    for p in projects:
        for s in spot_checks:
            if s in p.get('repoUrl', ''):
                print(f"{s}: {p.get('summaryVi', '')}")

if __name__ == '__main__':
    main()
