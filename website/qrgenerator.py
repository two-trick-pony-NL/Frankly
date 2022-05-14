import qrcode

#This script creates QR Codes, it is currently triggered on signup and at log in. 

def createQR(userID):
    userID = str(userID)
    # Create Promotor QR code
    img = qrcode.make('https://franklyapp.nl/send-feedback/'+userID+'/3')
    img.save("./website/static/qrcodes/User_"+userID+"_promotor.png")
    # Create Neutral QR code
    img = qrcode.make('https://franklyapp.nl/send-feedback/'+userID+'/2')
    img.save("./website/static/qrcodes/User_"+userID+"_neutral.png")
    # Create Detractor QR code
    img = qrcode.make('https://franklyapp.nl/send-feedback/'+userID+'/1')
    img.save("./website/static/qrcodes/User_"+userID+"_detractor.png")
    #Creating a generic QR code
    img = qrcode.make('https://franklyapp.nl/getfeedback/'+userID+'/1')
    img.save("./website/static/qrcodes/User_"+userID+"_generic.png")
  
createQR(1)

