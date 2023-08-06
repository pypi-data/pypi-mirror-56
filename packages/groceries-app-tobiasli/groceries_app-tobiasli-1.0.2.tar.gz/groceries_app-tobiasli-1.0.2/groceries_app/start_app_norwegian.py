"""Simple script for starting the Tkinter app."""

import tkinter as tk

from groceries_app.app import GroceryProgram
from groceries_app.email_sender.config import EmailAccessEnvironmentVariables
from groceries_app.wunderlist.config import WunderpyAccessEnvironmentVariables

from groceries import config, language

# Set different language:
config.set_config(language.norwegian.language)

root = tk.Tk()

try:
    email_config = EmailAccessEnvironmentVariables(
        api_var='EMAIL_API',
        sender_email_var='EMAIL_SENDER',
        token_var='EMAIL_TOKEN',
        recipients_var='EMAIL_RECIPIENTS')
except EnvironmentError:
    email_config = None

try:
    wunderpy_config = WunderpyAccessEnvironmentVariables(
        client_id_var='WUNDERPY_CLIENT_ID',
        access_token_var='WUNDERPY_ACCESS_TOKEN',
        default_list_var='WUNDERPY_DEFAULT_LIST',
    )
except EnvironmentError:
    wunderpy_config = None


initial_grocery_list = """
tirsdag: fisk
onsdag:taco til 8
2 l melk
500 ts melk
2 agurker
1/2 boks rømme'"""


grocery_program = GroceryProgram(
    master=root,
    email_config=email_config,
    wunderpy_config=wunderpy_config,
    inital_grocery_content=initial_grocery_list

)
root.mainloop()

