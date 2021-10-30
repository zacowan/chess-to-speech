# Chess Client

Pip install List:

pip install pygame

pip install python-chess

pip install requests

pip install pyaudio

If your having trouble with pyaudio, it is most likely because need to manually install the wheel, follow this to manually pip install pyaudio wheel
https://stackoverflow.com/a/55630212

## Zach's Notes

### Getting Started

1. I had to install `sdl2` via Homebrew on my Mac to get `pygame` to work.
2. I also needed to install `portaudio` via Homebrew on my Mac to get `pyaudio` to work.
3. To install the required packages, run `pipenv install` at the project root directory (`chess_client/`).
4. To run the client, run the command `pipenv run python -m client.the_main.py` at the project root directory.
