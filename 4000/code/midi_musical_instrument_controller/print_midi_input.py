# code/print_midi_input.py
import time
import pygame.midi

# initialize the midi module before you use it.
pygame.midi.init()

# print the devices
for i in range(pygame.midi.get_count()):
    r = pygame.midi.get_device_info(i)
    (interf, name, is_input, is_output, is_opened) = r
    print (interf, name, is_input, is_output, is_opened)

device_id = pygame.midi.get_default_input_id()

print('Using device id: %s' % device_id)
midi_in = pygame.midi.Input(device_id)
going = True
print ('Use ctrl+c to quit')
while going:
    midi_events = midi_in.read(20)
    if midi_events:
        print('midi events', midi_events)
        # make some pygame.Events to be used like other pygame events.
        print('pygame events', pygame.midi.midis2events(midi_events, device_id))
    time.sleep(0.1)
