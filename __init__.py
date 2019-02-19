import os
import time
from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_file_handler, intent_handler
from mycroft.util.log import LOG

__author__ = 'colla69'


def play_player():
    os.system("cmus-remote -p")


def pause_player():
    os.system("cmus-remote -u")


def search_player(text):
    os.system('cmus-remote -C "/' + text+'"')
    os.system('cmus-remote -C "win-activate"')
    # os.system("cmus-remote -n")


class CmusPlayerSkill(MycroftSkill):

    def __init__(self):
        super(CmusPlayerSkill, self).__init__(name="TemplateSkill")
        # Initialize working variables used within the skill.
        self.start_player()
        self.running = True

    @intent_file_handler('play.music.intent')
    def handle_play_music_ntent(self, message):
        if not self.running:
            self.start_player()
        play_player()

    @intent_file_handler('pause.music.intent')
    def handle_pause_music_intent(self, message):
        pause_player()

    @intent_handler(IntentBuilder("search.music.intent").require("search.music").require("SongToPlay").build())
    def handle_search_music_intent(self, message):
        songtoplay = message.data.get("SongToPlay")
        LOG.info(songtoplay)
        if not self.running:
            self.start_player()
        search_player(songtoplay)

    def start_player(self):
        self.running = True
        os.system("screen -d -m -S cmus cmus")
        # os.system("cmus  </dev/null>/dev/null 2>&1 &")
        # no stdout > cmus idles using 15 to 20 % CPU
        time.sleep(1)


    def stop_player(self):
        self.running = False
        os.system("cmus-remote -C quit")
        # os.system("killall cmus")

    def converse(self, utterances, lang="en-us"):
        # contains all triggerwords for second layer Intents
        LOG.info(self.dictation_words)
        ####
        return False

    def stop(self):
        if self.running:
            self.stop_player()


def create_skill():
    return CmusPlayerSkill()
