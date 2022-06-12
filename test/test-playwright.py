from csv import excel_tab
from playwright.sync_api import Playwright, sync_playwright, expect
from urllib import response
import time



def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    time.sleep( 5)
    # Open new page
    page = context.new_page()

    # Go to http://localhost:8080/
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
    expect(page).to_have_url("http://localhost:8080/legal/privacy")

    # Click footer >> text=Terms
    page.locator("footer >> text=Terms").click()
    expect(page).to_have_url("http://localhost:8080/legal/terms")

    # Click footer >> text=Pricing
    page.locator("footer >> text=Pricing").click()
    expect(page).to_have_url("http://localhost:8080/legal/pricing")

    # Click text=Github
    page.locator("text=Github").click()
    expect(page).to_have_url("https://github.com/two-trick-pony-NL/Frankly")

    # ---------------------
    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
