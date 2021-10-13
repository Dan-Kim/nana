class Remind:
  def __init__(self, id: int, requested_time: int, channel_id: int, user_id: int, message: str, guild_id: int):
    self.id = id
    self.requested_time = requested_time
    self.channel_id = channel_id
    self.user_id = user_id
    self.message = message
    self.guild_id = guild_id
