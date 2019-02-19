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


def next_player():
    os.system("cmus-remote -n")


def prev_player():
    os.system("cmus-remote -N")


def search_player(text):
    os.system('cmus-remote -C "/' + text+'"')
    os.system('cmus-remote -C "win-activate"')


def refresh_library(path):
    os.system('cmus-remote -C clear')
    LOG.info('reloading music files from: '+path)
    os.system('cmus-remote -C "add '+path+'"')

# TODO GetPlayerRunning implementieren

class Localmusicplayer(MycroftSkill):

    def __init__(self):
        super(Localmusicplayer, self).__init__(name="TemplateSkill")
        # Initialize working variables used within the skill.
        self.music_source = self.settings.get("musicsource", "")
        # init cmus player
        self.start_player()
        refresh_library(self.music_source)

    @intent_file_handler('play.music.intent')
    def handle_play_music_ntent(self, message):
        if not self.running:
            self.start_player()
            self.refresh_library()
        play_player()

    @intent_file_handler('pause.music.intent')
    def handle_pause_music_intent(self, message):
        pause_player()

    @intent_file_handler('reload.library.intent')
    def handle_reload_library_intent(self, message):
        refresh_library(self.music_source)
        self.speak_dialog("refresh.library")

    @intent_file_handler('next.music.intent')
    def handle_next_music_intent(self, message):
        next_player()

    @intent_file_handler('prev.music.intent')
    def handle_prev_music_intent(self, message):
        prev_player()

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

    def converse(self, utterances, lang="en-us"):
        return False

    def stop(self):
        if self.running:
            self.stop_player()


def create_skill():
    return Localmusicplayer()
