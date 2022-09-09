import json


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
        "them": "dark",
    }

    json_object = json.dumps(defualt_setting, indent=4)

    with open("config.json", "w") as file:
        file.write(json_object)

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

