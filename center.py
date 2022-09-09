import flet
from flet import (
    Page,
    Text,
    icons,
    colors,
    Divider,
    VerticalDivider,
    AppBar,
    IconButton,
    Image,
    Tabs,
    Tab,
    Container,
    TextButton,
    Column,
    border,
    border_radius,
    margin,
    Row,
    Slider,
    Slider,
    Icon,
    AlertDialog,
    TextField,
    FilePicker,
    FilePickerResultEvent,
    SnackBar
)


from utils import set_defualt_setting, read_data_setting, write_data_setting,_remove_play_list,_add_play_list,_add_new_song,Music
from os.path import exists

# Structure Cofig File ==> There in config.json.example
AddresRepositorie = "https://github.com/PooyaRezaee/PFM-Player"

def main(page: Page):
    # === CHECKER ===
    if not exists('config.json'):
        set_defualt_setting(page)
    # === Settings ===
    page.title = "PFM Player"  # Python Flet Music Player
    page.window_width = 500
    page.window_height = 800
    page.horizontal_alignment = "center"
    page.window_opacity = 0.95
    page.window_title_bar_hidden = True
    page.window_resizable = False
    page.window_center()
    page.show_semantics_debugger = False  # DEBUGER

    # Confg File
    them = read_data_setting()['them']
    page.theme_mode = them

    try:
        music = Music(read_data_setting()["active_song"][1])
    except:
        page.snack_bar = SnackBar(Text("1.Add Song \n2.click on song \n3.Restart Program"))

        page.snack_bar.open = True
        page.update()

    # === EVENTS ===

    def close_window(e):
        page.window_close()

    def minimize_widnow(e):
        pass #TODO MINIMIZE WINDOW AFTER CLICK

    def change_them(e):
        data_them = e.control.data
        if data_them == "dark":
            write_data_setting('them', data_them)
            page.theme_mode = "dark"
            btn_dark_mode.visible = False
            btn_light_mode.visible = True
            page.update()

        elif data_them == "light":
            write_data_setting('them', data_them)
            page.theme_mode = "light"
            btn_light_mode.visible = False
            btn_dark_mode.visible = True
            page.update()

        else:
            raise ValueError('data for change them is wrong')

    def play_song(e):
        # Enable btn old played song and Disable BTN new song player
        this = e.control  # Select Btn Clicked
        active_song = read_data_setting()["active_song"]
        active_song_btn = this.data['tabs']
        for tab in active_song_btn:
            if tab.text == active_song[0]:
                for btn in tab.content.controls:
                    if btn.data != None:
                        if btn.data['path'] == active_song[1]:
                            btn.disabled = False
                            break
                break
        this.disabled = True

        # Write in config file song played
        play_list = this.data['title_play_list']
        path = this.data['path']
        write_data_setting("active_song", [play_list,path])

        if music.is_played:
            music.change_path(path)
            play_pause_btn('changed')

        page.update()
        
    def change_volum(e):
        value = e.control.value
        music.set_volum(value / 100)

    def like_music(e):
        like_btn.visible = not like_btn.visible
        unlike_btn.visible = not unlike_btn.visible
        page.update()

    def play_pause_btn(e):
        if e == "changed":
            if not play_btn.visible:
                music.play()
            return

        if play_btn.visible:
            if not music.is_played():
                music.play()
                
            else:
                music.unpause()
            
            play_btn.visible = False
            pause_btn.visible = True
        else:
            music.pause()
            play_btn.visible = True
            pause_btn.visible = False
        
        page.update()

    def next_song(e):
        active_song = read_data_setting()["active_song"]
        all_play_list = read_data_setting()["play_lists"]
        for play_list in all_play_list:
            if play_list['title'] == active_song[0]:
                i = 0
                for song in play_list["songs"]:
                    if not i == 0:
                        path_next = song["path"]
                        write_data_setting("active_song",[active_song[0],path_next])
                        break
                    elif active_song[1] == song["path"]:
                        i = 1
                        path_next = play_list["songs"][0]["path"]
                        write_data_setting("active_song",[active_song[0],path_next])
                break
        
        for tab in tabs:
            if tab.text == active_song[0]:
                for btn in tab.content.controls:
                    if btn.data != None:
                        if btn.data['path'] == active_song[1]:
                            btn.disabled = False
                        elif btn.data['path'] == path_next:
                            btn.disabled = True

        if music.is_played:
            music.change_path(path_next)
            play_pause_btn('changed')

        page.update()

    def prevous_song(e):
        active_song = read_data_setting()["active_song"]
        all_play_list = read_data_setting()["play_lists"]
        for play_list in all_play_list:
            if play_list['title'] == active_song[0]:
                for song in play_list["songs"]:
                    if active_song[1] == song["path"]:
                        i = play_list["songs"].index(song)
                        prevous_path = play_list["songs"][i - 1]["path"]
                        write_data_setting("active_song",[active_song[0],prevous_path])
                        break
                break
        
        for tab in tabs:
            if tab.text == active_song[0]:
                for btn in tab.content.controls:
                    if btn.data != None:
                        if btn.data['path'] == active_song[1]:
                            btn.disabled = False
                        elif btn.data['path'] == prevous_path:
                            btn.disabled = True

        if music.is_played:
            music.change_path(prevous_path)
            play_pause_btn('changed')

        page.update()


    def add_song(e: FilePickerResultEvent,play_list_name):
        if not e.files:
            return

        files = e.files
        #play_list_name = "defualt" # FIX PROBLEM GET TITLE NAME LIST
        new_songs = []

        for file in files:
            new_song = {}
            new_song["name"] = file.name
            new_song["path"] = file.path

            new_songs.append(new_song)

        new_songs = _add_new_song(play_list_name,new_songs)
        
        for tab in tabs:
            if tab.text == play_list_name:
                old_songs_tab = tab.content.controls
                new_songs_tab = []

                for song in new_songs:
                    selection = TextButton(song["name"], data={"title_play_list": title_play_list, "tabs": tabs,"path": song["path"]}, on_click=play_song, width=400, height=40)  # TODO ADD IMG SONG TO BTN

                    new_songs_tab.append(selection)
                
                _play_list = Column(scroll='always', spacing=0)
                _play_list.controls = new_songs_tab + old_songs_tab

                tab.content = _play_list
                
                break

        page.update()


    def remove_play_list(e):
        _remove_play_list(e.control.data)
        for tab in tabs:
            if tab.text == e.control.data:
                tabs.remove(tab)
                page.update()
                break

    def add_play_list(e):
        command = e.control.data['command']
        if command == "open input":
            page.dialog = get_new_play_list_dialog
            get_new_play_list_dialog.open = True
            page.update()
        elif command == "add":
            name_new_play_list = e.control.data['name_playlist'].value
            e.control.data['name_playlist'].value = ""
            get_new_play_list_dialog.open = False

            

            _add_play_list(name_new_play_list)
            tabs.append(
                Tab(
                    text=name_new_play_list,
                    icon=icons.PLAYLIST_PLAY,
                    content=Column(
                        [
                        Divider(height=0, thickness=0),
                        Row(controls=[
                            TextButton(content=Row(controls=[Text('add song', color=colors.GREEN_300), Icon(icons.ADD, color=colors.GREEN_300)]), icon_color=colors.GREEN_300, on_click=lambda e:pick_song_dialog.pick_files(allow_multiple=True,file_type="audio",dialog_title=name_new_play_list), height=40),
                            TextButton(content=Row(controls=[Text('remove play list', color=colors.RED_300), Icon(icons.REMOVE, color=colors.RED_300)]),icon_color=colors.RED_300, data=name_new_play_list, on_click=remove_play_list, height=40)
                            ],alignment="spaceAround"),
                        Divider(height=0, thickness=0)
                        ]
                    )
                )
            )

            page.update()





        page.update()

    def pin_player(e):
        page.window_always_on_top = not page.window_always_on_top
        btn_pin_player.visible = not btn_pin_player.visible
        btn_unpin_player.visible = not btn_unpin_player.visible

        page.update()

    def open_repositorie(e):
        page.launch_url(AddresRepositorie)

    # === Widgets ===
    btn_close = IconButton(icon=icons.CLOSE, width=40,icon_color=colors.RED_300, on_click=close_window, tooltip='CLOSE')
    btn_change_size = IconButton(icon=icons.MINIMIZE_OUTLINED, width=40,icon_color=colors.BLUE_300, tooltip='MINIMIZE', on_click=minimize_widnow)
    btn_light_mode = IconButton(
        icons.SUNNY, icon_color=colors.YELLOW_50, data='light', on_click=change_them)
    btn_dark_mode = IconButton(
        icons.NIGHTLIGHT, icon_color=colors.BLUE_100, data='dark', on_click=change_them)
    btn_add_playlist = IconButton(
        icon=icons.PLAYLIST_ADD_CIRCLE, icon_color=colors.GREEN_300, on_click=add_play_list,data={"command":"open input"})
    btn_pin_player = IconButton(
        icon=icons.PUSH_PIN_OUTLINED, on_click=pin_player)
    btn_unpin_player = IconButton(
        icon=icons.PUSH_PIN,visible=False, on_click=pin_player)

    Title = Text(value='PFM Player', italic=True, size=30)

    input_add_play_list = TextField(label='Name Play List')
    get_new_play_list_dialog = AlertDialog(
        modal=False,
        title=Text("Add Play List"),
        content=input_add_play_list,
        actions=[
            TextButton("Add", data={"command":"add","name_playlist":input_add_play_list},on_click=add_play_list),
        ],
        actions_alignment="center",
    )

    tabs = [
        Tab(
            icon=icons.FAVORITE_SHARP,
            text="favorite",
        )
    ]

    for item in read_data_setting()["play_lists"]:
        pick_song_dialog = FilePicker(on_result=lambda e: add_song(e,e.control.dialog_title))
        page.overlay.append(pick_song_dialog)


        active_song = read_data_setting()["active_song"]
        title_play_list = item["title"]
        songs = item["songs"]
        list_music = Column(scroll='always', spacing=0)
        for song in songs:
            selection = TextButton(song["name"], data={"title_play_list": title_play_list, "tabs": tabs,"path": song["path"]}, on_click=play_song, width=400, height=40)  # TODO ADD IMG SONG TO BTN

            if active_song[0] == title_play_list and active_song[1] == song["path"]:
                selection.disabled = True
            list_music.controls.append(selection)

        list_music.controls.append(Divider(height=0, thickness=0))
        add_song_btn = TextButton(content=Row(controls=[Text('add song', color=colors.GREEN_300), Icon(icons.ADD, color=colors.GREEN_300)]), icon_color=colors.GREEN_300, on_click=lambda e:pick_song_dialog.pick_files(allow_multiple=True,file_type="audio",dialog_title=title_play_list), height=40) #TODO FIX BUG Don't Change Name Dialog Box as Name Play List
        remove_play_list_btn = TextButton(content=Row(controls=[Text('remove play list', color=colors.RED_300), Icon(icons.REMOVE, color=colors.RED_300)]),icon_color=colors.RED_300, data=title_play_list, on_click=remove_play_list, height=40)
        list_music.controls.append(Row(controls=[add_song_btn, remove_play_list_btn],alignment="spaceAround"))
        list_music.controls.append(Divider(height=0, thickness=0))

        if title_play_list == "favorite":
            list_music.controls[-2].controls.remove(remove_play_list_btn)
            tabs[0].content = list_music
        else:
            tabs.append(
                Tab(
                    text=title_play_list,
                    icon=icons.PLAYLIST_PLAY,
                    content=list_music,
                )
            )

    play_lists = Tabs(
        selected_index=1,
        animation_duration=200,
        tabs=tabs
    )

    play_back_btn = IconButton(icon=icons.SKIP_PREVIOUS_OUTLINED, icon_size=40,on_click=prevous_song)
    pause_btn = IconButton(icon=icons.PAUSE_CIRCLE,icon_size=80, visible=False, on_click=play_pause_btn)
    play_btn = IconButton(icon=icons.PLAY_CIRCLE_FILL,icon_size=80, on_click=play_pause_btn)
    play_next_btn = IconButton(icon=icons.SKIP_NEXT_OUTLINED, icon_size=40,on_click=next_song)

    unlike_btn = IconButton(icon=icons.FAVORITE_BORDER_OUTLINED, icon_size=30, on_click=like_music)
    like_btn = IconButton(icon=icons.FAVORITE, icon_size=30,on_click=like_music, visible=False)
    Volum = Slider(min=0, max=100, divisions=10,label="{value}%", on_change=change_volum, expand=True,value=100)

    if them == 'dark':
        btn_dark_mode.visible = False
    elif them == 'light':
        btn_light_mode.visible = False
    else:
        raise ValueError('exist problem in read config file')
    # === Additions ===



    page.add(Divider(height=0, thickness=0, opacity=0.5))

    icon_main = Image(
        src="icon.png",
        width=30,
        height=30,
        tooltip='PFM Player',
    )

    page.appbar = AppBar(
        toolbar_height=43,
        leading_width=0,
        title=Title,
        actions=[
            icon_main,
            VerticalDivider(width=20, opacity=0.5, thickness=1),
            btn_pin_player,
            btn_unpin_player,
            IconButton(icons.CODE_OUTLINED,on_click=open_repositorie),
            btn_add_playlist,
            btn_light_mode,
            btn_dark_mode,
            btn_change_size,
            btn_close,
            VerticalDivider(width=5, opacity=0),
        ],
    )

    page.add(Container(
        width=400,
        height=550,
        content=play_lists,
        padding=0,
        margin=margin.only(left=10, right=10, top=0, bottom=0),
        # alignment=alignment.center,
        # bgcolor='#FFCC0000',
        border=border.all(3, '#2f2f2f'),
        border_radius=border_radius.all(5),

    )
    )

    page.add(Column(controls=[
        Row(
            controls=[
                play_back_btn,
                pause_btn,
                play_btn,
                play_next_btn
            ],
            alignment='center'
        ),
        Row(
            controls=[
                unlike_btn,
                like_btn,
                Volum,
            ]
        ),
    ]
    ))

    page.update()


flet.app(target=main, assets_dir="assets")
