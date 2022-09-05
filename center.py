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
    alignment,
    TextButton,
    Column,
    alignment,
    border,
    border_radius,
    margin,
)

from utils import set_defualt_setting, read_data_setting, write_data_setting
from os.path import exists


def main(page: Page):
    # === CHECKER ===
    if not exists('config.json'):
        set_defualt_setting(page)
    # === Settings ===
    page.title = "PFM Player"  # Python Flet Music Player
    page.window_width = 500
    page.window_height = 700
    page.horizontal_alignment = "center"
    page.window_opacity = 0.95
    # page.window_title_bar_hidden = True
    # page.window_resizable = False
    # page.window_always_on_top = True  # This is For easy Debuging is Active
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
        this = e.control # Select Btn Clicked
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
        write_data_setting("active_song",f"{play_list}:{path}")


        page.update()

    # TODO To Work Play Music and other Funcionts

    # === Widgets ===
    btn_close = IconButton(icon=icons.CLOSE, width=40,
                           icon_color=colors.RED_300, on_click=close_window, tooltip='CLOSE')
    btn_change_size = IconButton(icon=icons.MINIMIZE_OUTLINED, width=40,
                                 icon_color=colors.BLUE_300, tooltip='MINIMIZE', on_click=minimize_widnow)
    btn_light_mode = IconButton(
        icons.SUNNY, icon_color=colors.YELLOW_50, data='light', on_click=change_them)
    btn_dark_mode = IconButton(
        icons.NIGHTLIGHT, icon_color=colors.BLUE_100, data='dark', on_click=change_them)
    Title = Text(value='PFM Player', italic=True, size=30)

    tabs = [
        Tab(
            icon=icons.FAVORITE_SHARP,
            text="favorite",
            content=Container(
                content=Text("This is Tab 1"), alignment=alignment.center
            ),
        ),
        Tab(
            text="Defualt",
            icon=icons.PLAYLIST_PLAY,
            content=Text("This is Tab 2"),
        ),
    ]

    for item in read_data_setting()["play_lists"]:
        active_song = read_data_setting()["active_song"].split(':')
        title_play_list = item["title"]
        paths = item["paths"]
        list_music = Column(scroll='always', spacing=0)
        for path in paths:
            selection = TextButton(f"{path}"  ,data={"title_play_list":title_play_list,"tabs":tabs,"path":path}, on_click=play_song, width=400, height=40) #TODO ADD IMG SONG TO BTN

            if active_song[0] == title_play_list and active_song[1] == path:
                selection.disabled = True
            list_music.controls.append(selection)

        if title_play_list == "favorite":
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
            # TODO OPEN LINK REPOSITORY GITHUB AFTER CLICK ON BTN
            IconButton(icons.CODE_OUTLINED),
            btn_light_mode,
            btn_dark_mode,
            btn_change_size,
            btn_close,
            VerticalDivider(width=5, opacity=0),
        ],
    )

    page.add(Container(
        width=400,
        height=500,
        content=play_lists,
        padding=0,
        margin=margin.only(left=10, right=10, top=0, bottom=0),
        # alignment=alignment.center,
        # bgcolor='#FFCC0000',
        border=border.all(3, '#2f2f2f'),
        border_radius=border_radius.all(5),

    )
    )

    # TODO MAKE BTN PLAYER --> (play,stop,volum,like)

    page.update()


flet.app(target=main, assets_dir="assets")
