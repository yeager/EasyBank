"""GTK4 Application entry point for EasyBank."""

import sys

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Adw, Gio

from easybank import __app_id__
from easybank.window import EasyBankWindow


class EasyBankApp(Adw.Application):
    """Main application class."""

    def __init__(self):
        super().__init__(
            application_id=__app_id__,
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
        )

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = EasyBankWindow(application=self)
        win.present()


def main():
    app = EasyBankApp()
    return app.run(sys.argv)
