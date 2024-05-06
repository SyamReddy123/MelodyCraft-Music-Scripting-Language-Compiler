from midiutil import MIDIFile
import subprocess

def generate_midi_file(instrument, notes, output_file="output.mid"):
    midi = MIDIFile(1)
    midi.addProgramChange(0, 0, 0, instrument)

    for time, note, duration in notes:
        midi.addNote(0, 0, note, time, duration, 100)

    with open(output_file, "wb") as midi_file:
        midi.writeFile(midi_file)

def play_midi_file(midi_file):
    subprocess.call(["fluidsynth", "-a", "alsa", "-m", "alsa_seq", "/usr/share/sounds/sf2/FluidR3_GM.sf2", midi_file])

def get_user_input():
    instrument = input("Enter the instrument name (piano/trumpet): ").lower()
    keys_input = input("Enter the keys to play (e.g., C D E): ").upper()
    keys = keys_input.split()
    return instrument, keys

def main():
    instrument, keys = get_user_input()

    # Map instrument names to MIDI program numbers
    instrument_mapping = {"piano": 0, "trumpet": 56}

    if instrument in instrument_mapping:
        instrument_number = instrument_mapping[instrument]
        notes_to_play = [(i, 60 + i, ) for i in range(len(keys))]  # Generating notes for keys
        generate_midi_file(instrument_number, notes_to_play)
        play_midi_file("output.mid")
    else:
        print("Invalid instrument name. Supported instruments: piano, trumpet")

if __name__ == "__main__":
    main()
