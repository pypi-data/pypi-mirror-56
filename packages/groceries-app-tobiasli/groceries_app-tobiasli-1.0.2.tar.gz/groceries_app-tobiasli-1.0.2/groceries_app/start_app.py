"""Simple script for starting the Tkinter app."""

import tkinter as tk

from groceries_app.app import GroceryProgram

root = tk.Tk()

email_config = None
wunderpy_config = None

initial_grocery_list = """
tirsdag: fisk
onsdag:taco for 8
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

