import os
from pydub import AudioSegment

def audio_to_wav(filepath):
    extracted_audio_file = os.path.join('output/conversion_wav', 'conversion.wav')
    try:
        audio = AudioSegment.from_file(filepath)
    except Exception as e:
        ext = os.path.splitext(filepath)[1].lower().lstrip('.')
        format_map = {'m4a': 'mp4', 'wma': 'asf'}
        format_hint = format_map.get(ext, ext)
        audio = AudioSegment.from_file(filepath, format=format_hint)
    
    audio_optimized = audio.set_frame_rate(16000).set_channels(1)
    # TODO: Keep eye on diaritization output loss of accuracy
    audio_optimized.export(extracted_audio_file, format="wav", 
                          parameters=["-acodec", "pcm_s16le"])
    return extracted_audio_file
    