import random

from services.db_service import select_banners


def get_random_banner():
  rows = select_banners()
  if not rows:
    return []
  row = random.choice(rows)
  return {
    'discord_id': row[0],
    'times_picked': row[1]
  }


def get_banner(discord_id):
  rows = select_banners(discord_id=discord_id)
  if not rows:
    return []
  return [{
    'discord_id': row[0],
    'times_picked': row[1]
  } for row in rows]
