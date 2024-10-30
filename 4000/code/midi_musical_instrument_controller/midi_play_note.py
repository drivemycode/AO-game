import time

# import pygame.midi and initialize the midi module before you use it.
# pygame.midi is not a default pygame module so you need to import it,
# and also pygame.init does not init it for you.
import pygame.midi
pygame.midi.init()

# initialize the midi module before you use it.
#  pygame.init does not do this for you.
pygame.midi.init()

# print the devices and use the last output port.
for i in range(pygame.midi.get_count()):
    r = pygame.midi.get_device_info(i)
    (interf, name, is_input, is_output, is_opened) = r
    print (interf, name, is_input, is_output, is_opened)
    if is_output:
        last_port = i

# You could also use this to use the default port rather than the last one.
# default_port = pygame.midi.get_default_output_id()

midi_out = pygame.midi.Output(last_port, 0)

# select an instrument.
instrument = 19 # general midi church organ.
midi_out.set_instrument(instrument)

# play a note.
midi_out.note_on(note=62, velocity=127)
midi_out.note_off(note=62, velocity=0)

# sleep for a bit, and play another higher pitched note.
time.sleep(0.2)
midi_out.note_on(note=80, velocity=127)
midi_out.note_off(note=80, velocity=0)
time.sleep(0.2)

# play a note for longer.
midi_out.note_on(note=62, velocity=127)
time.sleep(0.8)
midi_out.note_off(note=62, velocity=0)
