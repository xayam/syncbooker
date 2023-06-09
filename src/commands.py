from abc import ABC, abstractmethod


class Commands(ABC):
    @abstractmethod
    def menu_file_exit_click(self, event=None):
        pass

    @abstractmethod
    def menu_help_faq_click(self, event=None):
        pass

    @abstractmethod
    def menu_help_about_click(self, event=None):
        pass

    @abstractmethod
    def toolbar_options_click(self, event=None):
        pass
