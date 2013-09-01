SmartRoom
=========

This repo will contain the source code to run on the Raspberry Pi which will control Smartroom in Brooks and Greg's room, 2013-2014.

Note: It might not wind up being called Smartroom. It's a working title.

Dependencies
------------
Pianobar: A Pandora app that runs in the terminal.
    sudo apt-get install pianobar
    cp /usr/share/doc/pianobar/contrib/config-example ~/.config/pianobar
    vim ~/.config/pianobar
Edit the `tls\_fingerprint` to be:

    ```
    2D0AFDAFA16F4B5C0A43F3CB1D4752F9535507C0
    ```

Notes
-----
I did not make the PyTTS speech synthesizer; Robin David did. Thanks for being a pal, Robin David!
