import requests

RSS_FEED_BASE_URL = 'https://myanimelist.net/rss.php'
RSS_FEED_TYPES = {'Anime': 'rw', 'Anime by Episode': 'rwe', 'Manga': 'rm', 'Manga by Chapter': 'rrm'}


def get_rss_feeds_for_user(user):
  try:
    output = {}
    for media_type, rss_feed_type in RSS_FEED_TYPES.items():
      url = '{0}?type={1}&u={2}'.format(RSS_FEED_BASE_URL, rss_feed_type, user)
      r = requests.get(url)
      r.raise_for_status()
      output[media_type] = r.text
    return output
  except requests.exceptions.HTTPError as err:
    return err
