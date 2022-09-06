# matrix-reaction-signature-bot
Admin bot, which add signature reaction to users messages in matrix.
Bot allow set user signature by admin room (signature will show as reaction text) for each message of target user. Also admin can +1 to count rule interruption of room. This count will also show as reaction of user. Admin can set description for each rule interruption of target user. Clear activ rule interruption, show description in room, statistic.
Also each user can set/clear/show own description. Alsow description of user can see any user in room.

Need python modules for install:

asyncio
nio
configparser
logging
sys
json
os
traceback
datetime
psycopg2
psycopg2.extras
time
re
gettext

Install steps:
1. clone code: `git clone https://github.com/progserega/matrix-reaction-signature-bot.git`
2. install need python modules
3. create bot postgres user (if need), for example: 
4. create postgres database with owner of bot postgres user (for example: `create database reaction_bot owner=reaction_bot ;`)
5. enter in directory with code: `cd matrix-reaction-signature-bot`
6. create tables by exec cmd: `psql reaction_bot < sql/create_tables.sql`
7. grant access to bot user by exec cmd: `psql reaction_bot < sql/grant_db_priviledges_to_reaction_bot.sql`
8. create config: `cp config.ini.example config.ini`
9. create matrix user and add it params to bot config
9. fix need options in config (see comments in config)
10. start bot as: `python3 bot.py config.ini` or use systemd unit-file from source (file: matrix-reaction-signature-bot.service)
11. invite bot matrix user to room (check, that you allow for this in [invites] section in config.ini)
12. now you can use this bot in your room. 
13. All feature allow only for room moderators by default (see [powers] sections in config.ini)
