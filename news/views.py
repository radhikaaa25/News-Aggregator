
import requests
from django.shortcuts import render, redirect
from bs4 import BeautifulSoup as BSoup
from news.models import Headline

# Create your views here.

import feedparser
from news.models import Headline


def scrape(request, name):
    Headline.objects.all().delete()

    rss_urls = {
    "latest": "http://feeds.bbci.co.uk/news/world/rss.xml",
    "sports": "http://feeds.bbci.co.uk/sport/rss.xml",
    "politics": "https://www.theguardian.com/world/rss",
    "tech": "https://hnrss.org/frontpage",
    "entertainment": "http://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml",
}
    print("📰 Scraping news for:", name)  # 👀 LOG IT

    feed_url = rss_urls.get(name)
    if not feed_url:
        return redirect("/")

    feed = feedparser.parse(feed_url)

    for entry in feed.entries:
        title = entry.title
        link = entry.link
        image = None
        if "media_content" in entry:
            image = entry.media_content[0].get("url")
        elif "media_thumbnail" in entry:
            image = entry.media_thumbnail[0].get("url")
        elif "summary" in entry:
            soup = BeautifulSoup(entry.summary, "html.parser")
            img_tag = soup.find("img")
            if img_tag:
                image = img_tag.get("src")

        print("Image URL:", image)  # 👀 LOG IT

        if not image:
            image = "https://via.placeholder.com/300x200.png?text=No+Image"

        Headline.objects.create(title=title, url=link, image=image)

    return redirect("/")


def news_list(request):
    print("🎯 Home view hit")  # just to see if it prints in terminal
    headlines = Headline.objects.all()[::-1]
    context = {
        "object_list": headlines,
    }
    return render(request, "news/home.html", context)

