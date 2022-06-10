from playwright.sync_api import Playwright, sync_playwright, expect
from urllib import response
from website.payments import *
from website.qrgenerator import *
import os
import subprocess
import tempfile

import pytest

from app import app



@pytest.fixture
def client():
    app.config.update({'TESTING': True})
    with app.test_client() as client:
        yield client

def run(playwright: Playwright) -> None:
    subprocess.run('pwd')
    subprocess.run('cd ../..; cd ..; aws s3 cp s3://franklyappsecret/Env_Settings.cfg .; python3 developmentserver.py')
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()

    # Open new page
    page = context.new_page()

    # Go to http://localhost/
    page.goto("http://localhost:8080/")

    # Click text=Who is behind Frankly?
    page.locator("text=Who is behind Frankly?").click()

    # Click text=How can I get in contact with Frankly?
    page.locator("text=How can I get in contact with Frankly?").click()

    # Click text=Is Frankly free to use?
    page.locator("text=Is Frankly free to use?").click()

    # Click text=Why do you need my phone number (and email address)?
    page.locator("text=Why do you need my phone number (and email address)?").click()

    # Click text=We use those details to send you your Frankly templates. For instance we'll text
    page.locator("text=We use those details to send you your Frankly templates. For instance we'll text").click()

    # Click text=We use those details to send you your Frankly templates. For instance we'll text
    page.locator("text=We use those details to send you your Frankly templates. For instance we'll text").click()

    # Click text=I like Frankly but I miss functionality X, can you add that?
    page.locator("text=I like Frankly but I miss functionality X, can you add that?").click()

    # Click text=I'm on the waiting list, when can I use Frankly?
    page.locator("text=I'm on the waiting list, when can I use Frankly?").click()

    # Click text=/.*Frankly is in "Beta", what does that mean\?.*/
    page.locator("text=/.*Frankly is in \"Beta\", what does that mean\\?.*/").click()

    # Click text=Privacy
    page.locator("text=Privacy").click()
    expect(page).to_have_url("http://localhost/legal/privacy")

    # Click footer >> text=Terms
    page.locator("footer >> text=Terms").click()
    expect(page).to_have_url("http://localhost/legal/terms")

    # Click footer >> text=Pricing
    page.locator("footer >> text=Pricing").click()
    expect(page).to_have_url("http://localhost/legal/pricing")

    # Click text=Github
    page.locator("text=Github").click()
    expect(page).to_have_url("https://github.com/two-trick-pony-NL/Frankly")

    # ---------------------
    context.close()
    browser.close()

with sync_playwright() as playwright:
    
    run(playwright)
