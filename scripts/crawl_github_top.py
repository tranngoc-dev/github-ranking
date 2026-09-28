import os
import requests
import json
import time
import re

TOKEN = os.environ.get('GITHUB_TOKEN')
HEADERS = {'Authorization': f'token {TOKEN}'} if TOKEN else {}

ranges = [
    (100000, 1000000),
    (50000, 99999),
    (35000, 49999),
    (25000, 34999),
    (20000, 24999),
    (17000, 19999),
    (14500, 16999),
    (12500, 14499),
    (11000, 12499),
    (10000, 10999)
]

def clean_description(desc, name, language):
    if not desc:
        return f"Top open-source {language or ''} project for {name}."
    
    # Strip markdown badges
    desc = re.sub(r'\[\!\[.*?\]\(.*?\)\](?:.*?$)?', '', desc)
    # Strip markdown links
    desc = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', desc)
    # Strip advertising notes
    desc = re.sub(r'\[NOTE:.*?\]', '', desc)
    
    desc = desc.strip()
    
    # Strip boilerplate openers
    replacements = {
        'A curated list of': 'Curated collection of',
        'An awesome': 'Awesome collection of',
        'Welcome to ': ''
    }
    
    for old, new in replacements.items():
        if desc.startswith(old):
            desc = desc.replace(old, new, 1)
            break
            
    # Truncate at 180 chars
    if len(desc) > 180:
        desc = desc[:177] + '...'
        
    return desc.strip()

def get_category(topics, desc):
    topics = [t.lower() for t in topics]
    desc = desc.lower() if desc else ""
    combined = " ".join(topics) + " " + desc
    
    if any(k in combined for k in ['ai', 'llm', 'machine-learning', 'deep-learning', 'gpt', 'model', 'agent', 'nlp', 'cv', 'pytorch', 'tensorflow', 'diffusers']):
        return 'ai-ml'
    if any(k in combined for k in ['devops', 'cli', 'developer-tools', 'terminal', 'git', 'docker', 'kubernetes', 'linux', 'editor', 'neovim', 'shell']):
        return 'dev-tools'
    if any(k in combined for k in ['tutorial', 'course', 'interview', 'roadmap', 'book', 'learn', 'awesome', 'guide', 'algorithm', 'leetcodes']):
        return 'learning-guides'
    if any(k in combined for k in ['api', 'cloud', 'serverless', 'database', 'backend', 'web', 'proxy', 'auth', 'redis', 'postgres']):
        return 'cloud-services'
    if any(k in combined for k in ['framework', 'library', 'runtime', 'compiler', 'react', 'vue', 'angular', 'svelte', 'rust', 'golang', 'python', 'typescript']):
        return 'frameworks-libs'
    
    return 'apps-utilities'

def main():
    projects = []
    seen_urls = set()
    
    for min_s, max_s in ranges:
        page = 1
        while True:
            if min_s == 100000:
                q = f"stars:>{min_s}"
            else:
                q = f"stars:{min_s}..{max_s}"
                
            url = f"https://api.github.com/search/repositories?q={q}&sort=stars&order=desc&per_page=100&page={page}"
            print(f"Fetching {url}")
            
            resp = requests.get(url, headers=HEADERS)
            if resp.status_code != 200:
                print(f"Error {resp.status_code}: {resp.text}")
                break
                
            data = resp.json()
            items = data.get('items', [])
            
            if not items:
                break
                
            for r in items:
                url_lower = r['html_url'].lower()
                if url_lower in seen_urls:
                    continue
                seen_urls.add(url_lower)
                
                lang = r.get('language') or 'General'
                desc = r.get('description', '')
                topics = r.get('topics', [])
                
                proj = {
                    'id': f"repo-{r['id']}",
                    'name': r['name'],
                    'repoUrl': r['html_url'],
                    'author': r['owner']['login'],
                    'stars': r['stargazers_count'],
                    'forks': r.get('forks_count', 0),
                    'language': lang,
                    'year': int(r['created_at'][:4]) if r.get('created_at') else 2024,
                    'categoryVi': get_category(topics, desc),
                    'summaryVi': clean_description(desc, r['name'], lang)
                }
                projects.append(proj)
                
            if len(items) < 100:
                break
                
            page += 1
            time.sleep(1.2)
            
    print(f"Crawled {len(projects)} projects.")
    
    with open('src/data/projects.json', 'w', encoding='utf-8') as f:
        json.dump(projects, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()
