import feedparser

def arxiv_research(data_endpoint, requested_announce_type):
    url = f'https://rss.arxiv.org/rss/{data_endpoint}'

    feed = feedparser.parse(url)
    entries = feed.get('entries')

    if requested_announce_type == 'all':
        return entries
    else:
        processed_entries = []

        for entry in entries:
            announce_type = entry.get('arxiv_announce_type')

            if (announce_type == requested_announce_type):
                processed_entries.append(entry)

        return processed_entries