import re
from datetime import datetime
from music21 import stream, note, metadata, tempo, meter, key

def char_to_scale_degree(char, scale):
    print(char, ord(char.lower()) % len(scale), ord(char.lower()))
    return ord(char.lower()) % len(scale)

def char_to_duration(char, rhythm_pattern):
    ascii_val = ord(char)
    return rhythm_pattern[ascii_val % len(rhythm_pattern)]

def create_notes_from_text(text, scale, rhythm_pattern):
    notes_sequence = []
    for char in text:
        if char.isalpha():
            pitch = scale[char_to_scale_degree(char, scale)]
            duration = char_to_duration(char, rhythm_pattern)
            notes_sequence.append({'type': 'note', 'pitch': pitch, 'duration': duration})
        elif char.isspace():
            duration = char_to_duration(char, rhythm_pattern)
            notes_sequence.append({'type': 'rest', 'duration': duration})
    return notes_sequence

def create_music_stream(notes_sequence, key_signature, time_signature='4/4', bpm=120):
    score = stream.Score(id='mainScore')
    score.insert(0, metadata.Metadata())
    score.metadata.title = 'Algorithmic Composition'
    score.metadata.composer = 'Composer Name'

    part = stream.Part(id='part1')
    part.append(key.KeySignature(key_signature.sharps))
    part.append(meter.TimeSignature(time_signature))
    part.append(tempo.MetronomeMark(number=bpm))

    for note_info in notes_sequence:
        if note_info['type'] == 'note':
            n = note.Note(note_info['pitch'])
            n.duration.type = note_info['duration']
        elif note_info['type'] == 'rest':
            n = note.Rest()
            n.duration.type = note_info['duration']
        part.append(n)

    score.insert(0, part)
    return score

def save_music_xml(score, text, file_path=None):
    if not file_path:
        sanitized_text = re.sub(r'\W+', '', text)
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        #file_path = f'{sanitized_text}_{timestamp}.musicxml'
        file_path = f'{sanitized_text}_{timestamp}.xml'
    file_path = score.write('musicxml', fp=file_path)
    score.show('musicxml')
    print(f'MusicXML written to {file_path}')
    return file_path



def get_scale_from_key(key_obj):
    # Assuming key_obj is an instance of music21.key.Key
    return [str(p) for p in key_obj.pitches]

text = '''
Love's vast ocean, a realm where emotions soar
If words were notes, our love's the score,
The irresistible call of the siren, beckoning evermore
Seas torn asunder, the world from Moussa’s lore.

A heart set sail, without compass or oar
Waves and wind sang to rich and poor
Sirens silence along the shore,
Luring hearts to depths unknown.

A heart sets sail, guided by passion's core
If waves held stories, they'd be ones we’ve sung,
Sirens whisper tales from ancient lore,
Their silence deafening as the nilpotent tongue.

The sea, initially calm beneath the moon's glow
A sailor's tale of work and woe,
Yet within its depths, a storm begins to grow
Transformed by love's enduring glow.

Anticipation rises, a tempestuous flow
Should he resist, or should he bend,
A whirlwind fueled by longing for you, I know
To the maiden's call, where paths extend?

We race against time, the tide, to seize the day
He chose her love, the siren's spell,
The ship of love cannot forever in harbor stay
A harmony he knows so well.

Like rain, we cherish the moments, fleeting though they may be
No longer lost in ocean's foam,
The winds of time, never held at bay
In love and land, he's found his home.'''
#scale = ['C#', 'D#', 'E', 'F#', 'G#', 'A', 'B', 'C#']  # C# Major Scale
rhythm_pattern = ['16th', 'eighth', 'quarter', 'half', 'whole']  # More varied rhythm
key_signature = key.Key('c#')

scale = get_scale_from_key(key_signature)
print(scale)
time_signature = '3/4'
bpm = 100  # Beats per minute

notes_sequence = create_notes_from_text(text, scale, rhythm_pattern)
score = create_music_stream(notes_sequence, key_signature, time_signature, bpm)
named = 'output.xml'
save_music_xml(score, text, file_path=named)