# Franklyapp
## Currently in pre-production stage
![WhatsApp Image 2022-03-18 at 6 31 34 PM](https://user-images.githubusercontent.com/71013416/159140820-3f84a0a2-acf1-43b4-991b-93ff60fd82b4.jpeg)

![Schermafbeelding 2022-03-19 om 23 50 08](https://user-images.githubusercontent.com/71013416/159141082-ea9481c5-9e38-48ec-859d-417d132c3e38.png)

![WhatsApp Image 2022-03-30 at 6 30 49 PM](https://user-images.githubusercontent.com/71013416/161023146-d84b51a8-0b2c-4b24-a12f-8b4420363762.jpeg)

![WhatsApp Image 2022-03-30 at 8 51 00 PM (1)](https://user-images.githubusercontent.com/71013416/161023157-b4e2c01f-53de-44af-90d0-6e676667c86a.jpeg)
![WhatsApp Image 2022-03-30 at 8 51 00 PM](https://user-images.githubusercontent.com/71013416/161023180-2cc41cbf-9648-4f59-95da-060578e74263.jpeg)

## Frankly
Frankly helps to make giving feedback easier. Users can generate QR codes that they can add to workshops, powerpoints, put in waiting areas or share after events to collect feedback on how visitors liked the event. 

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

## Feature roadmap

- [x] Recieve feedback assets via Whatsapp / Email functionality
- [ ] Create password reset logic
- [ ] Add Terms and conditions
- [ ] Add blog
- [ ] Link to this github and make user feature ideas possible
- [x] Implement pricing for multiple campaigns
- [x] Implement logic for calculating pricing
- [ ] Improve the look and feel of the chat functionality
- [x] Add custom questions to be added from the interface
