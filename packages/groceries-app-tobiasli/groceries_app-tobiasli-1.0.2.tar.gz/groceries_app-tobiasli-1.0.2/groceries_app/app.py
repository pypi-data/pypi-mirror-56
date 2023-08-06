import os
import html
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

from groceries import Cookbook, Menu
from groceries import config
from groceries_app import cookbook_reader
from groceries_app.wunderlist import add_groceries_to_wunderlist, WunderpyAccessBase
from groceries_app.email_sender import send_email, EmailAccessBase

# Initialize cookbook:
path = os.path.dirname(__file__)
cookbook_file = os.path.join(path, 'cookbook.yaml')
COOKBOOK = Cookbook(cookbook_reader.recipes)


class GroceryProgram:

    def __init__(self, master,
                 email_config: EmailAccessBase = None,
                 wunderpy_config: WunderpyAccessBase = None,
                 inital_grocery_content: str = ''):
        self.inital_menu_content = inital_grocery_content
        self.wunderpy_config = wunderpy_config
        self.email_config = email_config
        self.master = master

        self.master.wm_title('Grocery shopping')
        self.master.geometry('1000x500')

        self.current_menu = None

        # Grid definition:

        tk.Grid.rowconfigure(self.master, 0, weight=1)
        tk.Grid.columnconfigure(self.master, 0, weight=1)

        frame = tk.Frame(self.master)
        frame.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        grid = tk.Frame(frame)
        grid.grid(sticky=tk.N + tk.S + tk.E + tk.W, column=0, row=0)
        tk.Grid.rowconfigure(frame, 0, weight=1)
        tk.Grid.columnconfigure(frame, 0, weight=1)

        ## Grocery list
        self.grocery_list = ScrolledText(frame, undo=True)
        self.grocery_list.grid(rowspan=2, columnspan=1, row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W, padx=10,
                               pady=10)

        # Set callback on all key presses:
        bindtags = list(self.grocery_list.bindtags())
        bindtags.insert(2, "custom")  # index 1 is where most default bindings live
        self.grocery_list.bindtags(tuple(bindtags))
        self.grocery_list.bind_class("custom", "<Key>", self.callback_any_key_grocery_list)
        self.grocery_list.bind('<Control-Return>', self.callback_controll_return_grocery_list)
        self.grocery_list.bind('<Control-BackSpace>', self.callback_get_recipe_from_parsed)
        # self.grocery_list.bind('<Key>', self.callback_parse_grocery_list)

        # set initial grocery_list:
        self.grocery_list.insert(tk.INSERT,
                                 inital_grocery_content)

        ## Menu list
        self.menu_box = ScrolledText(frame, undo=True)
        self.menu_box.grid(rowspan=2, columnspan=3, row=0, column=1, sticky=tk.N + tk.S + tk.E + tk.W, padx=10, pady=10)

        ## View menu
        self.view_menu_button = tk.Button(frame, text='View menu', command=self.callback_view_menu)
        self.view_menu_button.grid(rowspan=1, columnspan=1, row=2, column=0, sticky=tk.N + tk.S + tk.E + tk.W,
                                   padx=10, pady=10)

        ## View grocery list
        self.view_grocery_list = tk.Button(frame, text='View grocery list',
                                           command=self.callback_view_grocery_list)
        self.view_grocery_list.grid(rowspan=1, columnspan=1, row=3, column=0, sticky=tk.N + tk.S + tk.E + tk.W,
                                    padx=10, pady=10)

        ## View categories
        self.categories_button = tk.Button(frame, text='View categories', command=self.calback_show_categories_list)
        self.categories_button.grid(rowspan=1, columnspan=1, row=2, column=1, sticky=tk.N + tk.S + tk.E + tk.W, padx=10,
                                    pady=10)

        ## Commands
        self.command_text = tk.Label(frame, text='Ctrl+Enter: Reroll recipe suggestion.\nCtrl+Backspace: Lock suggestion.')
        self.command_text.grid(rowspan=1, columnspan=1, row=3, column=1, sticky=tk.N + tk.S + tk.E + tk.W, padx=10,
                               pady=10)

        ## Email recipients
        self.email_target_entry = tk.Entry(frame)
        self.email_target_entry.grid(rowspan=1, columnspan=1, row=2, column=2, sticky=tk.N + tk.S + tk.E + tk.W,
                                     padx=10, pady=10)
        if self.email_config:
            self.email_target_entry.insert(tk.INSERT,
                                           ', '.join(self.email_config.recipients))

        ## Send email_sender button
        self.email_button = tk.Button(frame, text='Send menu to email_sender', command=self.callback_send_menu_to_email)
        self.email_button.grid(rowspan=1, columnspan=1, row=2, column=3, sticky=tk.N + tk.S + tk.E + tk.W, padx=10,
                               pady=10)
        if not self.email_config:
            self.email_button['state'] = tk.DISABLED

        ## Wunderlist target entry
        self.wunderlist_target_entry = tk.Entry(frame)
        self.wunderlist_target_entry.grid(rowspan=1, columnspan=1, row=3, column=2, sticky=tk.N + tk.S + tk.E + tk.W,
                                          padx=10, pady=10)
        if self.wunderpy_config:
            self.wunderlist_target_entry.insert(tk.INSERT, self.wunderpy_config.default_list)

        ## Send to wunderlist button:
        self.send_to_wunderlist_button = tk.Button(frame, text='Send groceries to Wunderlist',
                                                   command=self.callback_send_to_wunderlist_button)
        self.send_to_wunderlist_button.grid(rowspan=1, columnspan=1, row=3, column=3, sticky=tk.N + tk.S + tk.E + tk.W,
                                            padx=10, pady=10)
        if not self.wunderpy_config:
            self.send_to_wunderlist_button['state'] = tk.DISABLED

        rows = range(3)
        columns = []

        for row in rows:
            tk.Grid.rowconfigure(frame, row, weight=1)
        for column in columns:
            tk.Grid.columnconfigure(frame, column, weight=1)

        self.parse_grocery_list()

    def callback_get_recipe_from_parsed(self, event):
        cursor_position = self.grocery_list.index(tk.INSERT)
        row = int(cursor_position.split('.')[0])
        corresponding_line = self.menu_box.get(1.0, tk.END).split('\n')[row - 1]
        all_lines = self.grocery_list.get(1.0, tk.END).split('\n')
        # Swap line:
        all_lines[row - 1] = corresponding_line

        self.grocery_list.delete(1.0, tk.END)
        self.grocery_list.insert(tk.INSERT, '\n'.join(all_lines))
        self.grocery_list.mark_set(tk.INSERT, cursor_position)
        print("I've hit control+backspace at row {0} and column {1}".format(
            *self.grocery_list.index(tk.INSERT).split('.')))
        return 'break'

    def callback_send_menu_to_email(self):
        print('send menu by email_sender button')
        sender = 'GroceryProgram'
        recipients = self.email_target_entry.get().split(', ')
        text = html.escape(self.current_menu.generate_menu_str(), quote=True)
        template = '<html><pre><font face="Courier New, Courier, monospace">%s</font></pre></html>' % text
        template = template.replace('\n', '<br />')

        send_email(self.email_config, 'Week menu', recipients, template)
        print('email_sender ok')

    def callback_send_to_wunderlist_button(self):
        print('send to wunderlist button')
        target_list = self.wunderlist_target_entry.get()

        # Create a list of {item, description} for all groceries
        processed_groceries = []
        for grocery in self.current_menu.groceries.components():
            item = ''
            if grocery['amount']:
                item += grocery['amount'] + ' '
            item += grocery['name']

            descriptions = []
            for source_dict in grocery['components']:
                source = ''
                source_name = ''
                if source_dict['amount']:
                    source_name += source_dict['amount'] + ' '
                source_name += source_dict['name']

                source += source_name

                if source_dict['comments']:
                    comments = '(' + ', '.join(source_dict['comments']) + ')'
                    source += comments + ' '

                if source_dict['recipe']:
                    recipe = ' til %s' % source_dict['recipe']
                    if not source_dict['recipe'] == config.language.no_recipe_name:
                        if source_dict['recipe_multiplier'] == 1:
                            recipe += ' for %d pers' % source_dict['recipe_made_for']
                        else:
                            recipe += ' x%f' % source_dict['recipe_multiplier']
                    source += recipe

                descriptions += [source]

            processed_groceries += [{'item': item, 'description': ', '.join(descriptions)}]

        response = add_groceries_to_wunderlist(self.wunderpy_config, target_list_name=target_list,
                                               groceries=processed_groceries)

        print(response)

    def callback_controll_return_grocery_list(self, event):
        self.parse_grocery_list(smart=False)
        return 'break'

    def callback_any_key_grocery_list(self, event):
        self.parse_grocery_list()

    def callback_button_parse_grocery_list(self):
        self.parse_grocery_list(smart=False)

    def parse_grocery_list(self, smart=True):
        print('callback works')
        text = self.grocery_list.get(1.0, tk.END)

        self.menu_box.delete(1.0, tk.END)

        if text.strip() == 'tags':
            string = '\n'.join([tag for tag in COOKBOOK.available_tags.keys()])
            self.menu_box.insert(tk.INSERT, string)
        if text.strip() == 'recipes':
            string = '\n'.join(COOKBOOK.available_recipes)
            self.menu_box.insert(tk.INSERT, string)
        else:
            # Intelligent update: Only update the lines that have changed.
            if not self.current_menu or not smart:
                self.current_menu = COOKBOOK.parse_menu(self.grocery_list.get(1.0, tk.END))
            else:
                new_menu = COOKBOOK.parse_menu(self.grocery_list.get(1.0, tk.END))

                for index, line in enumerate(new_menu.input_lines):
                    if line in self.current_menu.input_lines:
                        current_index = self.current_menu.input_lines.index(line)
                        new_menu.input_lines[index] = self.current_menu.input_lines[current_index]
                        new_menu.processed_lines[index] = self.current_menu.processed_lines[current_index]

                new_menu.input_plan = '\n'.join(new_menu.input_lines)
                new_menu.processed_plan = new_menu.create_output_lines(new_menu.processed_lines)
                self.current_menu = new_menu

                self.current_menu.process_input()

            self.menu_box.insert(tk.INSERT, self.current_menu.processed_plan)

    def callback_view_menu(self):
        """Callback for the send menu as email_sender button."""
        print('callback_send_menu_email')
        if isinstance(self.current_menu, Menu):
            self.menu_box.delete(1.0, tk.END)
            self.menu_box.insert(tk.INSERT, '\n'+self.current_menu.generate_menu_str())
        else:
            print('No menu to view')

    def callback_view_grocery_list(self):
        """Callback for the send menu as email_sender button."""
        print('callback_view_grocery_list')
        if isinstance(self.current_menu, Menu):
            self.menu_box.delete(1.0, tk.END)
            string = '\n'.join(self.current_menu.groceries.ingredients_formatted(pretty=True, sort='alphabetical'))
            self.menu_box.insert(tk.INSERT, string)
        else:
            print('No menu to view')

    def calback_show_categories_list(self):
        self.menu_box.delete(1.0, tk.END)
        string = '\n'.join(sorted(COOKBOOK.tags))
        self.menu_box.insert(tk.INSERT, string)

##w = Label(root, text="Red Sun", bg="red", fg="white")
##w.pack(fill=X,padx=10)
##w = Label(root, text="Green Grass", bg="green", fg="black")
##w.pack(fill=X,padx=10)
##w = Label(root, text="Blue Sky", bg="blue", fg="white")
##w.pack(fill=X,padx=10)
##
##colours = ['red','green','orange','white','yellow','blue']
##
##r = 0
##for c in colours:
##    Label(text=c, relief=RIDGE,width=15).grid(row=r,column=0)
##    Entry(bg=c, relief=SUNKEN,width=10).grid(row=r,column=1)
##    r = r + 1
