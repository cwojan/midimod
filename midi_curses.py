## Script to create curses TUI for receiving MIDI signals and displaying them to the user

## First import required packages
import curses
import mido
import rtmidi
import time

def main(stdscr):
    ## Get lists of MIDI inputs and outputs
    midi_inputs = mido.get_input_names()
    midi_outputs = mido.get_output_names()

    ## Clear screen
    stdscr.clear()

    ## If no MIDI inputs detected, allow for clean quitting
    try:
        temp = 1/len(midi_inputs)
    except:
        stdscr.addstr("Howdy! No MIDI devices detected. Press any key to quit.\n")
        stdscr.refresh()
        stdscr.getch()
        return

    ## Ask for MIDI input selection
    stdscr.addstr("Howdy! Choose your MIDI input:\n")
    for i, item in enumerate(midi_inputs):
        stdscr.addstr(f"{i+1}.) {item}\n")
    stdscr.refresh()

    ## Receive selection
    input_selection = stdscr.getkey().strip()
    try:
        input_index = int(input_selection) - 1
        input_port = mido.open_input(midi_inputs[input_index])  # Open MIDI input
    except (ValueError, IndexError):
        stdscr.addstr("Invalid input! Press any key to exit.\n")
        stdscr.refresh()
        stdscr.getch()
        return  # Exit if invalid selection

    ## Ask for MIDI output selection
    stdscr.addstr("\nNow choose your MIDI output:\n")
    for i, item in enumerate(midi_outputs):
        stdscr.addstr(f"{i+1}.) {item}\n")
    stdscr.refresh()

    output_selection = stdscr.getkey().strip()
    try:
        output_index = int(output_selection) - 1
        output_port = mido.open_output(midi_outputs[output_index])  # Open MIDI output
    except (ValueError, IndexError):
        stdscr.addstr("Invalid output! Press any key to exit.\n")
        stdscr.refresh()
        stdscr.getch()
        return

    ## MIDI processing loop
    held_keys = set()  # Keep track of held keys
    arp = 1 # set default arpeggiating method
    # Define the arpeggiation methods in a dictionary
    arp_methods = {
            1: lambda: sorted(held_keys), # Ascend
            2: lambda: sorted(held_keys, reverse=True), # Descend
            3: lambda: sorted(held_keys) + sorted(held_keys, reverse=True)[1:-1] # Ascend-Descend
        }
    # define text of arp methods
    arp_options = [
        "1.) Ascend",
        "2.) Descend", 
        "3.) Ascend-Descend"
        ]
    # set tempo and note length
    tempo = 60
    note_length = 0.05

    while True:
        stdscr.clear()
        stdscr.addstr("Now listening for MIDI signals...\n")

        ## Read MIDI input
        for msg in input_port.iter_pending():  # Check for new MIDI messages
            if msg.type == 'note_on' and msg.velocity > 0:
                held_keys.add(msg.note)  # Store pressed key
            elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                if msg.note in held_keys:
                    held_keys.discard(msg.note)  # Remove released key

        ## Display held keys
        stdscr.addstr("\nHeld Notes: " + ", ".join(map(str, sorted(held_keys))) + "\n")

        # Get the corresponding arpeggio output based on the current arp value
        arp_out = arp_methods.get(arp, lambda: [])()  # Default to empty list if arp is not found

        # Display the outgoing arpeggio sequence
        stdscr.addstr("Outgoing arpeggio: " + ", ".join(map(str, arp_out)) + " (repeat).\n")

        # Set sleep times for tempo and note length
        total_sleep = 15 / tempo  
        tempo_sleep = total_sleep - note_length

        ## Simulate arpeggiation (for now, just send notes back out)
        for note in arp_out:
           output_port.send(mido.Message('note_on', note=note, velocity=64))
           time.sleep(note_length) # Note duration
           output_port.send(mido.Message('note_off', note=note))
           time.sleep(tempo_sleep) # Delay between notes

        ## Display user options
        stdscr.addstr("\nPress a number to change arpeggio mode, +/- to change tempo, [/] to change note length, or 'q' to quit.\n")
        stdscr.addstr(f"Currently, Arpeggio: {arp_options[arp-1]}; Tempo: {tempo}; Note Length: {note_length}\n")
        stdscr.addstr("Arpeggio options: " + "; ".join(arp_options) + "\n")
        


        # Number keys' ASCII values: '1' = 49, '2' = 50, '3' = 51
        modes = {49, 50, 51}  # Set of ASCII values for '1', '2', '3'

        ## Check for user key press
        stdscr.nodelay(True)  # Make getch() non-blocking
        key = stdscr.getch()
        if key == ord('q'):
            break  # Exit loop if 'q' is pressed
        elif key in modes:
            arp = key - 48
        elif key == ord('='):
            tempo = min(240, tempo + 1)  # Prevent excessive tempo
        elif key == ord('-'):
            tempo = max(30, tempo - 1)  # Prevent too-slow tempo
        elif key == ord(']'):
            note_length = min(1.0, note_length + 0.01)  # Cap note length
        elif key == ord('['):
            note_length = max(0.01, note_length - 0.01)  # Prevent too-short notes


        ## Refresh display
        stdscr.refresh()
        if len(held_keys) == 0:
            time.sleep(0.1)  # Prevent excessive CPU usage

## Run the TUI
curses.wrapper(main)
