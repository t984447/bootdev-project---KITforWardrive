# KIT, as in Kismet in terminal
## _a boot.dev project_
As a part for most of [Bood.dev's](https://www.boot.dev/u/gunilla) learningplans there is a course to make your own project. Ive thus decided to 
make a terminal based UI for kismet that simple pulls information from kismet. This can be useful for low end devices with small screens, like uConsole, where a webbrowser is overboard.

(!) While I am doing this for learning Python I am using AI as an guidance for certain parts like Textual (since their YT tuts are a tab bit out of date.)

## Features
- Simple UI whith little actual data on screen. 
- show last devices heard
- show last X message from feed
- configure via config file

## How to use
This UI was intended for use on a uConsole but can be used on other devices also
and has mainly been tested on Ubuntu and Debian devices through terminals.
This works using the [kismet API](https://www.kismet-wifi.net/docs/api/) over TCPIP which means it can be used by
other devices in the network.

At this current time you wont find any executable and as such requires Python with UV.
Clone the git yo a localtion you desire, for example ~/git/ and navigate into the folder.

1. create your virtual environment
```bash
uv venv kitapp
```
2.  and download the reuired modules
```bash
uv pip install -r requirements.txt
```
3. Make a copy of *settings-example.ini* to modify if desired.
```bash
cp settings_example.ini settings.ini
```

4. start kismet and login, you need to navigate to *settings* and create an API token to use.
Read permissions are enough. 

5. Copy the token and copy it to *settings-example.ini* where you replace the XXXX's with the token.
```ini
apitoken = XXXXXXXXXXXXXXXXXXXXXX
```
### Planned todo and plus features
- Compile to an executable.
- Run through the code and add loggers where needed.
- Might need to tweak the screen space as the header is creating an emptyness.

#### and if I have time:
- trigger a sound for each new find
- add menu for interactive costumatization
