This is the GUI for our Smart Mirror.

To run:
python3 startup/poweron.py

To run on startup on the Raspberry Pi add the following line to the rc.local file.
python3 startup/poweron.py




Global variables you need to set:
SPOTIPY_CLIENT_ID   - Spotify developer project ID
SPOTIPY_CLIENT_SECRET 
WEATHERAPI_TOKEN    - Weaterapi.com account token

Dependencies:
pip install spotipy --upgrade
pip3 install pytz
pip3 install python-dateutil