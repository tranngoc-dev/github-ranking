import json
import sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/projects.json', encoding='utf-8') as f:
    projects = json.load(f)

spots = ['build-your-own-x', 'awesome', 'public-apis', 'freeCodeCamp', 'anthropics/skills']
for p in projects:
    for s in spots:
        if s in p.get('repoUrl', ''):
            print(f"{s}: {p.get('summaryVi', '')}")
