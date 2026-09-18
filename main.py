import base.static_variables
from base.kitBaseSetup import setlogger, loadset
from base.kismetFetch import *
from base.kitTextual import *
import sys
import datetime
import logging
#import os
#import configparser
from pathlib import Path
from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Footer, Header, Static


## Setup settings and logger
kitSettings = loadset()
setlogger(kitSettings)
kitLogger = logging.getLogger(__name__)

## Setup kismet related objects
kismetHost = kistmetDataFetch(kitSettings["kismethost"]["hosturl"], kitSettings["kismethost"]["apitoken"])

## Visual


class KitApp(App):
    def __init__(self, kismet_host):
        super().__init__()
        self.kismet_host = kismet_host

    BINDINGS = [
        ("d", "toggle_dark_mode", "Toggle dark mode"),
        ("q", "exit_kit", "Exit KIT"),
        ("m", "open_menu", "Open the menu"),
    ] # End bindings

    CSS_PATH = "basecss.tcss"
    TITLE = "Kistmet in terminal"

    def compose(self):
        ## What is this app initally composed of
        #yield Header(show_clock=True)
        yield KismetHeader(kismet_host=self.kismet_host)
        yield Footer()
        yield MainWindow(kismet_host=self.kismet_host)
    
    def action_toggle_dark_mode(self):
        self.theme = "textual-dark" if self.theme == "textual-light" else "textual-light"
        kitLogger.info("Toggled darkmode")

    def action_exit_kit(self):
        sys.exit()

    def action_open_menu(self) -> None:
        #self.push_screen(MenuScreen())
        self.push_screen(MenuScreen(), callback=self.menu_result)
    
    def menu_result(self, result):
        print(result)


def main():
    kitLogger.debug(f"LET GO, its {datetime.datetime.now()}")
    kitAPP = KitApp(kismetHost)
    kitAPP.run()


if __name__ == "__main__":
    main()


    #kismetHost.printDataSources()
    #kismetHost.printWifiDevicesXSeconds()
    
    #for dev in kismetHost.listWifiDevicesXSeconds():
    #    print(dev)