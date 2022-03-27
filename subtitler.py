#!/usr/bin/env python3
#Adapted from Vosk test_microphone.py
import argparse
import os
#vosk imports
import queue
import sounddevice as sd
import vosk
import sys
#oled imports
from oled.device import ssd1306, sh1106
from oled.render import canvas
from PIL import ImageFont

font = ImageFont.load_default()
oled = sh1106(port=1, address=0x3C)

q = queue.Queue()
#startup display
with canvas(oled) as draw:
    draw.text((0, 0), " Subtitler 0.1.0",  font=font, fill=255)

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    '-f', '--filename', type=str, metavar='FILENAME',
    help='audio file to store recording to')
parser.add_argument(
    '-m', '--model', type=str, metavar='MODEL_PATH',
    help='Path to the model')
parser.add_argument(
    '-d', '--device', type=int_or_str,
    help='input device (numeric ID or substring)')
parser.add_argument(
    '-r', '--samplerate', type=int, help='sampling rate')
args = parser.parse_args(remaining)

try:
    if args.model is None:
        args.model = "/root/model"
    if not os.path.exists(args.model):
        print ("Please download a model for your language from https://alphacephei.com/vosk/models")
        print ("and unpack as 'model' in the current folder.")
        parser.exit(0)
    if args.samplerate is None:
        device_info = sd.query_devices(args.device, 'input')
        # soundfile expects an int, sounddevice provides a float:
        args.samplerate = int(device_info['default_samplerate'])

    model = vosk.Model(args.model)

    if args.filename:
        dump_fn = open(args.filename, "wb")
    else:
        dump_fn = None
#higher blocksize needed to prevent inputoverflow
    with sd.RawInputStream(samplerate=args.samplerate, blocksize = 18000, device=args.device, dtype='int16',
                            channels=1, callback=callback):
            print('#' * 80)
            print('Press Ctrl+C to stop the recording')
            print('#' * 80)

            rec = vosk.KaldiRecognizer(model, args.samplerate)
            while True:
                data = q.get()
                if rec.AcceptWaveform(data):
                    rco = rec.Result()
                    count = 0
                    #display formatting
                    reducedOutput = ' ' + rco[14:-3]
                    out_text = '\n '.join(reducedOutput[i:i+19] for i in range(0,len(reducedOutput),19))
                    print(out_text)
                    #add i2c text print
                    try:
                        with canvas(oled) as draw:
                            draw.text((0, 0), out_text,  font=font, fill=255)
                    except OSError as e:
                        print(e)
                else:
                    print(rec.PartialResult())
                if dump_fn is not None:
                    dump_fn.write(data)

except KeyboardInterrupt:
    print('\nDone')
    parser.exit(0)
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))
