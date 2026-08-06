import feedparser
import json
import os
import socket

# Set a global timeout for network requests
socket.setdefaulttimeout(10)

output_path = "../database/articles.json"

# Load existing articles if file exists
if os.path.exists(output_path):
    with open(output_path, "r", encoding="utf-8") as infile:
        articles = json.load(infile)
else:
    articles = []

# Helper: normalize URL
def normalize_url(url: str) -> str:
    return url.strip().lower().split("?")[0]

# Build a set of existing URLs for fast duplicate detection
existing_urls = {normalize_url(a["link"]) for a in articles if "link" in a}

with open("../database/rss_sources.json", "r", encoding="utf-8") as file:
    sources = json.load(file)

# Loop through categories
for category, feeds in sources.items():
    print(f"\nCategory: {category}")
    for source in feeds:
        print(f"Source: {source['name']} ({source['category']})")
        url = source["url"]

        try:
            feed = feedparser.parse(url)
            if not feed.entries:
                print("   ⚠️ No articles found or invalid RSS format.")
                continue

            for article in feed.entries[:5]:
                link = normalize_url(article.get("link", ""))
                if not link or link in existing_urls:
                    print(f"   ⏩ Skipping duplicate: {link}")
                    continue

                article_dict = {
                    "title": article.get("title", ""),
                    "link": link,
                    "published": article.get("published", ""),
                    "summary": article.get("summary", ""),
                    "source": source["name"],
                    "category": category,
                    "keywords": [],
                    "entities": [],
                    "sentiment": "",
                    "importance": 0,
                    "processed": False
                }

                articles.append(article_dict)
                existing_urls.add(link)

        except Exception as e:
            print(f"   ❌ Error fetching {url}: {e}")

# Save results
with open(output_path, "w", encoding="utf-8") as outfile:
    json.dump(articles, outfile, indent=2, ensure_ascii=False)

print(f"\nSaved {len(articles)} articles to {output_path}")
