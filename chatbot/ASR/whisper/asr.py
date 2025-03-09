import speech_recognition as sr
from transformers import WhisperProcessor, WhisperForConditionalGeneration
import numpy as np
import audioop
import warnings
import time
import torch
warnings.filterwarnings("ignore")

device = torch.device("cpu")

def prepare_asr():
    recognizer = sr.Recognizer()
    processor = WhisperProcessor.from_pretrained("chatbot/ASR/whisper/checkpoints_turbo/whisper-large-v3-turbo")
    model = WhisperForConditionalGeneration.from_pretrained("chatbot/ASR/whisper/checkpoints_turbo/whisper-large-v3-turbo")
    model.to(device)
    return recognizer, processor, model

def save_from_micro(path, recognizer):
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        with open(path, "wb") as f:
            f.write(audio.get_wav_data())


# Define a function to convert speech to text
def speech_to_text(recognizer, processor, model, micro=True, path=None, printout=False):
    if micro==True:
        with sr.Microphone() as source:

            print("Listening...")
            audio = recognizer.listen(source)
            print("Listening successfully...")
            start_time_asr = time.time()
            audio_frame_data = audioop.ratecv(audio.frame_data, 2, 1, 48000, 16000, None)[0]
            audio_nparray = np.frombuffer(audio_frame_data, dtype=np.int16).flatten()
            audio_as_np_float32 = audio_nparray.astype(np.float32)
            max_int16 = 2**15
            audio_normalised = audio_as_np_float32 / max_int16
        try:
            input_features = processor(audio_normalised, sampling_rate=16000, return_tensors="pt")
            input_features = input_features.input_features
            input_features = input_features.to(device)
            predicted_ids = model.generate(input_features)
            # skip_special_tokens = False
            transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)  # Using Google's speech recognition
            result = transcription[0]
            print("User: "+result)
            end_time_asr = time.time()
            print("Time ASR: " + str(end_time_asr - start_time_asr))
        except sr.UnknownValueError:
            print("Sorry, could not understand audio.")
        except sr.RequestError as e:
            print("Error fetching results; {0}".format(e))
    
    elif path != None:
        print("Read wav file...")
        
        with open(path, 'rb') as f:
            new_audio = f.read()
        print("Read wav successfully...")
        start_time_asr = time.time()
        audio_frame_data = audioop.ratecv(new_audio, 2, 1, 48000, 16000, None)[0]
        audio_nparray = np.frombuffer(audio_frame_data, dtype=np.int16).flatten()
        audio_as_np_float32 = audio_nparray.astype(np.float32)
        max_int16 = 2**15
        audio_normalised = audio_as_np_float32 / max_int16
        try:
            input_features = processor(audio_normalised, sampling_rate=16000, return_tensors="pt")
            input_features = input_features.input_features
            input_features = input_features.to(device)
            predicted_ids = model.generate(input_features, language='en')
            transcription = processor.batch_decode(predicted_ids, skip_special_tokens=False)
            # skip_special_tokens = False
            transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)  # Using Google's speech recognition
            result = transcription[0]
            print("User: "+result)
            end_time_asr = time.time()
            print("Time ASR: " + str(end_time_asr - start_time_asr))
        except sr.UnknownValueError:
            print("Sorry, could not understand audio.")
        except sr.RequestError as e:
            print("Error fetching results; {0}".format(e))
    else:
        result = input("User: ")
    return result

if __name__=='__main__':
    recognizer, processor, model = prepare_asr()
    text = speech_to_text(recognizer, processor, model, micro=False, path="speech.wav")
