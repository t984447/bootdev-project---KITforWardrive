import base.static_variables

from textual.app import App
from textual.widgets import Footer, Header, Static

class DEVICEFEED():
    pass

class MAINWINDOW(Static):
    """börje"""
    def compose(self):
        yield DEVICEFEED()



class KitApp(App):
    BINDINGS = [
        ("d", "toggle_dark_mode", "Toggle dark mode")
    ]

    def compose(self):
        ## What is this app composed of
        self.title = "Kistmet in terminal"
        yield Header(show_clock=True)
        yield Footer()
        yield MAINWINDOW()
    
    def action_toggle_dark_mode(self):
        self.theme = "textual-dark" if self.theme == "textual-light" else "textual-light"



def main():
    KitApp().run()



if __name__ == "__main__":
    main()