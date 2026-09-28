import requests
import json
import os
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from deep_translator import GoogleTranslator

# Constants
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
HEADERS = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'User-Agent': 'Mozilla/5.0',
    'Accept': 'application/vnd.github.v3+json'
}

DATA_DIR = os.path.join('src', 'data')
PROJECTS_FILE = os.path.join(DATA_DIR, 'projects.json')
CATEGORIES_FILE = os.path.join(DATA_DIR, 'categories.json')

def translate_to_vi(text):
    if not text:
        return "Dự án nguồn mở nổi bật trên GitHub."
    try:
        translator = GoogleTranslator(source='auto', target='vi')
        translated = translator.translate(text)
        return translated
    except Exception as e:
        print(f"Translation error: {e}")
        return text

def get_category(topics, description):
    text = (description + ' ' + ' '.join(topics)).lower()
    
    if any(k in text for k in ['ai', 'llm', 'machine-learning', 'deep-learning', 'gpt', 'model', 'agent']):
        return 'ai-tools'
    if any(k in text for k in ['devops', 'cli', 'developer-tools', 'terminal', 'git', 'docker', 'kubernetes']):
        return 'dev-tools'
    if any(k in text for k in ['tutorial', 'course', 'interview', 'roadmap', 'book', 'learn']):
        return 'tutorials'
    if any(k in text for k in ['awesome', 'list', 'cheatsheet', 'collection']):
        return 'collections'
    if any(k in text for k in ['plugin', 'extension']):
        return 'plugins'
    if any(k in text for k in ['font', 'icon', 'media', 'audio', 'video', 'image']):
        return 'media-tools'
    if any(k in text for k in ['framework', 'library', 'runtime', 'compiler']):
        return 'libraries-frameworks'
    
    return 'utilities'

def process_repo(r, rank):
    name = r.get('name')
    repoUrl = r.get('html_url')
    author = r.get('owner', {}).get('login', 'Unknown')
    stars = r.get('stargazers_count', 0)
    language = r.get('language') or 'General'
    created_at = r.get('created_at')
    year = int(created_at[:4]) if created_at else 2024
    description = r.get('description') or ''
    topics = r.get('topics') or []
    
    summaryVi = translate_to_vi(description)
    if not summaryVi or summaryVi == description and not description:
        summaryVi = f"Dự án {name} với nhiều chủ đề nổi bật."
        
    categoryVi = get_category(topics, description)
    
    return {
        'id': f'proj-top-{rank}',
        'name': name,
        'repoUrl': repoUrl,
        'author': author,
        'categoryVi': categoryVi,
        'summaryVi': summaryVi,
        'stars': stars,
        'language': language,
        'year': year,
        'isTop1000': True
    }

def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Load existing projects
    if os.path.exists(PROJECTS_FILE):
        with open(PROJECTS_FILE, 'r', encoding='utf-8') as f:
            projects = json.load(f)
    else:
        projects = []
        
    # Build dictionary by repoUrl
    projects_by_url = {p['repoUrl'].lower(): p for p in projects}
    
    print("Fetching Top 1000 repositories from GitHub...")
    top_repos = []
    
    for page in range(1, 11):
        url = f'https://api.github.com/search/repositories?q=stars:>1000&sort=stars&order=desc&per_page=100&page={page}'
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            items = data.get('items', [])
            top_repos.extend(items)
            print(f"Fetched page {page} - {len(items)} items")
        else:
            print(f"Error fetching page {page}: {response.status_code} - {response.text}")
        
        time.sleep(1.5)
        
    print(f"Total fetched repos: {len(top_repos)}")
    
    # Process repos in parallel
    print("Processing and translating repositories...")
    processed_repos = []
    
    # To maintain order and correct rank, we submit tasks with rank
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(process_repo, r, i+1): r for i, r in enumerate(top_repos)}
        for future in futures:
            try:
                processed = future.result()
                processed_repos.append(processed)
            except Exception as e:
                print(f"Error processing repo: {e}")
                
    # processed_repos might be out of order from ThreadPoolExecutor, so let's sort them by rank
    processed_repos.sort(key=lambda x: int(x['id'].split('-')[-1]))
    
    # Now merge into projects list
    for idx, new_p in enumerate(processed_repos):
        url_lower = new_p['repoUrl'].lower()
        if url_lower in projects_by_url:
            p = projects_by_url[url_lower]
            p['stars'] = new_p['stars']
            p['isTop1000'] = True
        else:
            projects.append(new_p)
            projects_by_url[url_lower] = new_p

    # Reset isTop1000 for any older projects that might have fallen out of Top 1000
    # Wait, the prompt says "Ensure total projects with isTop1000: True is exactly 1000!"
    top_1000_urls = {r['repoUrl'].lower() for r in processed_repos}
    for p in projects:
        if p['repoUrl'].lower() not in top_1000_urls:
            p.pop('isTop1000', None)
            
    with open(PROJECTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(projects, f, ensure_ascii=False, indent=2)
        
    print(f"Saved {len(projects)} projects to {PROJECTS_FILE}")
    
    # Update categories.json
    if os.path.exists(CATEGORIES_FILE):
        with open(CATEGORIES_FILE, 'r', encoding='utf-8') as f:
            categories = json.load(f)
    else:
        categories = []
        
    # Remove existing top-1000 if present
    categories = [c for c in categories if c['id'] != 'top-1000']
    
    # Prepend top-1000
    top_1000_cat = {
        "id": "top-1000",
        "name": "⭐ Top 1000 Nhiều Sao Nhất"
    }
    categories.insert(0, top_1000_cat)
    
    with open(CATEGORIES_FILE, 'w', encoding='utf-8') as f:
        json.dump(categories, f, ensure_ascii=False, indent=2)
        
    print(f"Updated categories in {CATEGORIES_FILE}")

if __name__ == '__main__':
    main()
