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
    TextField
)


from utils import set_defualt_setting, read_data_setting, write_data_setting,_remove_play_list,_add_play_list
from os.path import exists

# Structure Cofig File ==> active_song: the song playing -> PlayListName:path | them: 'dark' or light 'them' | play_lists: [  {title:name play list , paths:list of path songs },...  ] |


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
    # page.window_resizable = False
    page.window_center()
    page.show_semantics_debugger = False  # DEBUGER

    # Confg File
    them = read_data_setting()['them']
    page.theme_mode = them

    # === EVENTS ===

    def close_window(e):
        page.window_close()

    def minimize_widnow(e):
        pass

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
        # TODO COMPLATE IT --> 1.Play Song

        # Enable btn old played song and Disable BTN new song player
        this = e.control  # Select Btn Clicked
        active_song = read_data_setting()["active_song"].split(':')
        active_song_btn = this.data['tabs']
        for tab in active_song_btn:
            if tab.text == active_song[0]:
                for btn in tab.content.controls:
                    if btn.data['path'] == active_song[1]:
                        btn.disabled = False
                        break
                break
        this.disabled = True

        # Write in config file song played
        play_list = this.data['title_play_list']
        path = this.text
        write_data_setting("active_song", f"{play_list}:{path}")

        page.update()

    # TODO To Work Play Music and other Funcionts
    def change_volum(e):
        page.update()

    def like_music(e):
        like_btn.visible = not like_btn.visible
        unlike_btn.visible = not unlike_btn.visible
        page.update()

    def play_pause_btn(e):
        play_btn.visible = not play_btn.visible
        pause_btn.visible = not pause_btn.visible
        page.update()

    def add_song(e):
        pass

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
                )
            )

            page.update()


    def remove_play_list(e):
        _remove_play_list(e.control.data)
        for tab in tabs:
            if tab.text == e.control.data:
                tabs.remove(tab)
                page.update()
                break


        page.update()

    def pin_player(e):
        page.window_always_on_top = not page.window_always_on_top
        btn_pin_player.visible = not btn_pin_player.visible
        btn_unpin_player.visible = not btn_unpin_player.visible

        page.update()

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
        ),
        Tab(
            text="defualt",
            icon=icons.PLAYLIST_PLAY,
        ),
    ]

    for item in read_data_setting()["play_lists"]:
        active_song = read_data_setting()["active_song"].split(':')
        title_play_list = item["title"]
        paths = item["paths"]
        list_music = Column(scroll='always', spacing=0)
        for path in paths:
            selection = TextButton(f"{path}", data={"title_play_list": title_play_list, "tabs": tabs,"path": path}, on_click=play_song, width=400, height=40)  # TODO ADD IMG SONG TO BTN

            if active_song[0] == title_play_list and active_song[1] == path:
                selection.disabled = True
            list_music.controls.append(selection)

        list_music.controls.append(Divider(height=0, thickness=0))
        add_song_btn = TextButton(content=Row(controls=[Text('add song', color=colors.GREEN_300), Icon(icons.ADD, color=colors.GREEN_300)]), icon_color=colors.GREEN_300, on_click=add_song, height=40)
        remove_play_list_btn = TextButton(content=Row(controls=[Text('remove play list', color=colors.RED_300), Icon(icons.REMOVE, color=colors.RED_300)]),icon_color=colors.RED_300, data=title_play_list, on_click=remove_play_list, height=40)
        list_music.controls.append(Row(controls=[add_song_btn, remove_play_list_btn],alignment="spaceAround"))
        list_music.controls.append(Divider(height=0, thickness=0))

        if title_play_list == "favorite":
            list_music.controls[-2].controls.remove(remove_play_list_btn)
            tabs[0].content = list_music
        elif title_play_list == "defualt":
            tabs[1].content = list_music
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

    play_back_btn = IconButton(icon=icons.SKIP_PREVIOUS_OUTLINED, icon_size=40)
    pause_btn = IconButton(icon=icons.PAUSE_CIRCLE,icon_size=80, visible=False, on_click=play_pause_btn)
    play_btn = IconButton(icon=icons.PLAY_CIRCLE_FILL,icon_size=80, on_click=play_pause_btn)
    play_next_btn = IconButton(icon=icons.SKIP_NEXT_OUTLINED, icon_size=40)

    unlike_btn = IconButton(icon=icons.FAVORITE_BORDER_OUTLINED, icon_size=30, on_click=like_music)
    like_btn = IconButton(icon=icons.FAVORITE, icon_size=30,on_click=like_music, visible=False)
    Volum = Slider(min=0, max=100, divisions=10,label="{value}%", on_change=change_volum, expand=True)

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
            # TODO OPEN LINK REPOSITORY GITHUB AFTER CLICK ON BTN
            IconButton(icons.CODE_OUTLINED),
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
