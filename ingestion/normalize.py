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
