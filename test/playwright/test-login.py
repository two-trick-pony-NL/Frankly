from playwright.sync_api import Playwright, sync_playwright, expect
import time

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    time.sleep( 5)
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
    page.locator("[placeholder=\"Enter your Email\"]").fill("test@testuser2022.com")
    # Press Tab
    page.locator("[placeholder=\"Enter your Email\"]").press("Tab")
    # Fill [placeholder="Enter your Password"]
    page.locator("[placeholder=\"Enter your Password\"]").fill("testuser2022")
    # Click section:has-text("Sign In to your account Email Address Password If you have forgotten your passwo")
    page.locator("section:has-text(\"Sign In to your account Email Address Password If you have forgotten your passwo\")").click()
    # Click text=Login
    page.locator("text=Login").click()
     expect(page).to_have_url("http://localhost:8080/sign-in")
    # Click [placeholder="Enter your Email"]
    page.locator("[placeholder=\"Enter your Email\"]").click()
    
    # Click text=Login
    page.locator("text=Login").click()
     expect(page).to_have_url("http://localhost:8080/dashboard/testuser2022?user=%3CUser+2%3E")
    # Click a:has-text("2") >> nth=0
    page.locator("a:has-text(\"2\")").first.click()
     expect(page).to_have_url("http://localhost:8080/dashboard/testuser2022?page=2")
    # Click text=Next Next graph
    page.locator("text=Next Next graph").click()
    # Click text=Next Next graph
    page.locator("text=Next Next graph").click()
    # Click text=Next Next graph
    page.locator("text=Next Next graph").click()
    # Click text=Next Next graph
    page.locator("text=Next Next graph").click()
    # Click text=Log Out
    page.locator("text=Log Out").click()
     expect(page).to_have_url("http://localhost:8080/home")
    # ---------------------
    context.close()
    browser.close()
with sync_playwright() as playwright:
    run(playwright)