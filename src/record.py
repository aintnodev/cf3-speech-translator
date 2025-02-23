import sounddevice as sd
import numpy as np
from pydub import AudioSegment
import sys

import noisereduce as nr
from scipy.io import wavfile

import whisper

import pathlib
import argostranslate.package
import argostranslate.translate


class colors:
    reset = "\033[0m"
    bold = "\033[01m"
    red = "\033[31m"
    green = "\033[32m"
    blue = "\033[34m"
    yellow = "\033[93m"


class audio:
    def __init__(
        self,
        sample_rate=44100,
        channel=1,
        model="small",
    ):
        self.sample_rate = sample_rate
        self.channel = channel
        self.model = model

    def record_voice(self):
        print(f"{colors.yellow}{colors.bold}:: Recording...{colors.red}")
        audio_chunks = []

        try:
            while True:
                chunk = sd.rec(
                    int(self.sample_rate * 1),
                    samplerate=self.sample_rate,
                    channels=self.channel,
                    dtype="int16",
                )
                sd.wait()
                audio_chunks.append(chunk)
        except KeyboardInterrupt:
            print(f"\n{colors.reset}{colors.green}✓ Recording complete.")

        audio_data = np.concatenate(audio_chunks, axis=0)

        audio_segment = AudioSegment(
            audio_data.tobytes(),
            frame_rate=self.sample_rate,
            sample_width=audio_data.dtype.itemsize,
            channels=self.channel,
        )

        audio_segment.export("output.wav", format="wav")

    def reduce_noise(self):
        print(f"{colors.bold}{colors.yellow}:: Reducing noise...")
        rate, data = wavfile.read("output.wav")
        reduced_noise = nr.reduce_noise(y=data, sr=rate, stationary=False, n_jobs=-1)
        wavfile.write("output_reduced_noise.wav", rate, reduced_noise)
        print(f"{colors.reset}{colors.green}✓ Voice reduction complete")

    def transcribe_voice(self):
        print(f"{colors.bold}{colors.yellow}:: Started transcribing...")
        model = whisper.load_model(self.model)

        audio = whisper.load_audio("output_reduced_noise.wav")
        audio = whisper.pad_or_trim(audio)

        mel = whisper.log_mel_spectrogram(audio, n_mels=model.dims.n_mels).to(
            model.device
        )
        _, probs = model.detect_language(mel)

        detected_language = max(probs, key=probs.get)
        print(f"{colors.reset}{colors.green}✓ Text transcribed")
        print(
            f"{colors.reset}{colors.green}  Detected language:{colors.reset} {detected_language}"
        )

        if detected_language != "en":
            options = whisper.DecodingOptions(
                task="translate", without_timestamps=True, fp16=False
            )
            self.from_code = "en"
            self.to_code = "hi"
            self.package_version = "1.1"
        else:
            options = whisper.DecodingOptions(
                task="transcribe", without_timestamps=True, fp16=False
            )
            self.from_code = detected_language
            self.to_code = "hi"
            self.package_version = "1.1"
        self.result = whisper.decode(model, mel, options)
        print(
            f"{colors.reset}{colors.green}  Detected text:{colors.reset} {self.result.text}"
        )

    def translate_text(self):
        print(f"{colors.bold}{colors.yellow}:: Started translating...")
        package_version = self.package_version.replace(".", "_")
        package_path = pathlib.Path(
            f"./translate-{self.from_code}_{self.to_code}-{package_version}.argosmodel"
        )
        argostranslate.package.install_from_path(package_path)

        translatedText = argostranslate.translate.translate(
            self.result.text, self.from_code, self.to_code
        )
        print(f"{colors.reset}{colors.green}✓ Translation complete")
        print(f"{colors.reset}{colors.green}  Translated text: {translatedText}")


if __name__ == "__main__":
    new_audio = audio()
    new_audio.record_voice()
    new_audio.reduce_noise()
    new_audio.transcribe_voice()
    new_audio.translate_text()
