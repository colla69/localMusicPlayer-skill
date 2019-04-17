import os
import time
from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_file_handler, intent_handler
from mycroft.util.log import LOG
from mycroft.skills.common_play_skill import CommonPlaySkill, CPSMatchLevel

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
    LOG.info('cmus-remote -C "/' + text+'"')
    os.system('cmus-remote -C "/' + text+'"')
    os.system('cmus-remote -C "win-activate"')


def refresh_library(path):
    os.system('cmus-remote -C clear')
    LOG.info('reloading music files from: '+path)
    os.system('cmus-remote -C "add '+path+'"')


def show_player():
    os.system('x-terminal-emulator -e "screen -r " ')


def getrunning():
    check = os.popen('ps ax | grep cmus | grep -v " grep"').readlines()
    if len(check) == 0:
        return False
    else:
        return True


def shufflin():
    check = os.popen('cmus-remote -Q | grep "shuffle" |  tail -c 5').readlines()
    if check[0] == "true\n":
        return True
    else:
        return False


def changeshuffling():
    if shufflin():
        os.system('cmus-remote -C "set shuffle=false"')
    else:
        os.system('cmus-remote -C "set shuffle=true"')


class Localmusicplayer(CommonPlaySkill):
    def CPS_match_query_phrase(self, phrase):
        library = open('/home/cola/.config/cmus/lib.pl')
        for line in library:
            mySongs.append(line.strip())

        LOG.info(mySongs)

        return phrase, CPSMatchLevel.TITLE

    def CPS_start(self, phrase, data):
        #search_player(phrase)
        pass

    def __init__(self):
        super().__init__(name="TemplateSkill")
        # Initialize working variables used within the skill.
        self.music_source = self.settings.get("musicsource", "")
        # init cmus player
        self.activate_player()

    def getspoken_shufflestate(self):
        if shufflin():
            self.speak("active")
        else:
            self.speak("nonoperational")

    @intent_file_handler('play.music.intent')
    def handle_play_music_ntent(self, message):
        self.activate_player()
        play_player()

    @intent_file_handler('pause.music.intent')
    def handle_pause_music_intent(self, message):
        self.activate_player()
        pause_player()

    @intent_file_handler('reload.library.intent')
    def handle_reload_library_intent(self, message):
        refresh_library(self.music_source)
        self.speak_dialog("refresh.library")

    @intent_file_handler('shuffling.library.intent')
    def handle_shuffling_library_intent(self, message):
        self.getspoken_shufflestate()

    @intent_file_handler('next.music.intent')
    def handle_next_music_intent(self, message):
        self.activate_player()
        next_player()

    @intent_file_handler('prev.music.intent')
    def handle_prev_music_intent(self, message):
        self.activate_player()
        prev_player()

    @intent_file_handler('show.music.intent')
    def handle_show_music_intent(self, message):
        self.activate_player()
        show_player()

    @intent_file_handler('change.shuffling.music.intent')
    def handle_change_shuffle_music_intent(self, message):
        changeshuffling()
        self.getspoken_shufflestate()

    @intent_handler(IntentBuilder("search.music.intent").require("search.music").require("SongToPlay").build())
    def handle_search_music_intent(self, message):
        songtoplay = message.data.get("SongToPlay")
        self.activate_player()
        LOG.info("playing "+songtoplay)
        search_player(songtoplay)

    def start_player(self):
        os.system("screen -d -m -S cmus cmus &")
        time.sleep(1)
        # config player for usage
        os.system('cmus-remote -C "view 2"')
        os.system('cmus-remote -C "set softvol_state=70 70"')
        os.system('cmus-remote -C "set continue=true"')
        time.sleep(1)
        refresh_library(self.music_source)

    def stop_player(self):
        os.system("cmus-remote -C quit")

    def activate_player(self):
        if not getrunning():
            self.start_player()
            refresh_library(self.music_source)

    def converse(self, utterances, lang="en-us"):
        return False

    def stop(self):
        pass
        #if getrunning():
        #  self.stop_player()


def create_skill():
    return Localmusicplayer()
