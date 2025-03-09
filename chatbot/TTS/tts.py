import nemo.collections.tts as nemo_tts
import numpy as np
import soundfile as sf
import sounddevice as sd
import torch
import warnings
from utils import split_text_into_fragments
warnings.filterwarnings("ignore")

device = torch.device("cpu")

def prepare_tts():
    spec_generator = nemo_tts.models.FastPitchModel.from_pretrained("tts_en_fastpitch")
    vocoder = nemo_tts.models.HifiGanModel.from_pretrained(model_name="tts_en_hifigan")
    spec_generator.to(device)
    vocoder.to(device)
    return spec_generator, vocoder

def text_to_speech(spec_generator, vocoder, text, samplerate=22050, savefile=False, device="cpu"):
    device = torch.device(device)
    spec_generator.to(device)
    vocoder.to(device)
    import time
    start = time.time()
    text = text.replace("*", "")
    texts = split_text_into_fragments(text, 250)
    all_audio = []
    for txt in texts:
        parsed = spec_generator.parse(txt)
        spectrogram = spec_generator.generate_spectrogram(tokens=parsed)
        audio = vocoder.convert_spectrogram_to_audio(spec=spectrogram)
        all_audio.append(np.ravel(audio.to('cpu').detach().numpy()))
    large_audio = np.concatenate(all_audio)
    print("Playing audio...")

    sd.play(large_audio , samplerate)
    sd.wait()
    print("Playing audio successfully...")
    if savefile:
        sf.write(file='speech.wav', data=np.ravel(audio.to('cpu').detach().numpy()), samplerate=samplerate)
        print("Save audio successfully...")

if __name__ == "__main__":
    text = "This means that some of words will remain unchanged if they are not handled by any of the rules in self.parse_one_word(). This may be intended if phonemes and chars are both valid inputs, otherwise, you may see unexpected deletions in your input."
    text = text + text + text
    print(len(text))
    spec_generator, vocoder = prepare_tts()
    text_to_speech(spec_generator, vocoder, text, samplerate=22050, savefile=False)
