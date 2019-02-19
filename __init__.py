from mycroft import MycroftSkill, intent_file_handler


class Localmusicplayer(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('localmusicplayer.intent')
    def handle_localmusicplayer(self, message):
        self.speak_dialog('localmusicplayer')


def create_skill():
    return Localmusicplayer()

