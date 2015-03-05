
from twisted.internet import defer
from twisted.internet import protocol
import simplejson as json
import os
import re
import subprocess

class GerritBot(protocol.ProcessProtocol):

    def __init__(self, gerrit, whitelist, token, room, key):
        self.gerrit = gerrit
        self.hipchat_white_list = whitelist
        self.hipchat_auth_token = token
        self.hipchat_room_id = room
        self.hipchat_cli = "./hipchat_room_message"
        self.redmine_api_key = key
        self.redmine_cli = "./redmine_update_issue"
        self.bot_name = "GIT"

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
            return defer.succeed(None)

        if not(type(event) == type({}) and "type" in event):
            log.msg("no type in event %s" % (line,))
            return defer.succeed(None)

        if event["type"] == "change-merged":
            skip = True
            for p in self.hipchat_white_list:
                if event["change"]["project"] == p:
                    skip = False
                    break

            if not skip:
                msg = "This patch has been merged:\n\n"
                msg += "project: %s\n" % (event["change"]["project"])
                msg += "subject: %s\n" % (event["change"]["subject"])
                msg += "gerrit:  <a href=\"%s\">link</a>\n" % (event["change"]["url"])
                msg += "gitweb:  <a href=\"http://%s/gitweb/?p=%s.git;a=commitdiff;h=%s\">link</a>\n" % (self.gerrit, event["change"]["project"], event["patchSet"]["revision"])
                cmd1 = ["echo", msg]
                cmd2 = [self.hipchat_cli,
                        "-c",
                        "green",
                        "-t",
                        self.hipchat_auth_token,
                        "-r",
                        self.hipchat_room_id,
                        "-f",
                        self.bot_name]
                p1 = subprocess.Popen(cmd1, stdout=subprocess.PIPE)
                p2 = subprocess.Popen(cmd2, stdin=p1.stdout, stdout=subprocess.PIPE)
                p2.communicate()
        elif event["type"] == "patchset-created":
            pattern = re.compile(".*\[t(\d+)\].*")
            match = pattern.match(event["change"]["subject"])
            if match:
                cmd = [self.redmine_cli,
                       event["change"]["owner"]["name"],
                       event["change"]["project"],
                       event["change"]["url"],
                       match.group(1),
                       self.redmine_api_key]
                ret = subprocess.call(cmd)
