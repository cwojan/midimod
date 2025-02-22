## Script to create curses TUI for receiving MIDI signals and displaying them to the user

## First import required packages
import curses
import mido
import rtmidi
import time

## set up initial curses screen with a "main function" to be given to wrapper()
def main(stdscr):
    ## get lists of midi inputs and ouputs
    midi_inputs = mido.get_input_names()
    midi_outputs = mido.get_output_names()

    ## clear screen
    stdscr.clear()

    ## Ask for midi input selection
    stdscr.addstr("Howdy! Choose your MIDI input:\n")
    ## Print each MIDI input name
    for i, item in enumerate(midi_inputs):
        stdscr.addstr(f"{i+1}.) {item}\n")
    ## push text to screen    
    stdscr.refresh()
    ## receive selection
    input_selection = stdscr.getkey().strip()  # Remove any surrounding whitespace
    try:
        input_index = int(input_selection) - 1  # Convert to 0-based index
    except ValueError:
        stdscr.addstr("Invalid input! Please enter a number.\n")
    ## check selection
    stdscr.addstr(f"You selected this MIDI input: {int(input_selection)}.) {midi_inputs[input_index]}\n")

    ## ask for output selection
    stdscr.addstr("Now choose your MIDI output:\n")
    ## Print each MIDI output name
    for i, item in enumerate(midi_outputs):
        stdscr.addstr(f"{i+1}.) {item}\n")
    ## push text to screen    
    stdscr.refresh()
    ## receive selection
    output_selection = stdscr.getkey().strip()  # Remove any surrounding whitespace
    try:
        output_index = int(output_selection) - 1  # Convert to 0-based index
    except ValueError:
        stdscr.addstr("Invalid input! Please enter a number.\n")
    ## check selection
    stdscr.addstr(f"You selected this MIDI output: {int(output_selection)}.) {midi_inputs[output_index]}\n")

    ## start listening
    stdscr.addstr("Now listening for signals...\n")
    ## here is where held keys will be displayed
    ## then display of the repeating sequence sent to MIDI out
    ## and a menu for selecting arpeggio style with number keys
    stdscr.refresh()
    stdscr.getch()

## call curses.wrapper with main function
curses.wrapper(main)
