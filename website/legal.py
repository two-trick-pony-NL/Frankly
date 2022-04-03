from flask import Blueprint, render_template, redirect, url_for, request, flash

legal = Blueprint("legal", __name__)

@legal.route("/pricing")
def pricing():
    return render_template("/legal/pricing.html")

@legal.route("/terms")
def terms():
    return render_template("/legal/terms.html")

@legal.route("/privacy")
def privacy():
    return render_template("/legal/privacy.html")