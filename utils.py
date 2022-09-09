import json
from pygame import mixer

class Music():
    def __init__(self,path):
        self.mixer = mixer
        self.music = self.mixer.music
        self.path = path
        self.IS_PLAY = False
        self.IS_PLAYED = False

        self.mixer.init()
        self.music.load(self.path)
    
    def play(self):
        self.music.play()
        self.IS_PLAYED = True
        self.IS_PLAY = True
    
    def change_path(self,path):
        self.stop()
        self.IS_PLAYED = False
        self.IS_PLAY = False
        self.path = path
        self.music.load(self.path)

    def pause(self):
        self.music.pause()
        self.IS_PLAY = False

    def unpause(self):
        self.music.unpause()
        self.IS_PLAY = True


    def stop(self,fade=False):
        self.IS_PLAY = False
        if fade:
            self.music.fadeout(800)
        else:
            self.music.stop()
    

    def set_volum(self,volum):
        # 0 to 1
        self.music.set_volume(volum)
    
    def set_pos(self,secound):
        self.music.set_pos(secound)
    
    def get_volum(self):
        return self.music.get_volume()

    def get_pos(self):
        return self.music.get_pos()

    def is_play(self):
        return self.IS_PLAY

    def is_played(self):
        return self.IS_PLAYED

def read_data_setting():
    with open('config.json', 'r') as file:
        json_config = json.load(file)

    return json_config


def write_data_setting(key, value):
    settings = read_data_setting()
    settings[key] = value

    new_settings = json.dumps(settings, indent=4)

    with open("config.json", "w") as file:
        file.write(new_settings)

    return True


def set_defualt_setting(page):
    defualt_setting = {
        "active_song": ["play list name","path"],
        "them": "dark",
        "play_lists": [{"title": "favorite","songs": []}]
    }

    configs = json.dumps(defualt_setting, indent=4)

    with open("config.json", "w") as file:
        file.write(configs)

    return True

def _remove_play_list(play_list_name):
    play_lists = read_data_setting()['play_lists']

    for play_list in play_lists:
        if play_list['title'] == play_list_name:
            play_lists.remove(play_list)
        
    write_data_setting("play_lists",play_lists)

def _add_play_list(play_list_name):
    play_lists = read_data_setting()['play_lists']
    play_lists.append({"title":play_list_name,"songs":[]})
        
    write_data_setting("play_lists",play_lists)

def _add_new_song(play_list_name,songs_list):
    play_lists = read_data_setting()['play_lists']
    for play_list in play_lists:
        if play_list["title"] == play_list_name:
            
            theree_song = play_list["songs"]
            for song in songs_list.copy():
                if song in theree_song:
                    songs_list.remove(song)
                    print('have repet')
            

            play_list["songs"].extend(songs_list)
            break
    
    write_data_setting("play_lists",play_lists)

    return songs_list

