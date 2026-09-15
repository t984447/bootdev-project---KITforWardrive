import base.static_variables
import sys
from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Footer, Header, Static

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

    def action_exit_kit(self):
        sys.exit()


def main():
    KitApp().run()



if __name__ == "__main__":
    main()