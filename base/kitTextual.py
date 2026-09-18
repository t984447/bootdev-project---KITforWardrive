from textual.app import App, ComposeResult
from textual.screen import ModalScreen
from textual.containers import Horizontal
from textual.widgets import Footer, Header, OptionList, Static
from textual.widgets.option_list import Option
from base.kismetFetch import *
from base.kitBaseSetup import setlogger, loadset
import datetime

class MenuScreen(ModalScreen):

    def compose(self) -> ComposeResult:
        yield OptionList(
            Option("Networks"),
            Option("Devices"),
            Option("Settings"),
            Option("Exit KIT"),
            id="menu",
        )
    BINDINGS = [
        ("escape", "close_menu", "Close menu"),
    ]

    def on_option_list_option_selected(
        self,
        event: OptionList.OptionSelected,
    ) -> None:

        if event.option.prompt == "Exit KIT":
            self.app.exit()
        else:
            print(f"Selected: {event.option.prompt}")

            # Close the menu
            self.dismiss()

    def action_close_menu(self) -> None:
        self.dismiss()


class DeviceFeed(Static):
    """ To be window that fill with device information. """
    def __init__(self, kismet_host, **kwargs):
        super().__init__(**kwargs)
        self.kismet_host = kismet_host

    def on_mount(self):
        self.set_interval(1.0, self.update_devices)

    def update_devices(self):
        output = ""
        
        try:
            devices = self.kismet_host.listWifiDevicesXSeconds()
            output += (
                    f"{"name":<20} "
                    f"{"signal":>10} dBm  "    
                    f"{"mac":<17}  "
                    f"{"last seen"}\n"
                )
            for name, signal, mac, last_seen in devices:
                output += (
                    f"{name:<20} "
                    f"{signal:>10} dBm  "    
                    f"{mac:<17}  "
                    f"{last_seen}\n"
                )

        except Exception as e:
            output = f"{type(e).__name__}: {e}"

        self.update(output)

class KismetHeader(Horizontal):
    """ Instead of the included Textual header I am making my own to include the data points for seen Wifi and Bluetooth. """
    def __init__(self, kismet_host, **kwargs):
        super().__init__(**kwargs)
        self.kismet_host = kismet_host

    def compose(self) -> ComposeResult:
        yield Static("[Seen WiFi: 0]", id="wifi")
        yield Static("Kismet in Terminal", id="title")
        yield Static("[Seen Bluetooth: 0]", id="bluetooth")
        yield Static("15:42", id="clock")

    def update_header(self):

        try:
            DSinfo = self.kismet_host.listDataSources()
            DSwifiCount = DSinfo[0][2]
            DSbluetoothCount = DSinfo[1][2]

            self.query_one("#wifi", Static).update(
            f"[Seen WiFi: {DSwifiCount}]"
            )


            self.query_one("#bluetooth", Static).update(
                f"[Seen Bluetooth: {DSbluetoothCount}]"
            )

            current_time = datetime.datetime.now().strftime("%H:%M")

            self.query_one("#clock", Static).update(
                current_time
            )

        except Exception as e:
            print(f"{type(e).__name__}: {e}")

    def on_mount(self):
        self.set_interval(2.0, self.update_header)



class MainWindow(Horizontal):
    """ Main window contains two widets that will be split horizontally 70/30.
        One for device and one for messages. """
    def __init__(self, kismet_host):
        super().__init__()
        self.kismet_host = kismet_host

    def compose(self):
        yield DeviceFeed(
            kismet_host=self.kismet_host,
            id="devicefeed",
        )

        yield MessageFeed(
            id="messagefeed",
        )


class MessageFeed(Static):
    """ To be window that fill with message information. """
    pass