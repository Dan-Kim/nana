import sqlite3

NANA_DB = '../nana-db/nana.db'


def select_banners(discord_id='%%'):
  conn = sqlite3.connect(NANA_DB)
  c = conn.cursor()
  c.execute('SELECT * FROM banner WHERE discord_id LIKE ?', (discord_id,))
  rows = c.fetchall()
  conn.close()
  return rows


def increment_banner_count(discord_id=''):
  conn = sqlite3.connect(NANA_DB)
  c = conn.cursor()
  c.execute('SELECT * FROM banner WHERE discord_id = ?', (discord_id,))
  selected = c.fetchone()
  c.execute('REPLACE INTO banner(discord_id, times_picked) VALUES (?,?)', (selected[0], selected[1] + 1))
  conn.commit()
  conn.close()

def select_mal_users():
  conn = sqlite3.connect(NANA_DB)
  c = conn.cursor()
  c.execute('SELECT * FROM myanimelist_profiles_for_rss')
  rows = c.fetchall()
  conn.close()
  return rows
