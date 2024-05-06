import mido
from mido import MidiFile, MidiTrack, Message
from IPython.display import display, Audio
import subprocess

def note_name_to_number(note_name):
    note_dict = {
        'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5,
        'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11
    }
    if note_name[:-1] in note_dict:
        return note_dict[note_name[:-1]] + (int(note_name[-1]) + 1) * 12
    else:
        raise ValueError(f"Invalid note name: {note_name}")

def get_user_input():
    notes_and_durations_str = input("Enter the notes and durations for bass (e.g., C4 1 D4 1 E4 2): ")
    input_list = notes_and_durations_str.split()
    if len(input_list) % 2 != 0:
        raise ValueError("Invalid input format. Each note should be followed by a duration.")
    return list(zip(input_list[::2], input_list[1::2]))

def create_midi_file(notes_and_durations):
    # Create a new MIDI file and track
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    # Set MIDI Tempo (100 beats per minute)
    track.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(100)))

    # Set the instrument to Acoustic Bass (instrument number 32)
    track.append(Message('program_change', program=32, time=0))

    ticks_per_beat = mid.ticks_per_beat  # Default is usually 480

    for note_name, duration in notes_and_durations:
        note_number = note_name_to_number(note_name)
        duration_in_ticks = int(duration) * ticks_per_beat

        # Add NOTE ON and NOTE OFF events
        track.append(Message('note_on', note=note_number, velocity=64, time=0))
        track.append(Message('note_off', note=note_number, velocity=64, time=duration_in_ticks))

    # Save to a MIDI file
    mid.save('output_bass.mid')

def convert_and_play_wav():
    # Convert the MIDI file to WAV using Timidity
    subprocess.run(['timidity', '-Ow', '-o', 'out_bass.wav', 'output_bass.mid'])

    # Play the WAV file in Colab
    audio = Audio('out_bass.wav')
    display(audio)

def main():
    notes_and_durations = get_user_input()
    create_midi_file(notes_and_durations)
    convert_and_play_wav()

if __name__ == "__main__":
    main()
