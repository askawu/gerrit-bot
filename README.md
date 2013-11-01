hipchat-git-bot
===============

You can add a git bot for you hipchat room based on gerrit stream events.

## Installation

This script need the help of hipchat/hipchat-cli

Clone [hipchat-cli](https://github.com/hipchat/hipchat-cli)

And modify hipchat-git-bot.py for your own setting

```sh

GERRIT="your_gerrit_server"
PROJECT_WHITE_LIST=["your_project"]
HIPCHAT_CLI_SCRIPT="/path/to/hipchat_room_message"
HIPCHAT_AUTH_TOKEN="hipchat_auth_token"
HIPCHAT_ROOM_ID="hipchat_room_id"
BOT_NAME="bot_name"
```
aska.wu@acer.com
