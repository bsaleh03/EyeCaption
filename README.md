# CaptionIt
### v0.1.0
### Live subtitles for any situation
[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/DIHrooFKeLU/0.jpg)](https://www.youtube.com/watch?v=DIHrooFKeLU)
## Introduction
CaptionIt is a wearable offline heads up display designed to clip on to glasses' frames. It listens and displays what it hears on the HUD. For questions or to order a premade kit, reach out to me at bsaleh03+captionit@gmail.com
## Requirements
- A single board computer with an armv7 or above chip: This project is designed around the OrangePi Zero Two as it was the most readily available SBC but any raspberry pi (not zero) and other SBCs will work just fine instead. NOTE: This software will not work without GLIBC 2.27, ensure it is available on the linux distro you choose for your SBC or in your Docker environment
- An I2C Oled display: driving the HUD is a 0.96 inch, 128x64 px oled display
- Access to a 3d printer: To print the HUD mound. If one cannot be accessed, prints can be ordered from [Shapeways](https:shapeways.com) or with the whole kit from me. Alternatively a long piece of plastic is needed where the plastic and i2c display can be attached
- A USB microphone: An adapter may be needed depending on the SBCs USB interface. This is not required on SBCs with onboard microphones
- An SD card and a USB to SD adapter: For programming the SBC
- A USB powerbank: To power the SBC
- Two binder clips: To attach the HUD to glasses' frames
# Setup Instructions
## Software
- On Windows, use [Win32DiskImager](https://win32diskimager.org/) to install images on to your SD card. If you're using a raspberry pi, use their [install tool](https://www.raspberrypi.com/software/).
### If you are using an Orange Pi Zero 2, all you need to do is flash *captionit_0.1.0_ubuntu_focus_OPI_Z2.img* under project releases, to your sd card and you'll be good to go
- Otherwise, flash the appropriate image for your SBC onto your SD card
- Boot up the SBC and login to your device (usually through serial TTL or SSH). You will need to connect this device to the internet the first time to install the required packages. Run ```sudo apt-get update``` 
- Clone this repo on to the device
- Install the conda environment by using ```pip install -r requirements.txt```
- Prepare the voice recognition model:
```
wget https://alphacephei.com/kaldi/models/vosk-model-small-en-us-0.15.zip
unzip vosk-model-small-en-us-0.15.zip
mv vosk-model-small-en-us-0.15 model
```
- ### Only run these steps if you are on orange pi
  - Checkout branch *OrangePi*
  - cd into *OrangePi-OLED*
  - Run ```sudo python3 setup.py install``` to install the OLED package
- Run ```python3 captionit.py -l``` to see where the USB microphone is listed
- cd back into the repo and move *captionit.service* into ```/etc/systemd/system/```. Make sure to edit the service file to ensure the paths are correct and the correct microphone device is specified after -d. This will ensure the captionit script will run at startup every time. Once the service is moved, run ```sudo systemctl enable captionit```

Setup should be complete from SW side

## Hardware
- Cut the polystyrene plastic into a roughly 1.5x2.25 inch rectangle. To cut the plastic, mark the outline of your cut and use a sharp knife to score the surface repeatedly until it is thin enough to snap off. This process does produce dust so it is best to do this outdoors and with a mask.
- Print out *3d-models/HUD_mount_v3.stl*.
- Connect the pins on the OLED display to their respective ports on the SBC. If you are using the Orange Pi Zero Two, the ports are SDA:3, SCL:5, VCC:1, GND: 25
- Fit the I2C display and plastic screen into their positions on the mount. If it is not possible to print a mount, attach the display parallel to a long thin piece of plastic and attach the plastic screen at a 53 degree angle from the display.

Setup should be complete from HW side

# Usage
Once setup is complete, CaptionIt is easy to use, plug the microphone and power source into the SBC and attach the mount to your glasses' frames with the butterfly clips. Subtitles should automatically pop up in the HUD reflection as they are heard. Absolutely no internet connection is needed after initial setup, this setup is portable anywhere.

# Refrences
- https://alphacephei.com/vosk/
- https://github.com/karabek/OrangePi-OLED

# Contributing
Issues and pull requests are more than welcome. Feel free to reach out to me through email if youd like to request features.

## License
Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International Public License. In license file
