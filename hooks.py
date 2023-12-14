from cat.mad_hatter.decorators import tool, hook
import os.path
import json

def get_settings():
    if os.path.isfile("cat/plugins/pizzayolo/settings.json"):
        with open("cat/plugins/pizzayolo/settings.json", "r") as json_file:
            settings = json.load(json_file)
    else:
        with open("cat/plugins/pizzayolo/settings.json", "r") as json_file:
            settings = json.load(json_file)
    return settings

@hook
def agent_prompt_prefix(prefix, cat):
    settings = get_settings()
    prefix = settings["prompt_prefix"]

    return prefix

