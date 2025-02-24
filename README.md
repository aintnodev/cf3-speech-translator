# cf3-stt: An offline voice recognizer and translator

[![asciicast](https://asciinema.org/a/zujQ5GSLie2SwMQ0o4bXLHxNZ.svg)](https://asciinema.org/a/zujQ5GSLie2SwMQ0o4bXLHxNZ)

## Installation

Download [translate-en_hi-1_1.argosmodel](https://argos-net.com/v1/translate-en_hi-1_1.argosmodel) in `cf3-speech-translator/src` directory.

```sh
# clone the repository
git clone https://github.com/aintnodev/cf3-speech-translator.git
cd cf3-speech-translator

# create virtual environment
virtualenv -p 3.9 venv

# install dependencies
pip install -r requisrements.txt
```

Change directory to `cf3-speech-translator/src` as translation model is placed along with `record.py` and `record.py` is using relative path to load the model.

```sh
cd src
python record.py
```
