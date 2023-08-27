from abc import ABC, abstractmethod


class Commands(ABC):
    @abstractmethod
    def menu_file_quit_click(self, event=None): pass

    @abstractmethod
    def menu_service_catalog_click(self, event=None): pass

    @abstractmethod
    def menu_service_options_click(self, event=None): pass

    @abstractmethod
    def menu_help_faq_click(self, event=None): pass

    @abstractmethod
    def menu_help_updates_click(self, event=None): pass

    @abstractmethod
    def menu_help_about_click(self, event=None): pass
