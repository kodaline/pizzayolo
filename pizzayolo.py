from cat.mad_hatter.decorators import tool, hook, plugin
from pydantic import BaseModel, Field
from datetime import datetime, date, time
from pprint import pprint
from form import Form
import json
from hooks import get_settings

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

menu = get_settings()["menu"]
form_fields = get_settings()["form_fields"]
form_object = Form(form_fields)

@plugin
def settings_schema():   
    return MySettings.schema()

@tool(return_direct=True)
def pizzayolo(tool_input, cat):
    """Use this tool to get pizza orders from a customer.
       The Input is a dictionary structure with the following keys:
       - pizza_flavor: the pizza flavor, the available pizzas are in the menu, if a pizza is not in the menu you need to inform the customer and ask another flavor
       - delivery_time: when to deliver the pizza at delivery_address
       - delivery_address: where to deliver the order
       - user_phone: customer telephone contact
       - payment_method: the type of payment method: it can be card or cash

       The Input needs to be filled only with the correct information the customer gives during the conversation, if no information is given by the customer answer with None.
    """

    pprint("tool input============================================")
    pprint(tool_input)
    pprint("============================================")
    if tool_input == "None":
        return "If you want to place a pizza order, please let me know the following information: %s" % ([val.replace("_"," ") for val in form_object.form.keys()],)
    try:
        c_tool_input = tool_input.replace("'", '"')
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
