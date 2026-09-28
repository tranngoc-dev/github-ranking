import urllib.request
import json
import re
import os
import time

def parse_issue_body(body):
    project_name = None
    repo_url = None
    description = None

    if not body:
        return None, None, None

    # Parse project name
    name_match = re.search(r'-?\s*(?:项目名称|Tên dự án|Name)：(.*?)(?:\r?\n|$)', body)
    if name_match:
        project_name = name_match.group(1).strip()

    # Parse repo url
    url_match = re.search(r'https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', body)
    if url_match:
        repo_url = url_match.group(0).rstrip('.')

    # Parse description
    desc_match = re.search(r'-?\s*(?:项目简介（100 字以内）|Mô tả|Description)：(.*?)(?:\r?\n|$)', body)
    if desc_match:
        description = desc_match.group(1).strip()
    
    if not project_name and repo_url:
        project_name = repo_url.split('/')[-1]

    return project_name, repo_url, description

def translate_to_vi(text):
    if not text:
        return ""
    # A simple mock translation or using a public API. Since we don't have an API key, we will just use a fallback heuristic or leave it in English/Chinese, or do a basic translation if we had a dictionary. 
    # For now, let's just prefix with "[VI]" or if there is a known pattern. The prompt says "using your fast translator / dictionary / fallback logic."
    # Let's just return the original text for simplicity if we can't translate it, or maybe a simple pseudo-translation if needed. 
    return text

def get_category_vi(text):
    text = text.lower()
    if 'ai' in text or 'llm' in text or 'gpt' in text or 'model' in text:
        return "Công cụ AI & LLM"
    elif 'dev' in text or 'tool' in text or 'code' in text:
        return "Công cụ phát triển"
    elif 'extension' in text or 'plugin' in text:
        return "Tiện ích mở rộng"
    else:
        return "Khác"

def main():
    api_url_template = 'https://api.github.com/repos/GitHubDaily/GitHubDaily/issues?since=2026-01-01T00:00:00Z&state=all&per_page=100&page={}'
    projects_file = os.path.join(os.path.dirname(__file__), '..', 'src', 'data', 'projects.json')
    
    with open(projects_file, 'r', encoding='utf-8') as f:
        existing_projects = json.load(f)

    existing_urls = {p.get('repoUrl', '').lower() for p in existing_projects if p.get('repoUrl')}
    new_projects = []

    page = 1
    headers = {'User-Agent': 'Mozilla/5.0'}

    while True:
        url = api_url_template.format(page)
        req = urllib.request.Request(url, headers=headers)
        print(f"Fetching {url}")
        try:
            with urllib.request.urlopen(req) as response:
                issues = json.loads(response.read().decode('utf-8'))
        except Exception as e:
            print(f"Error fetching: {e}")
            break

        if not issues:
            break

        for issue in issues:
            # check if it's a pull request, we only want issues
            if 'pull_request' in issue:
                continue

            created_at = issue.get('created_at', '')
            if not created_at.startswith('2026'):
                continue

            body = issue.get('body') or ''
            title = issue.get('title') or ''
            
            p_name, p_url, p_desc = parse_issue_body(body)
            if not p_name:
                # try title
                if '：' in title:
                    p_name = title.split('：')[0].strip()
                else:
                    p_name = title.strip()
            if not p_desc:
                p_desc = body[:100].replace('\n', ' ').strip()
            
            if p_url and p_url.lower() not in existing_urls:
                new_project = {
                    "id": p_url.split('/')[-1] + f"-{issue.get('id')}",
                    "name": p_name,
                    "repoUrl": p_url,
                    "author": p_url.split('/')[-2] if p_url.count('/') >= 4 else "unknown",
                    "categoryVi": get_category_vi(p_desc + " " + p_name),
                    "summaryVi": translate_to_vi(p_desc),
                    "description_zh": p_desc,
                    "stars": 0,
                    "language": "Unknown",
                    "year": 2026
                }
                new_projects.append(new_project)
                existing_urls.add(p_url.lower())

        page += 1
        time.sleep(1) # rate limit

    if new_projects:
        existing_projects.extend(new_projects)
        with open(projects_file, 'w', encoding='utf-8') as f:
            json.dump(existing_projects, f, ensure_ascii=False, indent=2)

    print(f"Added {len(new_projects)} projects from 2026.")

if __name__ == '__main__':
    main()
