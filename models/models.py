class BaseSegment: 
    def __init__(self, start: float, end: float):
        self.start = start
        self.end = end
    
class WhisperSegment(BaseSegment):
    def __init__(self, start: float, end: float, text: str, id: int):
        super().__init__(start, end)
        self.text = text
        self.id = id


class TranscriptSegment(BaseSegment):
    def __init__(self, start: float, end: float, text: str, speaker: str):
        super().__init__(start, end)
        self.speaker = speaker
        self.text = text

class DiaritzationSegment(BaseSegment):
    def __init__(self, start: float, end: float, speaker: str):
        super().__init__(start, end)
        self.speaker = speaker

class Summary:
    def __init__(self, observations: str, **key_points: str):    
        self.observations = observations
        for key, value in key_points.items():
                setattr(self, key, value)

class Transcript:
    def __init__(self, summary: Summary, segments: list[TranscriptSegment]):
        self.summary = summary
        self.segments = segments