import random

LEGENDS = [
  ['Ash', 'アッシュ', 'https://static.wikia.nocookie.net/apexlegends_gamepedia_en/images/7/70/Ash.jpg/revision/latest'],
  ['Alter', 'アルター', 'https://static.wikia.nocookie.net/apexlegends_gamepedia_en/images/f/f8/Alter.jpg/revision/latest'],
  ['Ballistic', 'バリスティック', 'https://static.wikia.nocookie.net/apexlegends_gamepedia_en/images/4/4a/Ballistic.jpg/revision/latest'],
  ['Bangalore', 'バンガロール', 'https://static.wikia.nocookie.net/apexlegends_gamepedia_en/images/f/f7/Bangalore.jpg/revision/latest'],
  ['Bloodhound', 'ブラッドハウンド', 'https://static.wikia.nocookie.net/apexlegends_gamepedia_en/images/0/05/Bloodhound.jpg/revision/latest'],
  ['Catalyst', 'カタリスト', 'https://static.wikia.nocookie.net/apexlegends_gamepedia_en/images/9/9d/Catalyst.jpg/revision/latest'],
  ['Caustic', 'コースティック', 'https://static.wikia.nocookie.net/apexlegends_gamepedia_en/images/e/e7/Caustic.jpg/revision/latest'],
  ['Conduit', 'コンジット', 'https://static.wikia.nocookie.net/apexlegends_gamepedia_en/images/8/8f/Conduit.jpg/revision/latest'],
  ['Crypto', 'クリプト', 'https://static.wikia.nocookie.net/apexlegends_gamepedia_en/images/1/1f/Crypto.jpg/revision/latest'],
  ['Fuse', 'ヒューズ', 'https://static.wikia.nocookie.net/apexlegends_gamepedia_en/images/2/25/Fuse.jpg/revision/latest'],
  ['Gibraltar', ' ジブラルタル', 'https://static.wikia.nocookie.net/apexlegends_gamepedia_en/images/8/8b/Gibraltar.jpg/revision/latest'],
  ['Horizon', 'ホライゾン', 'https://static.wikia.nocookie.net/apexlegends_gamepedia_en/images/7/7d/Horizon.jpg/revision/latest'],
  ['Lifeline', 'ライフライン', 'https://static.wikia.nocookie.net/apexlegends_gamepedia_en/images/4/4f/Lifeline.jpg/revision/latest'],
  ['Loba', 'ローバ', 'https://static.wikia.nocookie.net/apexlegends_gamepedia_en/images/7/7d/Loba.jpg/revision/latest'],
  ['Mad Maggie', 'マッドマギー', 'https://static.wikia.nocookie.net/apexlegends_gamepedia_en/images/5/5f/Mad_Maggie.jpg/revision/latest'],
  ['Mirage', 'ミラージュ', 'https://static.wikia.nocookie.net/apexlegends_gamepedia_en/images/a/a6/Mirage.jpg/revision/latest'],
  ['Newcastle', 'ニューキャッスル', 'https://static.wikia.nocookie.net/apexlegends_gamepedia_en/images/b/b9/Newcastle.jpg/revision/latest'],
  ['Octane', 'オクタン', 'https://static.wikia.nocookie.net/apexlegends_gamepedia_en/images/d/d6/Octane.jpg/revision/latest'],
  ['Pathfinder', 'パスファインダー', 'https://static.wikia.nocookie.net/apexlegends_gamepedia_en/images/5/53/Pathfinder.jpg/revision/latest'],
  ['Rampart', 'ランパート', 'https://static.wikia.nocookie.net/apexlegends_gamepedia_en/images/5/51/Rampart.jpg/revision/latest'],
  ['Revenant', 'レヴナント', 'https://static.wikia.nocookie.net/apexlegends_gamepedia_en/images/5/59/Revenant.jpg/revision/latest'],
  ['Seer', 'シア', 'https://static.wikia.nocookie.net/apexlegends_gamepedia_en/images/4/4b/Seer.jpg/revision/latest'],
  ['Valkyrie', 'ヴァルキリー', 'https://static.wikia.nocookie.net/apexlegends_gamepedia_en/images/5/5f/Valkyrie.jpg/revision/latest'],
  ['Vantage', 'ヴァンテージ', 'https://static.wikia.nocookie.net/apexlegends_gamepedia_en/images/5/5a/Vantage.jpg/revision/latest'],
  ['Wattson', 'ワットソン', 'https://static.wikia.nocookie.net/apexlegends_gamepedia_en/images/8/82/Wattson.jpg/revision/latest'],
  ['Wraith', 'レイス', 'https://static.wikia.nocookie.net/apexlegends_gamepedia_en/images/a/a4/Wraith.jpg/revision/latest']
]

def get_random_legend():
  return random.choice(LEGENDS)
