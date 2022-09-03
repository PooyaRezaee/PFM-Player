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
    page.window_title_bar_hidden = True
    page.window_resizable = False
    page.window_always_on_top = True  # This is For easy Debuging is Active
    page.window_center()

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

    page.update()
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
            IconButton(icons.CODE_OUTLINED),
            btn_light_mode,
            btn_dark_mode,
            btn_change_size,
            btn_close,
            VerticalDivider(width=5, opacity=0),
        ],
    )

    page.update()


flet.app(target=main, assets_dir="assets")
