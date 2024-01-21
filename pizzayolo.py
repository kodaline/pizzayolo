from cat.mad_hatter.decorators import tool, hook, plugin
from pydantic import BaseModel, Field
from datetime import datetime, date, time
from pprint import pprint
from cat.plugins.pizzayolo.form import Form
import json
from cat.log import log

class MySettings(BaseModel):
    menu: str = Field(
        title="Available",
        description="Names of the available pizza flavors in your pizzeria",
        default="""margherita, ortolana, quattro stagioni, quattro formaggi, salsiccia e friarielli, diavola""",
        extra={"type": "TextArea"}
    )
    form_fields: str = Field(
        title="Form",
        description="Names of the dictionary keys form data to be collected from the customer",
        default="pizza_flavor, str, delivery_time, time, delivery_address, str, user_phone, str, payment_method, PaymentMethod",
        extra={"type": "TextArea"}
    )

@plugin
def settings_schema():
    return MySettings.schema()

@tool(return_direct=True)
def pizzayolo(tool_input, cat):
    """Use this tool to get pizza orders from a customer.
    While collecting the data, return them always in a JSON
    """
    log.error(cat.mad_hatter.get_plugin().load_settings())
    menu = cat.mad_hatter.get_plugin().load_settings()["menu"]
    form_fields = cat.mad_hatter.get_plugin().load_settings()["form_fields"]
    pprint(menu)
    pprint(form_fields)
    form_object = Form(form_fields)
    if tool_input == "None":
        return "If you want to place a pizza order, please let me know the following information: %s" % ([val.replace("_"," ") for val in form_object.form.keys()],)
    '''
    try:
        c_tool_input = tool_input.replace("'", '"')
        pprint("c_tool_input============================================")
        pprint(c_tool_input)
        pprint("============================================")
        collected_data = json.loads(c_tool_input)
        pprint("collected_data============================================")
        pprint(collected_data)
        pprint("============================================")
    except Exception as e:
        pprint(e)
        return "Can you repeat please?"
    for k in collected_data:
        if k != "pizza_flavor":
            form_object.set_value(k, collected_data[k])
    pprint("form_object.form============================================")
    pprint(form_object.form)
    pprint("============================================")
    if collected_data["pizza_flavor"] not in menu:
        return "This flavor is not available, sorry, can you provide one from the menu please, %s?" % menu
    '''


@hook
def before_agent_starts(agent_input, cat):
    form_fields = cat.mad_hatter.get_plugin().load_settings()["form_fields"]
    form_fields = form_fields.split(",")
    form = {
        name.strip(): None for name, t in zip(form_fields[::2], form_fields[1::2])
    }
    pprint(form)
    pprint("agent_input========")
    pprint(agent_input)
    pprint("========")
    agent_input["declarative_memory"] = f"""\nYou need to collect the following data and return a JSON {form}"""
    pprint("declarative====")
    pprint(agent_input["declarative_memory"])
    pprint("=====")
    return agent_input