
from twisted.internet import reactor
from gerrit_bot import GerritBot

MINNIE="minnie.acer.com.tw"
MICKEY="mickey.acer.com.tw"
MINNIE_WHITE_LIST=["acer/dandelion", "acer/conga", "acer/timbero", "acer/bongo", "acer/bolero", "acer/asf", "acer/partyshot", "acer/icontrol", "acer/iot/openwrt"]
MICKEY_WHITE_LIST=["acer/apps/CloudPBX"]
HIPCHAT_AUTH_TOKEN="244a74652574b9bd0e43b98ecd1ff9"
HIPCHAT_ROOM_ID="324703"
REDMINE_API_KEY="003400126b0ef372e294c2916515dcde2cf5b2c3"

gb_minnie = GerritBot(MINNIE, MINNIE_WHITE_LIST, HIPCHAT_AUTH_TOKEN, HIPCHAT_ROOM_ID, REDMINE_API_KEY)
gb_mickey = GerritBot(MICKEY, MICKEY_WHITE_LIST, HIPCHAT_AUTH_TOKEN, HIPCHAT_ROOM_ID, REDMINE_API_KEY)
ctrl_minnie = reactor.spawnProcess(gb_minnie, "ssh", args= ["ssh", "-p", "29418", MINNIE, "gerrit", "stream-events"])
ctrl_mickey = reactor.spawnProcess(gb_mickey, "ssh", args= ["ssh", "-p", "29418", MICKEY, "gerrit", "stream-events"])
reactor.run()
