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

    return TRUE