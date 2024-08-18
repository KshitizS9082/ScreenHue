# ScreenHue
Dynamic Screen Content Based Ambient Lighting for Smart Bulbs Using TinyTuya and Python

## Background
Ambilight is a feature built into Philips TVs that has enabled the company to build a strong fan base thanks to this technology. TVs with this feature integrate LED lights around the edges to project backlight into the room. These LED lights are synchronised with the content on the screen to enhance visual immersion and comfort.

Ambilight enhances visual immersion, reduces fatigue and personalises lighting for an exceptional entertainment experience.

These lights project colours and hues that match the image on the screen, creating ambient lighting that extends beyond the edges of the TV.

While buying a TV for this is an option, it might be a little heavy on some pockets. 

Smart bulbs have all the lights, they can be changed remotely using apps. Apps must be using some API internally. We might be able to ping those APIs.

Simple python script can capture our monitors screens, that's not an issue. We can process the image and get the appropriate color, that's not an issue. 

![If they can do it, so CAN we](https://i.pinimg.com/564x/4f/f0/92/4ff0922666a17a117220733bbbf0fba1.jpg)

A little googling, and I came across the word [Bias Lighting](https://en.wikipedia.org/wiki/Bias_lighting). In home cinema and video editing technology, bias lighting is a weak light source on the backside of a screen or monitor that illuminates the wall or surface behind and just around the display.

Usually smart apps use cloud based API to ping IOT devices. Issue with that is that introduces too much latency and especially in our usecase of regular pings, probablity of throttling the calls. Luckily there's a python package [TinyTuya](https://github.com/jasonacox/tinytuya)(Shoutout to [jasonacox](https://github.com/jasonacox)) that leverages the access to local area network tuya API. This solved our latency issue. This solves our latency and API call limits issues. 

For getting the ideal colour we use colorthief on the screen's image. 

While this works nice, there's scope of improvement.
1. [Hyperion](https://github.com/hyperion-project/hyperion.ng) is an opensource [Bias or Ambient Lighting](https://en.wikipedia.org/wiki/Bias_lighting).


## Installation
```bash
# Clone the repo
git clone "https://github.com/KshitizS9082/ScreenHue"
cd ScreenHue

# Setup virtual environment
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt

# Creating devices.json (follow TinyTuya Installation )
python -m tinytuya wizard

# Run script
python ScreenHue.py 

```

## About TinyTuya
This python module controls and reads state of [Tuya](https://en.tuya.com/) compatible WiFi Smart Devices (Plugs, Switches, Lights, Window Covers, etc.) using the local area network (LAN) or the cloud (TuyaCloud API).  This is a compatible replacement for the `pytuya` PyPI module and currently supports Tuya Protocols 3.1, 3.2, 3.3, 3.4 and 3.5.

[Tuya](https://en.tuya.com/) devices are designed to communicate with the TuyaCloud but most also expose a local area network API.  This allows us to directly control the devices without using the cloud. This python module provides a way to poll status and issue commands to these devices.

TinyTuya can also connect to the Tuya Cloud to poll status and issue commands to Tuya devices.

![TinyTuya Diagram](https://raw.githubusercontent.com/jasonacox/tinytuya/master/docs/TinyTuya-diagram.svg)


NOTE: Devices need to be **activated** by Smart Life App.

## TinyTuya Installation  

```bash
# Install TinyTuya Library
python -m pip install tinytuya

# Optional: Install Command Line Tool
pipx install tinytuya
```

Pip will attempt to install `cryptography`, `requests` and `colorama` if not already installed.

## Tuya Device Preparation

Controlling and monitoring Tuya devices on your network requires the following:
* *Address* - Network address (IPv4) of the device e.g. 10.0.1.100
* *Device ID* - Unique identifier for the Tuya device
* *Version* - Tuya protocol version used (3.1, 3.2, 3.3, 3.4 or 3.5)
* *Local_Key* - Security key needed to access the Tuya device. See [Setup Wizard](https://github.com/jasonacox/tinytuya#setup-wizard---getting-local-keys) to get these keys.

### Network Scanner

TinyTuya has a built in network scanner that can be used to find Tuya Devices on your local network. It will show *Address*, *Device ID* and *Version* for each device. Your LAN and firewall will need to allow UDP (6666, 6667 and 7000) and TCP (6668) traffic.

```bash
python -m tinytuya scan
```

### Setup Wizard - Getting Local Keys

TinyTuya has a built-in setup Wizard that uses the Tuya IoT Cloud Platform to generate a JSON list (devices.json) of all your registered devices, including secret *Local_Key* and *Name* of your devices. Follow the steps below:

1. PAIR - Download the *Smart Life App* or *Tuya Smart App*, available for [iPhone](https://itunes.apple.com/us/app/smart-life-smart-living/id1115101477?mt=8) or [Android](https://play.google.com/store/apps/details?id=com.tuya.smartlife&hl=en). Set up your SmartLife account and pair all of your Tuya devices (this is important as you cannot access a device that has not been paired).  Do not use a 'guest' account, otherwise it will get deleted without confirmation at step 3.

2. SCAN (Optional) - Run the TinyTuya scan to get a list of Tuya devices on your network. It will show device *Address*, *Device ID* and *Version* number (3.x):
    ```bash
    python -m tinytuya scan
    ```
    NOTE: You will need to use one of the displayed *Device IDs* for step 4.

3. TUYA ACCOUNT - Set up a Tuya Account (see [PDF Instructions](https://github.com/jasonacox/tinytuya/files/12836816/Tuya.IoT.API.Setup.v2.pdf)):
    * *NOTE: Tuya often changes their portal and services. Please open an [issue](https://github.com/jasonacox/tinytuya/issues) with screenshots if we need to update these instructions.*
    * Create a Tuya Developer account on [iot.tuya.com](https://iot.tuya.com/). When it asks for the "Account Type", select "Skip this step..." (see [screenshot](https://user-images.githubusercontent.com/836718/213877860-34c39851-5671-4c9f-b4d5-251873f18c77.png)).  
    * Click on "Cloud" icon -> "Create Cloud Project"
      1. Pick the correct Data Center "Region" for your location (check [HERE](https://developer.tuya.com/en/docs/iot/oem-app-data-center-distributed?id=Kafi0ku9l07qb#title-3-Western%20America%20Data%20Center) to find your Region).  This will be used by TinyTuya Wizard ([screenshot](https://user-images.githubusercontent.com/836718/138598647-c9657e49-1a89-4ed6-8105-ceee95d9513f.png)).
      2. Skip the configuration wizard but remember the Authorization Key: *API ID* and *Secret* for below ([screenshot](https://user-images.githubusercontent.com/836718/138598788-f74d2fe8-57fa-439c-8003-18735a44e7e5.png)).
    * Click on "Cloud" icon -> Select your project -> **Devices** -> **Link Tuya App Account** ([see screenshot](https://user-images.githubusercontent.com/836718/155827671-44d5fce4-0119-4d0e-a224-ef3715fafc24.png))
    * Click **Add App Account** ([screenshot](https://user-images.githubusercontent.com/836718/273364035-0fd133b7-4e9e-4a6d-900e-efe63d69f1a0.png)) and it will pop-up a "Link Tuya App Account" dialog, chose "Automatic" and "Read Only Status" (it will still alow commands). Click OK and it will display a QR code. Scan the QR code with the *Smart Life app* on your Phone (see step 1 above) by going to the "Me" tab in the *Smart Life app* and clicking on the QR code button `[..]` in the upper right hand corner of the app. When you scan the QR code, it will link all of the devices registered in your *Smart Life app* into your Tuya IoT project. If the QR code will not scan then make sure to disable any browser theming plug-ins (such as Dark Reader) and try again.
    * **NO DEVICES?** If no devices show up after scanning the QR code, you will need to select a different data center and edit your project (or create a new one) until you see your paired devices from the *Smart Life App* show up. ([screenshot](https://user-images.githubusercontent.com/35581194/148679597-391adecb-a271-453b-90c0-c64cdfad42e4.png)). The data center may not be the most logical. As an example, some in the UK have reported needing to select "Central Europe" instead of "Western Europe".
    * **SERVICE API:** Under "Service API" ensure these APIs are listed: `IoT Core` and `Authorization`. To be sure, click subscribe again on every service.  Very important: **disable popup blockers** otherwise subscribing won't work without providing any indication of a failure. Make sure you authorize your Project to use those APIs:
        - Click "Service API" tab
        - Click "**Go to Authorize**" button
        - Select the API Groups from the dropdown and click `Subscribe` ([screenshot](https://user-images.githubusercontent.com/38729644/128742724-9ed42673-7765-4e21-94c8-76022de8937a.png))

5. WIZARD - Run Setup Wizard:
    * From your Linux/Mac/Win PC run the TinyTuya Setup **Wizard** to fetch the *Local_Keys* for all of your registered devices:
      ```bash
      python -m tinytuya wizard   # use -nocolor for non-ANSI-color terminals
      ```
    * The **Wizard** will prompt you for the *API ID* key, API *Secret*, API *Region* (cn, us, us-e, eu, eu-w, or in) from your Tuya IoT project as set in Step 3 above.
        * To find those again, go to [iot.tuya.com](https://iot.tuya.com/), choose your project and click `Overview`
            * API Key: Access ID/Client ID
            * API Secret: Access Secret/Client Secret
    * It will also ask for a sample *Device ID*.  You can have the wizard scan for one (enter `scan`), use one from step 2 above or in the Device List on your Tuya IoT project.
    * The **Wizard** will poll the Tuya IoT Cloud Platform and print a JSON list of all your registered devices with the "name", "id" and "key" of your registered device(s). The "key"s in this list are the Devices' *Local_Key* you will use to access your device. 
    * In addition to displaying the list of devices, **Wizard** will create a local file `devices.json` that TinyTuya will use to provide additional details for scan results from `tinytuya.deviceScan()` or when running `python -m tinytuya scan`. The wizard also creates a local file `tuya-raw.json` that contains the entire payload from Tuya Cloud.
    * The **Wizard** will ask if you want to poll all the devices. If you do, it will display the status of all devices on record and create a `snapshot.json` file with these results. Make sure your LAN and firewall permit UDP (6666, 6667 and 7000) and TCP (6668) traffic.

Notes:
* If you ever reset or re-pair your smart devices, the *Local_Key* will be reset and you will need to repeat the steps above.
* The TinyTuya *Wizard* was inspired by the TuyAPI CLI which is an alternative way to fetch the *Local_Keys*: `npm i @tuyapi/cli -g` and run `tuya-cli wizard`  


## Related Projects

  * https://github.com/sean6541/tuyaapi Python API to the web api
  * https://github.com/codetheweb/tuyapi node.js
  * https://github.com/Marcus-L/m4rcus.TuyaCore - .NET
  * https://github.com/SDNick484/rectec_status/ - RecTec pellet smokers control (with Alexa skill)
  * https://github.com/TradeFace/tuyaface - Python Async Tuya API

## TinyTuya Powered Projects

* https://github.com/mafrosis/tinytuya2mqtt - A bridge between TinyTuya and Home Assistant via MQTT
* https://github.com/Whytey/pymoebot - A Python library intended to monitor and control the MoeBot robotic lawn mowers.
* https://github.com/make-all/tuya-local - Local support for Tuya devices in Home Assistant
* https://github.com/teejo75/mtghs - Provides an HTTP service for Moonraker to control Tuya outlets.
* https://github.com/Xenomes/Domoticz-TinyTUYA-Plugin - Plugin for Domoticz Home Automation
