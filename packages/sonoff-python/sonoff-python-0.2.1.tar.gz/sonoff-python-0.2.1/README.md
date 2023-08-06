# sonoff-python
Make use of your sonoff smart switches without flashing them via the cloud APIs, this should work in Python 2 or Python 3.

This project is heavily inspired (read: almost entirely borrowed) by the work that Peter Buga did on a Simple Home Assistant integration for Ewelink https://github.com/peterbuga/HASS-sonoff-ewelink

I spent a day looking into various ways to work with Sonoff switches and drew a bit of a blank. There seeem to be quite a few projects that are designed to replace the Ewelink cloud platform either by flashing the Sonoff switches with new firmware, or hijacking the setup process and running a fake cloud service locally on a Raspberry Pi or similar.

I tried this approach but it didn't work for me as I was using a 4 channel switch, and it seems that most of them had only been tested with single channel switches. Also many of these were not maintained actively or had clearly been written for a specific use case.

I finally came across Peter's work written in python and it was exactly what I was looking for, a class that I could instantiate and control my switch remotely without flashing or having to use Charles to sniff my authentication code etc.

## Installation

Use pip or easy_install

> pip install sonoff-python

The requirements are requests and websocket-client, see _requirements.txt_

## Configuration

Configuration is simple and basically passed to the class when you instantiate it. Username is either the email address you use to log in to Ewelink, or your phone number with the country code in front.

> **username** - The email address or phone number you signed up with on Ewelink. Preface phone number with the country code

> **password** - Your password to Ewelink.

> **api_region** - The API region you use, valid ones are apparently 'us', 'eu' and 'cn'

> **user_apikey** - The API key of authenticated user, defaults to None

> **bearer_token** - The Bearer token of authenticated user, defaults to None

> **grace_period** - This defaults to 600, I don't know why yet.

## Usage
Here's a really simple example of how you can use this library. 

```
import sonoff
import config

s = sonoff.Sonoff(config.username, config.password, config.api_region)
devices = s.get_devices()
if devices:
    # We found a device, lets turn something on
    device_id = devices[0]['deviceid']
    s.switch('on', device_id, None)

# update config
config.api_region = s.get_api_region
config.user_apikey = s.get_user_apikey
config.bearer_token = s.get_bearer_token
```

## Support

I have tested in Python 2 and Python 3, however as we all know there may be some library weirdness.

I mainly put this together for my own use, I have learned a little about how the Sonoff kit works but for support it might be better to look at the library Peter Buga put together. I'm happy to look at any issues though.

## Troubleshooting

### Ewelink registration for 4 channel switches
The Sonoff switches have one of the most non-intuitive installation processes I have encountered. For registering my 4 channel switch I had to:
* Hold one of the buttons until it flashed quick, quick, slow.
* Hold a second time until it rapidly flashed in a constant pattern. I did not see the ITEAD-xx access point until it rapidly flashed.
* Once it is rapidly flashing, connect to the ITEAD-xx network.
* Choose the Compatible Pairing Mode (AP) option, then press Next. (This looks like a help page, but it is actually a fourth option (and the one you want!!)).
* Follow the onscreen instructions.
