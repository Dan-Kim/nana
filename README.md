# Nana Utility Bot

## Code Structure

### Cogs
Cogs contain logic that interacts directly with Discord. This includes 
commands and cron-like methods that periodically update channels and
messages or send messages. Cogs are organized by function.

`APScheduler`'s `AsyncIOScheduler` is used to set up the aforementioned
cron-like methods.

The `Miscellaneous` cog should contain a new `help` command because the
default is ugly.

### Models
Models contain a native python representation of data stored in databases.

### Serializers
Serializers should be deleted and are bad.

### Services
Services contain all logic that does not directly interact with Discord.
This includes calls to third party APIs, complicated `Discord.embed`
creation, text manipulation, database queries, etc. Services should be
split more or less by function and should be self-contained. 

## Packages

```commandline
python -m pip install apscheduler discord.py requests sqlite3 pymongo
```

## TODO

1. Refactor `banner_serializer` into a `Banner` model.
2. Refactor file related getting and setting logic to `file_service.py`.
3. Refactor `jisho_service` to use a request wrapper model.
4. Use embeds for `jisho` command.
5. Error output in Discord channel.
6. Linux restart script with instructions. 
