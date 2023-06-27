RU = 'RU'
EN = 'EN'
Locale = RU


def MENU_FILE_EXIT():
    if Locale == RU:
        return 'Выход'
    else:
        return 'Exit'


def MENU_HELP_ABOUT():
    if Locale == RU:
        return 'О программе'
    else:
        return 'About'
