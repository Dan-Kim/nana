import sqlite3
from typing import List

from models.remind import Remind
from models.banner import Banner

NANA_DB = '../nana-db/nana.db'


def select_reminds(requested_time, user_id='%%') -> List[Remind]:
  conn = sqlite3.connect(NANA_DB)
  c = conn.cursor()
  c.execute('SELECT * FROM remind WHERE requested_time=? AND user_id LIKE ?', (requested_time, user_id))
  reminds = [
    Remind(
      id=row[0],
      requested_time=row[1],
      channel_id=row[2],
      user_id=row[3],
      message=row[4],
      guild_id=row[5]
    ) for row in c.fetchall()
  ]
  conn.close()
  return reminds


def show_reminds(user_id='%%', guild_id='%%') -> List[Remind]:
  conn = sqlite3.connect(NANA_DB)
  c = conn.cursor()
  c.execute('SELECT * FROM remind WHERE user_id LIKE ? AND guild_id LIKE ? ORDER BY requested_time ASC',
            (user_id, guild_id))
  reminds = [
    Remind(
      id=row[0],
      requested_time=row[1],
      channel_id=row[2],
      user_id=row[3],
      message=row[4],
      guild_id=row[5]
    ) for row in c.fetchall()
  ]
  conn.close()
  return reminds


def count_reminds(user_id='%%', guild_id='%%'):
  conn = sqlite3.connect(NANA_DB)
  c = conn.cursor()
  c.execute('SELECT COUNT(*) FROM remind WHERE user_id LIKE ? AND guild_id LIKE ?', (user_id, guild_id))
  (count,) = c.fetchone()
  conn.close()
  return count


def insert_remind(requested_time, channel_id, user_id, message, guild_id):
  conn = sqlite3.connect(NANA_DB)
  c = conn.cursor()
  c.execute('INSERT INTO remind(requested_time, channel_id, user_id, message, guild_id) VALUES (?,?,?,?,?)',
            (requested_time, channel_id, user_id, message, guild_id))
  conn.commit()
  conn.close()


def delete_remind(requested_time, channel_id, user_id, message, guild_id):
  conn = sqlite3.connect(NANA_DB)
  c = conn.cursor()
  c.execute(
    'DELETE FROM remind WHERE requested_time = ? AND channel_id = ? AND user_id = ? AND message = ? AND guild_id = ?',
    (requested_time, channel_id, user_id, message, guild_id))
  conn.commit()
  conn.close()


def delete_old_reminds(requested_time=0):
  conn = sqlite3.connect(NANA_DB)
  c = conn.cursor()
  c.execute('DELETE FROM remind WHERE requested_time <= ?', (requested_time,))
  conn.commit()
  conn.close()


def select_banners(discord_id='%%'):
  conn = sqlite3.connect(NANA_DB)
  c = conn.cursor()
  c.execute('SELECT * FROM banner WHERE discord_id LIKE ?', (discord_id,))
  banners = [
    Banner(
      discord_id=row[0], 
      times_picked=row[1]
    ) for row in c.fetchall()
  ]
  conn.close()
  return banners


def increment_banner_count(discord_id=''):
  conn = sqlite3.connect(NANA_DB)
  c = conn.cursor()
  c.execute('SELECT * FROM banner WHERE discord_id = ?', (discord_id,))
  selected = c.fetchone()
  c.execute('REPLACE INTO banner(discord_id, times_picked) VALUES (?,?)', (selected[0], selected[1] + 1))
  conn.commit()
  conn.close()
