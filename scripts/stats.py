import json
from collections import Counter

with open('src/data/projects.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total: {len(data)}")
stars = [p['stars'] for p in data]
print(f"Min stars: {min(stars)}")
print(f"Max stars: {max(stars)}")

categories = [p['categoryVi'] for p in data]
counts = Counter(categories)
print("Categories:")
for k, v in counts.items():
    print(f"  {k}: {v}")
