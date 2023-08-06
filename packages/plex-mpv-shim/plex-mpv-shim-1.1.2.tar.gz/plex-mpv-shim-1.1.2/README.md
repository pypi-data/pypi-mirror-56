# Plex MPV Shim

Plex MPV Shim is a simple and lightweight Plex client. It supports Windows and
Linux and is easy to install. The project offers an experience similar to
Chromecast, but with direct play and subtitle support. The application requires
another app to play content and does not save login information, making it
ideal for applications where security is a concern. This project is
significantly smaller and less complicated than Plex Media Player, and is
written entirely in open-source Python.

The project supports the following:
 - Direct play of HEVC mkv files with subtitles.
 - Switching of subtitles and audio tracks.
 - Casting videos from the iOS mobile app and web app.
 - Seeking within a video using the seek bar and buttons.
 - Play, pause, and stop.
 - Using the built-in MPV controls. (OSD and keyboard shortcuts.)
 - Configuration of mpv via mpv.conf.
 - Connecting to shared servers.
 - Installing the package system-wide.
 - Skipping between videos.
 - Autoplaying the next video. (Can be disabled.)
 - Extra keyboard shortcuts: < > skip, u unwatched/stop, w watched/next
 - Playing multiple videos in a queue.
 - The app doesn't require or save any Plex passwords or tokens.
 - Executing commands before playing, after media end, and when stopped.
 - Configurable transcoding support based on remote server and bitrate.
 - The application shows up in Plex dashboard and usage tracking.

Transcoding is supported, but needs work:
 - Transcode bandwidth decisions are currently based on values in the config file.
 - Playback of videos can fail on remote servers if the available bandwidth is lower. 
 - Changing subtitle/audio tracks cannot be done after starting transcode playback.
 - The only way to control transcode video quality is using the config file.

You'll need [libmpv1](https://github.com/Kagami/mpv.js/blob/master/README.md#get-libmpv). To install `plex-mpv-shim`, run:
```bash
sudo pip3 install --upgrade plex-mpv-shim
```

The current Debian package for `libmpv1` doesn't support the on-screen controller. If you'd like this, or need codecs that aren't packaged with Debian, you need to build mpv from source. Execute the following:
```bash
sudo apt install autoconf automake libtool libharfbuzz-dev libfreetype6-dev libfontconfig1-dev libx11-dev libxrandr-dev libvdpau-dev libva-dev mesa-common-dev libegl1-mesa-dev yasm libasound2-dev libpulse-dev libuchardet-dev zlib1g-dev libfribidi-dev git libgnutls28-dev libgl1-mesa-dev libsdl2-dev cmake wget python g++ libluajit-5.1-dev
git clone https://github.com/mpv-player/mpv-build.git
cd mpv-build
echo --enable-libmpv-shared > mpv_options
./rebuild -j4
sudo ./install
sudo ldconfig
```

After installing the project, you can run it with `plex-mpv-shim`.
If you'd like to run it without installing it, run `./run.py`.

Keyboard Shortcuts:
 - Standard MPV shortcuts.
 - < > to skip episodes
 - q to close player
 - w to mark watched and skip
 - u to mark unwatched and quit

You can execute shell commands on media state using the config file:
 - media\_ended\_cmd - When all media has played.
 - pre\_media\_cmd - Before the player displays. (Will wait for finish.)
 - stop\_cmd - After stopping the player.
 - idle\_cmd - After no activity for idle\_cmd\_delay seconds.

This project is based on https://github.com/wnielson/omplex, which
is available under the terms of the MIT License. The project was ported
to python3, modified to use mpv as the player, and updated to allow all
features of the remote control api for video playback.

UPDATE: It looks like we have a reversal on the Plex Media Player situation.
That being said, this project has proven to be interesting as a hackable
Plex client. **I plan to maintain this client, although I may not work on
adding new features unless someone requests them.**

## Building on Windows

There is a prebuilt version for Windows in the releases section. When
following these directions, please take care to ensure both the python
and libmpv libraries are either 64 or 32 bit. (Don't mismatch them.)

1. Install [Python3](https://www.python.org/downloads/) with PATH enabled. Install [7zip](https://ninite.com/7zip/).
2. After installing python3, open `cmd` as admin and run `pip install pyinstaller python-mpv requests`.
3. Download [libmpv](https://sourceforge.net/projects/mpv-player-windows/files/libmpv/).
4. Extract the `mpv-1.dll` from the file and move it to the `plex-mpv-shim` folder.
5. Open a regular `cmd` prompt. Navigate to the `plex-mpv-shim` folder.
6. Run `pyinstaller -cF --add-binary "mpv-1.dll;." --icon media.ico run.py`.


