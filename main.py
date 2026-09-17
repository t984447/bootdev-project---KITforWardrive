import base.static_variables
from base.kitBaseSetup import setlogger, loadset
from base.kismetFetch import *
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
kismetHost = kistmetDataFetch(kitSettings["kismethost"]["hosturl"], kitSettings["kismethost"]["apitokenadmin"])

## Visual
class DEVICEFEED(Static):
    ## To be window that fill with device information.
    pass

class MAINWINDOW(Static):
    """början"""
    def compose(self):
        yield DEVICEFEED()

class KitApp(App):
    BINDINGS = [
        ("d", "toggle_dark_mode", "Toggle dark mode"),
        ("q", "exit_kit", "Exit KIT"),
    ] # End bindings
    CSS_PATH = "basecss.tcss"


    def compose(self):
        ## What is this app initally composed of
        self.title = "Kistmet in terminal"
        yield Horizontal(
                Static(id="devicefeed"),
                Static(id="messagefeed"),
        )
        yield Header(show_clock=True)
        yield Footer()
        yield MAINWINDOW()
    
    def action_toggle_dark_mode(self):
        self.theme = "textual-dark" if self.theme == "textual-light" else "textual-light"
        kitLogger.info("Toggled darkmode")

    def action_exit_kit(self):
        sys.exit()


def main():
    kitLogger.debug(f"LET GO, its {datetime.datetime.now()}")

    #kismetHost.printDataSources()
    #kismetHost.printDevicesXSeconds()
    #kismetHost.printDataSourcesSeen()


    #KitApp().run()



if __name__ == "__main__":
    main()