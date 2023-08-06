Set the following environment variables to run:
* CLIENT_ID
* CLIENT_SECRET
* DISCORD_WEBHOOK
* SUBREDDIT

Optional environment variable:
* TITLE_FILTER - filters for titles that contain the phrase in a case-insensitive fashion


The following entrypoints are available
* monitor_comments - looks for new comments and posts them to the discord webhook
* monitor_submissions - looks for new submissions and posts them to the discord webhook

### Example Running

```sh
cat > config.ini <<EOF
[monitor]
type=comments
client_id=CLIENT_ID
client_secret=CLIENT_SECRET
subreddit=worldnews
discord_webhook='https://discordapp.com/api/webhooks/{ID}/{SECRET_TOKEN}'
EOF

REDDITMONITOR_CONFIG=config.ini redditmonitor
```

### Running Spoiler Checker

```sh
cat > config.ini <<EOF
[monitor]
type=spoilers
client_id=CLIENT_ID
client_secret=CLIENT_SECRET
subreddit=worldnews
discord_webhook=https://discordapp.com/api/webhooks/{ID}/{SECRET_TOKEN}
spoiler_text='laconia,laconian' \
EOF

REDDITMONITOR_CONFIG=config.ini redditmonitor
```