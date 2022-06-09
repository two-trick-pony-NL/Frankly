from urllib import response
from website.payments import *
from website.qrgenerator import *
import os
import tempfile

import pytest

from app import app


@pytest.fixture
def client():
    app.config.update({'TESTING': True})

    with app.test_client() as client:
        yield client


"""
Testing that the testsuite works
"""
def test_answer1():
    assert func(3) == 4   


"""
QRCode URL validation (creating new QR code + testing the values)
"""
def test_qrcodedetractor():
    import cv2 as cv
    createQR(3) #testing on user3 the testuser
    im = cv.imread("./website/static/qrcodes/User_3_detractor.png")
    det = cv.QRCodeDetector()
    retval, points, straight_qrcode = det.detectAndDecode(im)
    assert retval == str("https://franklyapp.nl/send-feedback/3/1")


def test_qrcodeneutral():
    import cv2 as cv
    createQR(3) #testing on user3 the testuser
    im = cv.imread("./website/static/qrcodes/User_3_neutral.png")
    det = cv.QRCodeDetector()
    retval, points, straight_qrcode = det.detectAndDecode(im)
    assert retval == str("https://franklyapp.nl/send-feedback/3/2")

def test_qrcodepromotor():
    import cv2 as cv
    createQR(3) #testing on user3 the testuser
    im = cv.imread("./website/static/qrcodes/User_3_promotor.png")
    det = cv.QRCodeDetector()
    retval, points, straight_qrcode = det.detectAndDecode(im)
    assert retval == str("https://franklyapp.nl/send-feedback/3/3")

def test_qrcodeneutrallink():
    import cv2 as cv
    createQR(3) #testing on user3 the testuser
    im = cv.imread("./website/static/qrcodes/User_3_generic.png")
    det = cv.QRCodeDetector()
    retval, points, straight_qrcode = det.detectAndDecode(im)
    assert retval == str("https://franklyapp.nl/getfeedback/2")




"""
Testing the payment module
"""
#Test if we get an empty response
def test_knownuser(client):
    response = client.get('/incoming_payment/3')
    assert response.status_code == 204

#Test we handle unknown users
def test_unknownuser(client):
    response = client.get('/incoming_payment/aa')
    assert response.status_code == 404
    assert b"404 Not found" in response.data
def test_useroutofrange(client):
    response = client.get('/incoming_payment/99999999')
    assert response.status_code == 404
    assert b"404 Not found" in response.data