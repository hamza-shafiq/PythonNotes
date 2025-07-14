import os
from pyarabic.araby import tokenize, is_arabicword


def load_xtts():
    from torch.serialization import safe_globals
    from TTS.tts.configs.xtts_config import XttsConfig
    from TTS.tts.models.xtts import XttsAudioConfig, XttsArgs
    from TTS.config.shared_configs import BaseDatasetConfig
    from TTS.api import TTS

    with safe_globals([XttsConfig, XttsAudioConfig, BaseDatasetConfig, XttsArgs]):
        return TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2")


def image_generation(text, output_path="output_image.png"):
    from huggingface_hub import InferenceClient

    client = InferenceClient(
        provider="nebius",
        api_key=os.environ.get("HUGGINGFACE_API_KEY"),
    )

    # output is a PIL.Image object
    image = client.text_to_image(
        prompt=f"A cinematic illustration of the following Arabic story scene: “{text}”. "
               f"Ultra high detail, realistic lighting, dramatic composition, 4K resolution, "
               f"film-style depth, Arabian atmosphere, emotional storytelling frame",
        model="stabilityai/stable-diffusion-xl-base-1.0",
    )
    image.save(output_path)
    return output_path


def process_arabic_script(script):
    """Split Arabic script into sentences and filter non-Arabic."""
    sentences = []
    for line in script.split('\n'):
        if line.strip():
            tokens = tokenize(line)
            arabic_tokens = [t for t in tokens if is_arabicword(t)]
            sentences.append(' '.join(arabic_tokens))
    return [s for s in sentences if s]


def generate_arabic_audio(text, output_path="output_audio.wav"):
    """Generate Arabic speech using offline XTTS."""
    try:
        tts = load_xtts()
        tts.tts_to_file(
            text=text,
            speaker_wav="ar_speaker_sample.wav",  # Provide a 3-sec Arabic speaker reference
            language="ar",
            file_path=output_path
        )
        return output_path
    except Exception as e:
        print(f"Error generating audio: {e}")
        return None


def create_video(image_path, audio_path, video_output):
    from moviepy.editor import AudioFileClip, ImageClip

    audio = AudioFileClip(audio_path)
    image = ImageClip(image_path).set_duration(audio.duration)
    video = image.set_audio(audio)
    video.write_videofile(video_output, fps=24, audio_codec='aac')
    return video_output


if __name__ == "__main__":
    # Sample Arabic script
    arabic_script = """
    كان يا ما كان في قديم الزمان، كان هناك رجل يعيش في قرية صغيرة.
    أحب هذا الرجل السفر والمغامرة، فقرر أن يبحر عبر المحيط.
    """

    # # 1. Process script
    sentences = process_arabic_script(arabic_script)
    print(f"Processed Arabic sentences: {sentences}")

    # 2. Generate audio
    audio_file = generate_arabic_audio(sentences[0], "audio.wav")

    # 3. Generate image
    image_file = image_generation(sentences[0], "image.png")

    # 4. Generate video
    video_file = create_video(image_file, audio_file, "output.mp4")
    print(f"Video generated: {video_file}")
