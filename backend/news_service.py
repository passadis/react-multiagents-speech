import json
import urllib.request

def fetch_greek_news(api_key, max_articles=5, category='nation'):
    url = f"https://gnews.io/api/v4/top-headlines?country=gr&lang=el&category={category}&max={max_articles}&token={api_key}"

    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode("utf-8"))
            articles = data.get("articles", [])
            headlines = [article["title"] for article in articles]
            return " ".join(headlines)
    except Exception as e:
        print(f"Error fetching news: {e}")
        return "Error fetching news."

