import qrcode

def createQR(userID):
    userID = str(userID)
    # Create Promotor QR code
    img = qrcode.make('https://grapevine.vdotvo9a4e2a6.eu-central-1.cs.amazonlightsail.com//send-feedback/'+userID+'/10')
    img.save("./website/static/qrcodes/User_"+userID+"_promotor.png")
    # Create Neutral QR code
    img = qrcode.make('https://grapevine.vdotvo9a4e2a6.eu-central-1.cs.amazonlightsail.com//send-feedback/'+userID+'/7')
    img.save("./website/static/qrcodes/User_"+userID+"_neutral.png")
    # Create Detractor QR code
    img = qrcode.make('https://grapevine.vdotvo9a4e2a6.eu-central-1.cs.amazonlightsail.com//send-feedback/'+userID+'/3')
    img.save("./website/static/qrcodes/User_"+userID+"_detractor.png")
  
createQR(1)