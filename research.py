import feedparser

def arxiv_research(data_endpoint, requested_announce_type, requested_keywords):
    url = f'https://rss.arxiv.org/rss/{data_endpoint}'

    feed = feedparser.parse(url)
    entries = feed.get('entries')

    filtered_entries = []

    for entry in entries:
        announce_type = entry.get('arxiv_announce_type')
        if (requested_announce_type == 'all') or (requested_announce_type == announce_type):
            if (len(requested_keywords) != 0):
                title = entry.get('title')

                summary = entry.get('summary')
                abstract_index = summary.index('Abstract')
                abstract = summary[abstract_index:]

                if any((keyword in title) or (keyword in abstract) for keyword in requested_keywords):
                    filtered_entries.append(entry)
            else:
                filtered_entries.append(entry)
                

    return filtered_entries