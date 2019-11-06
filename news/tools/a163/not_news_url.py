def not_news_url(url):
    if "photoview" in url or "://v." in url or 'nba.' in url or '2018.163' in url or 'match' in url:
        return True

