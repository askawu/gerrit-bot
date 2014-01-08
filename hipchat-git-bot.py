
from twisted.internet import reactor
from twisted.internet import defer
from twisted.internet import protocol
import simplejson as json
import os
import subprocess

GERRIT=""
PROJECT_WHITE_LIST=[]
HIPCHAT_CLI_SCRIPT=""
HIPCHAT_AUTH_TOKEN=""
HIPCHAT_ROOM_ID=""
BOT_NAME="GIT"

class HookProtocol(protocol.ProcessProtocol):
    def outReceived(self, data):
        self.data = data
        lines = self.data.split("\n")
        self.data = lines.pop(-1)
        for line in lines:
            print "gerrit: %s" % line
            self.lineReceived(line)
        
    def lineReceived(self, line):
        try:
            event = json.loads(line.decode('utf-8'))
        except ValueError:
            defer.succeed(None)
       
        if not(type(event) == type({}) and "type" in event):
            log.msg("no type in event %s" % (line,))
            return defer.succeed(None)

        if event["type"] == "change-merged":
            skip = True
            for p in PROJECT_WHITE_LIST:
                if event["change"]["project"] == p:
                    skip = False
                    break

            if not skip:
                msg = "This patch has been merged:\n\n"
                msg += "project: %s\n" % (event["change"]["project"])
                msg += "subject: %s\n" % (event["change"]["subject"])
                msg += "gerrit:  <a href=\"%s\">link</a>\n" % (event["change"]["url"])
                msg += "gitweb:  <a href=\"http://%s/gitweb/?p=%s.git;a=commitdiff;h=%s\">link</a>\n" % (GERRIT, event["change"]["project"], event["patchSet"]["revision"])
                p1 = subprocess.Popen(["echo", msg], stdout=subprocess.PIPE)
                p2 = subprocess.Popen([HIPCHAT_CLI_SCRIPT, "-c", "green", "-t", HIPCHAT_AUTH_TOKEN, "-r", HIPCHAT_ROOM_ID, "-f", BOT_NAME], stdin=p1.stdout, stdout=subprocess.PIPE)
                p2.communicate() 

hp = HookProtocol()
ctrl = reactor.spawnProcess(hp, "ssh", args= ["ssh", "-p", "29418", GERRIT, "gerrit", "stream-events"])
reactor.run()
