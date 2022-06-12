from playwright.sync_api import Playwright, sync_playwright, expect
import time

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    time.sleep(5)
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
    # Click section:has-text("Sign In to your account Email Address Password If you have forgotten your passwo")
    page.locator("section:has-text(\"Sign In to your account Email Address Password If you have forgotten your passwo\")").click()
    # Click text=Login
    page.locator("text=Login").click()
    # expect(page).to_have_url("http://localhost:8080/dashboard/testuser2022?user=%3CUser+59%3E")
    # Click text=Log Out
    page.locator("text=Log Out").click()
    # expect(page).to_have_url("http://localhost:8080/home")
    # ---------------------
    context.close()
    browser.close()
with sync_playwright() as playwright:
    run(playwright)