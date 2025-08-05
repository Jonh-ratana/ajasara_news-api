# from flask import Flask, jsonify
# import feedparser
# from datetime import datetime

# app = Flask(__name__)

# @app.route('/news')
# def home():
#     url = "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en"
#     feed = feedparser.parse(url)
#     articles = []
#     today = datetime.utcnow().date() 
    
#     for entry in feed.entries[:100]: 
#         if hasattr(entry, 'published_parsed'):
#             published_date = datetime(*entry.published_parsed[:6]).date()
#             if published_date == today:  
#                 articles.append({
#                     "title": entry.title,
#                     "link": entry.link,
#                     "published": entry.published
#                 })
#     return jsonify(articles)

# if __name__ == '__main__':
#     app.run(debug=True)

# from flask import Flask, jsonify
# import feedparser
# from datetime import datetime

# app = Flask(__name__)

# RSS_FEEDS = [
#     "https://feeds.bbci.co.uk/news/rss.xml",
#     "https://www.aljazeera.com/xml/rss/all.xml",
#     "https://feeds.reuters.com/reuters/topNews",
#     "https://www.bloomberg.com/feed/podcast/etf-report.xml",
#     "https://www.cnbc.com/id/100003114/device/rss/rss.html",
#     "https://www.imf.org/external/cms/sitemap/rss.aspx",
#     "https://www.worldbank.org/en/news/all/rss",
#     "https://oecd.github.io/news-rss/all.xml",
#     "https://www.economist.com/latest/rss.xml",
#     "https://thediplomat.com/feed/",
#     "https://warontherocks.com/feed/",
#     'https://www.bangkokpost.com/rss/breakingnews.xml'
# ]

# @app.route('/news')
# def get_news():
#     articles = []
#     today = datetime.utcnow().date()
    
#     for url in RSS_FEEDS:
#         feed = feedparser.parse(url)
#         for entry in feed.entries:
#             if hasattr(entry, 'published_parsed'):
#                 published_date = datetime(*entry.published_parsed[:6]).date()
#                 if published_date == today: 
#                     articles.append({
#                         "source": feed.feed.title if 'title' in feed.feed else url,
#                         "title": entry.title,
#                         "link": entry.link,
#                         "published": entry.published
#                     })
#     return jsonify(articles)

# if __name__ == '__main__':
#     app.run(debug=True)

# from flask import Flask, jsonify, render_template
# import feedparser
# import requests
# from bs4 import BeautifulSoup
# from datetime import datetime

# app = Flask(__name__)

# # RSS feeds to fetch
# RSS_FEEDS = [
#     "https://feeds.bbci.co.uk/news/rss.xml",
#     "https://www.aljazeera.com/xml/rss/all.xml",
#     "https://feeds.reuters.com/reuters/topNews",
#     "https://www.bloomberg.com/feed/podcast/etf-report.xml",
#     "https://www.cnbc.com/id/100003114/device/rss/rss.html",
#     "https://www.imf.org/external/cms/sitemap/rss.aspx",
#     "https://www.worldbank.org/en/news/all/rss",
#     "https://oecd.github.io/news-rss/all.xml",
#     "https://www.economist.com/latest/rss.xml",
#     "https://thediplomat.com/feed/",
#     "https://warontherocks.com/feed/",
#     "https://www.bangkokpost.com/rss/breakingnews.xml"
# ]

# def scrape_article(url):
#     """Fetch article text & images."""
#     try:
#         headers = {"User-Agent": "Mozilla/5.0"}
#         response = requests.get(url, headers=headers, timeout=10)
#         response.raise_for_status()
#         soup = BeautifulSoup(response.text, "html.parser")

#         # Extract paragraphs and join them
#         paragraphs = [p.get_text(strip=True) for p in soup.find_all("p") if p.get_text(strip=True)]
#         content = " ".join(paragraphs)

#         # Extract images
#         images = [img['src'] for img in soup.find_all("img") if img.get('src') and img['src'].startswith("http")]

#         return {"content": content, "images": images}
#     except Exception:
#         return {"content": "", "images": []}

# # Frontend page
# @app.route('/')
# def index():
#     return render_template('index.html')

# # API endpoint
# @app.route('/news')
# def get_news():
#     articles = []
#     today = datetime.utcnow().date()
    
#     for url in RSS_FEEDS:
#         feed = feedparser.parse(url)
#         for entry in feed.entries:
#             if hasattr(entry, 'published_parsed'):
#                 published_date = datetime(*entry.published_parsed[:6]).date()
#                 if published_date == today:
#                     article_data = scrape_article(entry.link)
#                     articles.append({
#                         "source": feed.feed.title if 'title' in feed.feed else url,
#                         "title": entry.title,
#                         "link": entry.link,
#                         "published": entry.published,
#                         "content": article_data["content"],
#                         "images": article_data["images"]
#                     })
#     return jsonify(articles)

# if __name__ == '__main__':
#     app.run(debug=True)


# from flask import Flask, jsonify
# import feedparser, requests
# from bs4 import BeautifulSoup
# from flask_cors import CORS
# from datetime import datetime
# from concurrent.futures import ThreadPoolExecutor

# app = Flask(__name__)
# CORS(app)

# RSS_FEEDS = [
#     "https://www.aljazeera.com/xml/rss/all.xml",
#     # Add more feeds if needed
# ]

# def clean_text(text):
#     bad_phrases = [
#         "Sign up for free newsletters",
#         "All Rights Reserved",
#         "Get this delivered to your inbox",
#         "Global Business and Financial News"
#     ]
#     for phrase in bad_phrases:
#         text = text.replace(phrase, "")
#     return " ".join(text.split())

# def scrape_article(url):
#     """Fetch full article content & high-quality images."""
#     try:
#         headers = {"User-Agent": "Mozilla/5.0"}
#         response = requests.get(url, headers=headers, timeout=8)
#         response.raise_for_status()
#         soup = BeautifulSoup(response.text, "html.parser")

#         # Extract article text
#         paragraphs = [p.get_text(strip=True) for p in soup.find_all("p") if p.get_text(strip=True)]
#         content = clean_text(" ".join(paragraphs))

#         # Extract images (Al Jazeera often uses <picture> and <figure>)
#         images = []

#         # 1) From <figure> tags (main content images)
#         for figure in soup.find_all("figure"):
#             img = figure.find("img")
#             if img and img.get("src") and img["src"].startswith("http"):
#                 if not img["src"].endswith(".svg") and "logo" not in img["src"].lower():
#                     images.append(img["src"])

#         # 2) From <picture> tags (high-res sources)
#         for picture in soup.find_all("picture"):
#             img = picture.find("img")
#             if img and img.get("src") and img["src"].startswith("http"):
#                 if not img["src"].endswith(".svg") and "logo" not in img["src"].lower():
#                     images.append(img["src"])

#         # 3) Fallback: All <img> tags (in case above misses some)
#         for img in soup.find_all("img"):
#             src = img.get('src')
#             if src and src.startswith("http") and not src.endswith(".svg") and "logo" not in src.lower():
#                 images.append(src)

#         images = list(dict.fromkeys(images))  # Remove duplicates

#         return {"content": content, "images": images}
#     except Exception:
#         return {"content": "", "images": []}

# def fetch_articles_today(url):
#     """Fetch ALL articles from today from an RSS feed."""
#     today = datetime.utcnow().date()
#     feed = feedparser.parse(url)
#     articles = []
#     for entry in feed.entries:
#         if hasattr(entry, 'published_parsed'):
#             published_date = datetime(*entry.published_parsed[:6]).date()
#             if published_date == today:
#                 article_data = scrape_article(entry.link)
#                 articles.append({
#                     "source": feed.feed.title if 'title' in feed.feed else url,
#                     "title": entry.title,
#                     "link": entry.link,
#                     "published": entry.published,
#                     "content": article_data["content"],
#                     "images": article_data["images"]
#                 })
#     return articles

# @app.route('/news')
# def get_news():
#     with ThreadPoolExecutor(max_workers=8) as executor:
#         results = list(executor.map(fetch_articles_today, RSS_FEEDS))
#     articles = [item for sublist in results for item in sublist]  # flatten
#     return jsonify(articles)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0' , port = 5000)



# from flask import Flask, jsonify
# import feedparser, requests
# from bs4 import BeautifulSoup
# from flask_cors import CORS
# from datetime import datetime
# from concurrent.futures import ThreadPoolExecutor
# from apscheduler.schedulers.background import BackgroundScheduler
# import json
# import os
# import time

# # === CONFIG ===
# TELEGRAM_CHAT_ID = "6752369289"
# TELEGRAM_BOT_TOKEN = "8175213282:AAHffAb4shqzL7eKs5I0yNyfIsOpg4Fdfnc"
# SENT_FILE = "sent_articles.json"

# app = Flask(__name__)
# CORS(app)

# RSS_FEEDS = [
#     "https://www.aljazeera.com/xml/rss/all.xml",
# ]

# # === Helper: Load & Save Sent Articles ===
# def load_sent_articles():
#     if os.path.exists(SENT_FILE):
#         with open(SENT_FILE, "r") as f:
#             return set(json.load(f))
#     return set()

# def save_sent_articles(sent_articles):
#     with open(SENT_FILE, "w") as f:
#         json.dump(list(sent_articles), f)

# sent_articles = load_sent_articles()

# # === Clean Text ===
# def clean_text(text):
#     bad_phrases = [
#         "Sign up for free newsletters",
#         "All Rights Reserved",
#         "Get this delivered to your inbox",
#         "Global Business and Financial News"
#     ]
#     for phrase in bad_phrases:
#         text = text.replace(phrase, "")
#     return " ".join(text.split())

# # === Scrape full article ===
# def scrape_article(url):
#     try:
#         headers = {"User-Agent": "Mozilla/5.0"}
#         response = requests.get(url, headers=headers, timeout=8)
#         response.raise_for_status()
#         soup = BeautifulSoup(response.text, "html.parser")

#         paragraphs = [p.get_text(strip=True) for p in soup.find_all("p") if p.get_text(strip=True)]
#         content = clean_text(" ".join(paragraphs))

#         images = []
#         for figure in soup.find_all("figure"):
#             img = figure.find("img")
#             if img and img.get("src") and img["src"].startswith("http"):
#                 if not img["src"].endswith(".svg") and "logo" not in img["src"].lower():
#                     images.append(img["src"])
#         for picture in soup.find_all("picture"):
#             img = picture.find("img")
#             if img and img.get("src") and img["src"].startswith("http"):
#                 if not img["src"].endswith(".svg") and "logo" not in img["src"].lower():
#                     images.append(img["src"])
#         for img in soup.find_all("img"):
#             src = img.get('src')
#             if src and src.startswith("http") and not src.endswith(".svg") and "logo" not in src.lower():
#                 images.append(src)

#         images = list(dict.fromkeys(images))
#         return {"content": content, "images": images}
#     except Exception:
#         return {"content": "", "images": []}

# # === Fetch today's articles ===
# def fetch_articles_today(url):
#     today = datetime.utcnow().date()
#     feed = feedparser.parse(url)
#     articles = []
#     for entry in feed.entries:
#         if hasattr(entry, 'published_parsed'):
#             published_date = datetime(*entry.published_parsed[:6]).date()
#             if published_date == today:
#                 article_data = scrape_article(entry.link)
#                 articles.append({
#                     "source": feed.feed.title if 'title' in feed.feed else url,
#                     "title": entry.title,
#                     "link": entry.link,
#                     "published": entry.published,
#                     "content": article_data["content"],
#                     "images": article_data["images"]
#                 })
#     return articles

# # === Telegram Sender ===
# def send_to_telegram(article):
#     text = (
#         f"{article['title']}\n"
#         f"Source: {article['source']}\n"
#         f"Published: {article['published']}\n"
#         f"{article['link']}"
#     )
#     url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
#     payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text, "disable_web_page_preview": False}
#     requests.post(url, json=payload)

# # === Task: Fetch and Send New Articles ===
# def scrape_and_send():
#     global sent_articles
#     with ThreadPoolExecutor(max_workers=8) as executor:
#         results = list(executor.map(fetch_articles_today, RSS_FEEDS))
#     articles = [item for sublist in results for item in sublist]

#     new_articles = [a for a in articles if a["link"] not in sent_articles]
#     for article in new_articles:
#         send_to_telegram(article)
#         sent_articles.add(article["link"])
#     if new_articles:
#         save_sent_articles(sent_articles)

# # === Flask Route ===
# @app.route('/news')
# def get_news():
#     with ThreadPoolExecutor(max_workers=8) as executor:
#         results = list(executor.map(fetch_articles_today, RSS_FEEDS))
#     articles = [item for sublist in results for item in sublist]
#     return jsonify(articles)

# # === Scheduler: run every 10 minutes ===
# scheduler = BackgroundScheduler()
# scheduler.add_job(scrape_and_send, 'interval', minutes=10)
# scheduler.start()

# # === Run immediately on startup ===
# time.sleep(3)
# scrape_and_send()

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)



from flask import Flask, jsonify
import feedparser, requests
from bs4 import BeautifulSoup
from flask_cors import CORS
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler
import json
import os
import time

# === CONFIG ===
TELEGRAM_CHAT_ID = "6752369289"  # Make sure this is correct, or negative if group chat
TELEGRAM_BOT_TOKEN = "8276152927:AAFqpLdt5z-9P9Q54DVC2OCr3umLIlopt8U"  # Make sure this is correct
SENT_FILE = "sent_articles.json"
DEBUG_MODE = True           # Verbose logging
IGNORE_SENT = True          # Send articles even if sent before (for testing)
IGNORE_DATE = True          # Ignore date filtering (send all articles)

app = Flask(__name__)
CORS(app)

RSS_FEEDS = [
    "https://www.aljazeera.com/xml/rss/all.xml",
]

# === Helper: Load & Save Sent Articles ===
def load_sent_articles():
    if os.path.exists(SENT_FILE):
        with open(SENT_FILE, "r") as f:
            return set(json.load(f))
    return set()

def save_sent_articles(sent_articles):
    with open(SENT_FILE, "w") as f:
        json.dump(list(sent_articles), f)

sent_articles = load_sent_articles()

# === Clean Text ===
def clean_text(text):
    bad_phrases = [
        "Sign up for free newsletters",
        "All Rights Reserved",
        "Get this delivered to your inbox",
        "Global Business and Financial News"
    ]
    for phrase in bad_phrases:
        text = text.replace(phrase, "")
    return " ".join(text.split())

# === Scrape full article ===
def scrape_article(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=8)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        paragraphs = [p.get_text(strip=True) for p in soup.find_all("p") if p.get_text(strip=True)]
        content = clean_text(" ".join(paragraphs))

        images = []
        for figure in soup.find_all("figure"):
            img = figure.find("img")
            if img and img.get("src") and img["src"].startswith("http"):
                if not img["src"].endswith(".svg") and "logo" not in img["src"].lower():
                    images.append(img["src"])
        for picture in soup.find_all("picture"):
            img = picture.find("img")
            if img and img.get("src") and img["src"].startswith("http"):
                if not img["src"].endswith(".svg") and "logo" not in img["src"].lower():
                    images.append(img["src"])
        for img in soup.find_all("img"):
            src = img.get('src')
            if src and src.startswith("http") and not src.endswith(".svg") and "logo" not in src.lower():
                images.append(src)

        images = list(dict.fromkeys(images))
        return {"content": content, "images": images}
    except Exception as e:
        if DEBUG_MODE:
            print(f"[ERROR] Failed scraping {url}: {e}")
        return {"content": "", "images": []}

# === Fetch articles (today or all if IGNORE_DATE) ===
def fetch_articles(url):
    today = datetime.now(timezone.utc).date()
    feed = feedparser.parse(url)
    articles = []
    if DEBUG_MODE:
        print(f"[INFO] Fetching feed: {url} (entries: {len(feed.entries)})")

    for entry in feed.entries:
        try:
            published_date = None
            if hasattr(entry, 'published_parsed'):
                published_date = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc).date()

            if IGNORE_DATE or (published_date and published_date == today):
                article_data = scrape_article(entry.link)
                articles.append({
                    "source": feed.feed.title if 'title' in feed.feed else url,
                    "title": entry.title,
                    "link": entry.link,
                    "published": entry.published if hasattr(entry, 'published') else "",
                    "content": article_data["content"],
                    "images": article_data["images"]
                })
        except Exception as e:
            if DEBUG_MODE:
                print(f"[ERROR] Failed processing entry: {e}")
    return articles

# === Telegram Sender ===
def send_to_telegram(article):
    text = (
        f"{article['title']}\n"
        f"Source: {article['source']}\n"
        f"Published: {article['published']}\n"
        f"{article['link']}"
    )
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text, "disable_web_page_preview": False}
    response = requests.post(url, json=payload)
    if DEBUG_MODE:
        print(f"[TELEGRAM] Status: {response.status_code} | Response: {response.text}")

# === Daily Task: Fetch and Send New Articles ===
def daily_task():
    global sent_articles
    with ThreadPoolExecutor(max_workers=8) as executor:
        results = list(executor.map(fetch_articles, RSS_FEEDS))
    articles = [item for sublist in results for item in sublist]

    if DEBUG_MODE:
        print(f"[INFO] Found {len(articles)} articles (raw). Already sent: {len(sent_articles)}")
        print(f"[DEBUG] Already sent links: {sent_articles}")
        print(f"[DEBUG] Articles found links: {[a['link'] for a in articles]}")

    # Filter out already sent articles if IGNORE_SENT is False
    new_articles = articles if IGNORE_SENT else [a for a in articles if a["link"] not in sent_articles]

    if DEBUG_MODE:
        print(f"[INFO] New articles to send: {len(new_articles)}")
        print(f"[DEBUG] New article links: {[a['link'] for a in new_articles]}")

    for article in new_articles:
        send_to_telegram(article)
        sent_articles.add(article["link"])

    if new_articles and not IGNORE_SENT:
        save_sent_articles(sent_articles)
        if DEBUG_MODE:
            print("[INFO] Sent articles updated & saved.")

# === Flask Route ===
@app.route('/news')
def get_news():
    with ThreadPoolExecutor(max_workers=8) as executor:
        results = list(executor.map(fetch_articles, RSS_FEEDS))
    articles = [item for sublist in results for item in sublist]
    return jsonify(articles)

# === Scheduler ===
scheduler = BackgroundScheduler()
scheduler.add_job(daily_task, 'cron', hour=8, minute=0)  # Auto daily at 8:00 UTC
scheduler.start()

# === Run Once on Startup ===
time.sleep(3)
daily_task()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
