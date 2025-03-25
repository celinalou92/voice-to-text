import json
import os

def transcription_response(transcript_data, speaker_data):
    transcript_file = os.path.join('output/transcripts', 'transcript.json')
    summary_file_path = os.path.join('output/openai', 'summary.json')

    data_t = load_json(transcript_data)
    # data_s = load_json(speaker_data)
    data_summary = load_json(summary_file_path)


    labeled_transcription = []
    for seg_t in data_t:
        t_start = seg_t['start']
        t_end = seg_t['end']
        best_matching_speaker = None
        max_overlap = 0

        for seg_s in speaker_data:
            s_start = seg_s['start']
            s_end = seg_s['end']
            speaker = seg_s['speaker']

            overlap_start = max(t_start, s_start)
            overlap_end = min(t_end, s_end)
            overlap_duration = overlap_end - overlap_start

            if overlap_duration > 0 and overlap_duration > max_overlap:
                max_overlap = overlap_duration
                best_matching_speaker = speaker
    
        labeled_segment = {
            "start": t_start,
            "end": t_end,
            "text": seg_t["text"],
            "speaker": best_matching_speaker
        }
        labeled_transcription.append(labeled_segment)

    collapsed_transcription = []
    for segment in labeled_transcription:
        if not collapsed_transcription:
            collapsed_transcription.append(segment)
        else:
            last = collapsed_transcription[-1]
            if segment["speaker"] == last["speaker"]:
                last["end"] = segment["end"]
                last["text"] += " " + segment["text"]
            else:
                collapsed_transcription.append(segment)

    final_transcript = {
         "summary": data_summary,
         "segments": collapsed_transcription
    }

    with open(transcript_file, "w") as f:
            json.dump(final_transcript, f, indent=4)
    return transcript_file
    
def load_json(file_path):
    with open(file_path, "r") as f:
            return json.load(f)


