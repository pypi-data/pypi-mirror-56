"""
Hockey Jockey main menu module.
"""
import hockeyjockey as hj
from os import system, name
import hockeyjockey.config as cfg
import hockeyjockey.models as mod
import hockeyjockey.utilities as ut


class Menu(object):
    """
    Menu class defines functions for displaying menus and handling user input.
    """

    def __init__(self, title, subtitle, opts, prompt_str):
        self.title = title
        self.subtitle = subtitle
        self.opts = opts
        self.prompt_str = prompt_str

        self._prev = None
        self._prev_idx = None

    @property
    def prev(self):
        return self._prev

    @prev.setter
    def prev(self, value: 'Menu') -> None:
        """
        Stores the previous Menu object and its index number.

        :param value: The previous Menu object.
        :return: None.
        """
        self._prev = value
        self._prev_idx = len(self.opts)

    def __str__(self) -> str:
        """
        Returns a string representation of a Menu instance.

        :return: A string representation of a Menu instance.
        """
        # Menu title and subtitle
        menu_str = f'\n{self.title}\n{self.subtitle}\n'

        # Append the menu options
        for i, opt in enumerate(self.opts, 1):
            menu_str += f'{i}. {opt["name"]}\n'

        # Append a 'return to previous menu option' if there was a previous menu
        if self._prev:
            menu_str += str(self._prev_idx + 1) + '. Return\n'

        return menu_str

    def prompt(self) -> None:
        """
        Prompts the user to enter a choice from the displayed menu. Loops until user enters a valid menu option.

        :return: None.
        """
        choice = None
        try:
            # Convert choice to integer and make it zero-based
            choice = int(input(self.prompt_str)) - 1
        except ValueError:
            self.choice_invalid()

        # Execute choice, display previous menu, or invalid choice
        if choice in range(len(self.opts)):
            self.execute(choice)
        elif self._prev and choice == self._prev_idx:
            self._prev.display_menu()
        else:
            self.choice_invalid()

    def choice_invalid(self) -> None:
        """
        Displays a message to the user if they enter an invalid menu choice. Pauses for an 'any key' press, and then
        displays the last menu.

        :return: None.
        """
        input('Invalid choice.  Press any key to continue... ')
        self.display_menu()

    def payload_director(self, fn) -> callable:
        """
        Returns a closure that executes a Jockey function with the correct parameters based on the function name.

        :param fn: The function to execute.
        :return: The return value(s) of the executed function.
        """

        def inner():
            if fn.__name__ == hj.Jockey.load_matchups_custom.__name__:
                return fn(*self.prompt_for_dates())
            elif fn.__name__ == hj.Jockey.compare_stat.__name__:
                return fn(self.prompt_for_stat())
            else:
                # Default behaviour
                fn()

        return inner

    def execute(self, choice: int) -> None:
        """
        Executes the Menu option chosen by the user. The 'payload' to be executed could be a function or another Menu.

        :param choice: An integer representing the Menu option to execute.
        :return: None.
        """
        payload = self.opts[choice]['payload']
        if isinstance(payload, Menu):
            # The payload is a Menu, so update_prev tells the new menu to save a return path
            # to the current menu
            payload.display_menu(prev=self, update_prev=True)
        else:
            # The payload is a function to execute. payload_director returns a closure that knows how to
            # handle different functions
            payload = self.payload_director(payload)
            payload()
            # Give user a chance to read the output
            input('Press any key to continue...')
            # Re-display the menu and keep the current return path
            self.display_menu()

    def display_menu(self, prev: 'Menu' = None, update_prev: bool = False) -> None:
        """
        Clears the screen and displays the menu. If update_prev was set to True, store a return path to the Menu that
        called this one.

        :param prev: A previous Menu that called this one.
        :param update_prev: A boolean that determines whether the return path to the previous Menu should be updated
        before displaying the Menu.
        :return: None.
        """
        # Setup a return path to the previous menu
        if prev and update_prev:
            self.prev = prev

        self.clear()
        print(self)
        self.prompt()

    @staticmethod
    def prompt_for_cached() -> tuple:
        """
        Prompts the user as to whether or not they would like to use Matchups or Stats data loaded to local disk. The
        alternative is to download new data from the internet (statsapi).

        :return: A tuple of booleans indicating the response to both questions.
        """
        Menu.clear()

        print('If you have previously run HockeyJockey, some data may have been cached to disk.')
        print('You can elect to use that data, or download new data from the internet.')
        print()
        m_choice = input(
            'Type \'Y\' to use last MATCHUPS loaded to disk, any other key to reload from internet: ').lower()
        s_choice = input('Type \'Y\' to use last STATS loaded to disk, any other key to reload from internet: ').lower()

        m_choice = m_choice == 'y'
        s_choice = s_choice == 'y'

        return m_choice, s_choice

    @staticmethod
    def prompt_for_dates() -> tuple:
        """
        Prompts the user to enter a start date and an end date.  Loops until a valid start date and end date have
        been entered.

        :return:  A tuple containing a string-formatted start date and end date.
        """

        def date_prompt(date_type: str) -> str:
            """
            Prompts the user to enter a date as specified by date_type. Loops until a valid date is provided.

            :param date_type: An string displayed in the date entry prompt. i.e. 'start date'.
            :return: A string-formatted date.
            """
            print()
            while True:
                date_str = input('Enter {0} date <{1}>: '.format(date_type, ut.DATE_STR))
                return ut.valid_date(date_str) or date_prompt(date_type)

        return date_prompt('start'), date_prompt('end')

    def prompt_for_stat(self) -> int:
        """
        Displays a list of statistics available for comparision and prompts the user to choose one.

        :return: The integer index of the stat.
        """
        print()

        fields = sorted(mod.HJTeamStats._fields)
        field_width = max(map(lambda x: len(x), fields))
        index_width = 2
        acc_width = 0
        stats_str = ''

        for i, f in enumerate(fields):

            acc_width += (index_width + 1 + field_width + 1)
            if acc_width >= cfg.ts.scr_width:
                acc_width = index_width + 1 + field_width + 1
                stats_str += '\n'

            stats_str += f'{i:>{index_width + 1}}. {f:<{field_width + 1}}'

        print(stats_str)
        print()
        choice = None
        while True:
            try:
                choice = int(input('Enter the number of the stat you wish to compare: '))
            except ValueError:
                self.choice_invalid()
            if choice in range(len(fields)):
                return choice
            else:
                self.choice_invalid()

    @staticmethod
    def exit_() -> int:
        """
        Prints a goodbye message and exits the program with exit code 0.

        :return: int exit code 0.
        """
        print()
        print('Goodbye and good luck.')
        return exit(0)

    @staticmethod
    def clear() -> int:
        """
        Clears the screen.

        :return: int exit code 0.
        """
        if name == 'nt':
            return system('cls')
        else:
            return system('clear')
