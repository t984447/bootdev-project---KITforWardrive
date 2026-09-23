import base.static_variables
from base.kitBaseSetup import setlogger, loadset
from base.kismetFetch import kistmetDataFetch
from base.kitTextual import *
import sys
import datetime
from pathlib import Path
from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Footer, Header, Static


## Setup settings and logger
kitSettings = loadset()
setlogger(kitSettings)
kitLogger = logging.getLogger(__name__)

## Setup kismet related objects
kismetHost = kistmetDataFetch(kitSettings)

## Visual
class KitApp(App):
    def __init__(self, kismet_host):
        super().__init__()
        self.kismet_host = kismet_host
        self.messages_enabled = True

    BINDINGS = [
        ("d", "toggle_dark_mode", "Toggle dark mode"),
        ("q", "exit_kit", "Exit KIT"),
        ("m", "open_menu", "Open the menu"),
    ] # End bindings

    CSS_PATH = "basecss.tcss"
    TITLE = "Kistmet in terminal"

    def compose(self):
        ## What is this app initally composed of
        yield KismetHeader(kismet_host=self.kismet_host, updatefreq = kitSettings.getfloat('updatefrequency', 'headerupdate'))
        yield Footer()
        yield MainWindow(kismet_host=self.kismet_host, deviceUpdateFreq = kitSettings.getfloat('updatefrequency', 'devicefeed'), messageUpdateFreq = kitSettings.getfloat('updatefrequency', 'messagefeed'))
    
    def action_toggle_dark_mode(self):
        self.theme = "textual-dark" if self.theme == "textual-light" else "textual-light"
        kitLogger.info("Toggled darkmode")

    def action_exit_kit(self):
        sys.exit()

    def action_open_menu(self) -> None:
        self.push_screen(MenuScreen(), callback=self.menu_result)
    
    def menu_result(self, result):
        print(result)

    def toggle_messages(self):
        message_feed = self.query_one("#messagefeed", MessageFeed)
        device_feed = self.query_one("#devicefeed", DeviceFeed)

        if self.messages_enabled:
            message_feed.pause_updates()
            message_feed.display = False
            device_feed.styles.width = "100%"
            self.messages_enabled = False
        else:
            message_feed.display = True
            message_feed.resume_updates()
            device_feed.styles.width = "70%"
            self.messages_enabled = True


def main():
    kitLogger.debug(f"LET GO, its {datetime.datetime.now()}")
    kitAPP = KitApp(kismetHost)
    kitAPP.run()

if __name__ == "__main__":
    main()
