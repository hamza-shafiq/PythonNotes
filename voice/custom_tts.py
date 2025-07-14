import os
import json
from gtts import gTTS
from pydub import AudioSegment
# from pydub.playback import play
from pydub.silence import split_on_silence


class CustomTTS:
    def __init__(self):
        self.data = None
        self.silence_thresh = -50
        self.min_silence_len = 200

    def read_json(self, file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
        self.data = data
        return data

    @staticmethod
    def generate_speech(text, file_name):
        tts = gTTS(text, lang="en")
        tts.save(file_name)
        audio = AudioSegment.from_mp3(file_name)
        # play(audio)
        return audio

    def remove_silence(self, audio_segment):
        non_silent_chunks = split_on_silence(
            audio_segment,
            min_silence_len=self.min_silence_len,
            silence_thresh=self.silence_thresh,
            keep_silence=100
        )
        return sum(non_silent_chunks)

    @staticmethod
    def speed_adjust(audio_segment, target_duration):
        current_duration = len(audio_segment)
        speed_factor = round(current_duration/target_duration, 2)
        return audio_segment.speedup(playback_speed=speed_factor)

    def processing(self, output):
        combined = AudioSegment.empty()
        prev = 0

        for i, item in enumerate(self.data):
            text = item['text']
            start_time = item['start']
            end_time = item['end']
            target_duration = round((end_time - start_time) * 1000, 2)  # duration in milliseconds
            temp_file = f"temp_{i}.mp3"
            duration = round((start_time - prev) * 1000, 2)

            speech = self.generate_speech(text, temp_file)
            silent_text = AudioSegment.silent(duration)
            if len(speech) > target_duration:
                speech = self.speed_adjust(speech, target_duration)

            combined += speech
            combined += silent_text
            prev = end_time
            os.remove(temp_file)

        combined.export(output, format="mp3")


if __name__ == "__main__":
    json_file = "sentence.json"  # Path to your JSON data file
    output_file = "output_new.mp3"    # Path to the output MP3 file

    _obj = CustomTTS()
    _obj.read_json(json_file)
    _obj.processing(output_file)
