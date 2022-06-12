from playwright.sync_api import Playwright, sync_playwright, expect
import time

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    time.sleep(5)
    # Open new page
    # Open new page
    page = context.new_page()
    # Go to http://localhost:8080/
    page.goto("http://localhost:8080/")
    # Click text=Sign In
    page.locator("text=Sign In").click()
    # expect(page).to_have_url("http://localhost:8080/sign-in")
    # Click [placeholder="Enter your Email"]
    page.locator("[placeholder=\"Enter your Email\"]").click()
    # Fill [placeholder="Enter your Email"]
    page.locator("[placeholder=\"Enter your Email\"]").fill("testuser2022@petervandoorn.com")
    # Press Tab
    page.locator("[placeholder=\"Enter your Email\"]").press("Tab")
    # Fill [placeholder="Enter your Password"]
    page.locator("[placeholder=\"Enter your Password\"]").fill("testuser2022")
    # Click text=Login
    page.locator("text=Login").click()
    # expect(page).to_have_url("http://localhost:8080/dashboard/testuser2022?user=%3CUser+59%3E")
    # Click button:has-text("Email")
    page.locator("button:has-text(\"Email\")").click()
    # Click text=Send the template to my email address
    page.locator("text=Send the template to my email address").click()
    # expect(page).to_have_url("http://localhost:8080/dashboard/testuser2022?user=%3CUser+59%3E")
    # Click button:has-text("Email")
    page.locator("button:has-text(\"Email\")").click()
    # Click [placeholder="bob\@bob\.com\, alice\@alice\.com"]
    page.locator("[placeholder=\"bob\\@bob\\.com\\, alice\\@alice\\.com\"]").click()
    # Fill [placeholder="bob\@bob\.com\, alice\@alice\.com"]
    page.locator("[placeholder=\"bob\\@bob\\.com\\, alice\\@alice\\.com\"]").fill("test1@petrervandoorn.com, test2@petrervandoorn.com")
    # Click text=Send to client
    page.locator("text=Send to client").click()
    time.sleep(2)
    page.goto("http://localhost:8080/dashboard/testuser2022")
    time.sleep(2)
    # Click text=Next Next graph
    page.locator("text=Next Next graph").click()
    # Click text=Next Next graph
    page.locator("text=Next Next graph").click()
    # Click text=Next Next graph
    page.locator("text=Next Next graph").click()
    # Click text=Next Next graph
    page.locator("text=Next Next graph").click()
    
    page.locator("text=Log Out").click()
    # expect(page).to_have_url("http://localhost:8080/home")
    # ---------------------
    context.close()
    browser.close()
with sync_playwright() as playwright:
    run(playwright)