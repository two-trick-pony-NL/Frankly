from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user

payments = Blueprint("payments", __name__)

@payments.route("/incoming_payment/<paymentID>", methods=['GET', 'POST'])
def incoming_payment(paymentID):
    print(paymentID)
    return('success')
