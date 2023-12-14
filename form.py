from datetime import time
from enum import Enum

class PaymentMethod(Enum):
    card: str = 'Card'
    cash: str = 'Cash'

class Form:
    types = {
        "str": str,
        "time": time,
        "PaymentMethod": PaymentMethod,
    }
    def __init__(self, form_fields):
        form_fields = form_fields.split(",")
        self.validation_dict = {
            name.strip(): self.types[t.strip()] for name, t in zip(form_fields[::2], form_fields[1::2])
        }
        self.form = {
            name.strip(): None for name, t in zip(form_fields[::2], form_fields[1::2])
        }

    def set_value(self, key, value):
        if self.form[key] == None:
            self.form[key] = value
    
    def get_value(self, key):
        return self.form.get(key)