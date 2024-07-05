import feedparser

def arxiv_research():
    url = 'https://rss.arxiv.org/rss/cs'

    feed = feedparser.parse(url)

    print(feed)

if __name__ == "__main__":
    arxiv_research()