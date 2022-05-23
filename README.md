# Franklyapp

## Currently in Beta release
![Schermafbeelding 2022-05-23 om 14 46 48](https://user-images.githubusercontent.com/71013416/169822424-08e2365c-4cef-48f5-9643-33ac5e8313ce.png)

![Schermafbeelding 2022-05-23 om 14 45 53](https://user-images.githubusercontent.com/71013416/169822311-34d87a49-b1c6-4138-989a-e8f7aa47f612.png)

![WhatsApp Image 2022-03-30 at 6 30 49 PM](https://user-images.githubusercontent.com/71013416/161023146-d84b51a8-0b2c-4b24-a12f-8b4420363762.jpeg)

![WhatsApp Image 2022-03-30 at 8 51 00 PM (1)](https://user-images.githubusercontent.com/71013416/161023157-b4e2c01f-53de-44af-90d0-6e676667c86a.jpeg)
![WhatsApp Image 2022-03-30 at 8 51 00 PM](https://user-images.githubusercontent.com/71013416/161023180-2cc41cbf-9648-4f59-95da-060578e74263.jpeg)

## Frankly
Frankly helps to make giving feedback easier. There are 4 methods that frankly can help you get feedback: 
1. Through SMS: Frankly sends you the template to your phone, and you can copy it to any messaging app you like
2. Link: Simply share a URL 
3. QR codes: Simply print QR codes to your own design and share it in the real world
4. Email: Simply email yourself the template or send it in a batch to your customers directly 

## Installation

#### Set up: 
- You'll need a configfile named `Env_Settings.cfg`  that containt the API keys to the services used (Twilio and some other API'). 
- Upon startup the server will load in these keys so it can function 
- You'll need an SQL server to store records. Connection details are also added to the env_settings file, however SQLite can be used as well

#### how to run:
To run a developmentserver run: 
- python Developmentserver.py

For production server: 
- gunicorn.sh (for local running)
- deployscript.py to deploy to Lightsail and start the server there (This probably only works for me as you need very specific keys to deploy to amazon) 


