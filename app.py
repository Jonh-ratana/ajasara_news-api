from flask import Flask, jsonify
import feedparser, requests, json, os
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler
from flask_cors import CORS

# === CONFIG ===
TELEGRAM_CHAT_ID = "6752369289"
TELEGRAM_BOT_TOKEN = "8276152927:AAFqpLdt5z-9P9Q54DVC2OCr3umLIlopt8U"
SENT_FILE = "sent_articles.json"
DEBUG_MODE = True
CHECK_INTERVAL = 60   # ពិនិត្យរៀងរាល់ 60 វិនាទី
IGNORE_SENT = False   # ផ្ញើតែអត្ថបទថ្មី
IGNORE_DATE = True    # បើចង់ចាប់តែថ្ងៃនេះ → False

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
    for phrase in ["Sign up for free newsletters","All Rights Reserved","Get this delivered to your inbox","Global Business and Financial News"]:
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
        return {"content": content}
    except Exception as e:
        if DEBUG_MODE: print(f"[ERROR] Failed scraping {url}: {e}")
        return {"content": ""}

# === Fetch Articles ===
def fetch_articles(url):
    today = datetime.now(timezone.utc).date()
    feed = feedparser.parse(url)
    articles = []
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
                    "content": article_data["content"]
                })
        except Exception as e:
            if DEBUG_MODE: print(f"[ERROR] Failed processing entry: {e}")
    return articles

# === Telegram Sender ===
def send_to_telegram(article):
    text = f"{article['title']}\nSource: {article['source']}\nPublished: {article['published']}\n{article['link']}"
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
    r = requests.post(url, json=payload)
    if DEBUG_MODE: print(f"[TELEGRAM] {r.status_code} - {r.text}")

# === Main Job ===
def check_and_send():
    global sent_articles
    with ThreadPoolExecutor(max_workers=8) as executor:
        results = list(executor.map(fetch_articles, RSS_FEEDS))
    articles = [item for sublist in results for item in sublist]
    new_articles = [a for a in articles if a["link"] not in sent_articles]

    if DEBUG_MODE:
        print(f"[INFO] Found {len(articles)} articles. New: {len(new_articles)}")

    for article in new_articles:
        send_to_telegram(article)
        sent_articles.add(article["link"])

    if new_articles:
        save_sent_articles(sent_articles)

# === Schedule ===
scheduler = BackgroundScheduler()
scheduler.add_job(check_and_send, 'interval', seconds=CHECK_INTERVAL)
scheduler.start()

# Run first
check_and_send()

# === API Route ===
@app.route('/news')
def get_news():
    with ThreadPoolExecutor(max_workers=8) as executor:
        results = list(executor.map(fetch_articles, RSS_FEEDS))
    articles = [item for sublist in results for item in sublist]
    return jsonify(articles)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
