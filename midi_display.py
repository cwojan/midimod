# import packages
import mido

import time

#save MIDI input name
midi_in = mido.get_input_names()

# Set to track currently held keys
held_keys = set()




#monitor midi signals
with mido.open_input(midi_in[0]) as inport:
    # display midi signals   
    for msg in inport: # only available messages
        #display only key presses
        if msg.velocity > 0:
            held_keys.add(msg.note)
        #clear console when key released
        elif msg.velocity == 0:
            held_keys.discard(msg.note)

        print(f"\r{' ' * 50}", end="") 
        print(f"\rHeld Keys: {sorted(held_keys)}", end="")

