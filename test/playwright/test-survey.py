from playwright.sync_api import Playwright, sync_playwright, expect
import time

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    time.sleep(5)
    # Open new page
    # Open new page
    page = context.new_page()
    # Go to http://localhost:8080/send-feedback/59/3
    page.goto("http://localhost:8080/send-feedback/59/3")
    # Click [placeholder="Enter your message\.\.\."]
    page.locator("[placeholder=\"Enter your message\\.\\.\\.\"]").click()
    # Fill [placeholder="Enter your message\.\.\."]
    page.locator("[placeholder=\"Enter your message\\.\\.\\.\"]").fill("I am the playwright bot")
    # Click text=Send
    page.locator("text=Send").click()
    # expect(page).to_have_url("http://localhost:8080/step2?ModTotalpost=10&text=I+am+the+playwright+bot&ThisPost=192&user=testuser2022&question0=How+did+you+like+the+service%3F&question1=How+do+you+think+we+can+improve%3F&question2=is+there+anything+else+you%27d+like+to+tell+us%3F+")
    # Click [placeholder="Enter your message\.\.\."]
    page.locator("[placeholder=\"Enter your message\\.\\.\\.\"]").click()
    # Fill [placeholder="Enter your message\.\.\."]
    page.locator("[placeholder=\"Enter your message\\.\\.\\.\"]").fill("Faster pizza")
    # Click text=Send
    page.locator("text=Send").click()
    # expect(page).to_have_url("http://localhost:8080/step3?ThisPost=192&answer2=Faster+pizza&answer1=I+am+the+playwright+bot&user=59&username=testuser2022&question0=How+did+you+like+the+service%3F&question1=How+do+you+think+we+can+improve%3F&question2=is+there+anything+else+you%27d+like+to+tell+us%3F+")
    # Click [placeholder="Enter your message\.\.\."]
    page.locator("[placeholder=\"Enter your message\\.\\.\\.\"]").click()
    # Fill [placeholder="Enter your message\.\.\."]
    page.locator("[placeholder=\"Enter your message\\.\\.\\.\"]").fill("All done")
    # Click text=Send
    page.locator("text=Send").click()
    # expect(page).to_have_url("http://localhost:8080/thanks?publicname=testuser2022&answer1=I+am+the+playwright+bot&answer2=Faster+pizza&answer3=All+done&username=testuser2022&ThisPost=192&user=%3CUser+59%3E&question0=How+did+you+like+the+service%3F&question1=How+do+you+think+we+can+improve%3F&question2=is+there+anything+else+you%27d+like+to+tell+us%3F+")
    # Go to http://localhost:8080/send-feedback/59/1
    page.goto("http://localhost:8080/send-feedback/59/1")
    # Click [placeholder="Enter your message\.\.\."]
    page.locator("[placeholder=\"Enter your message\\.\\.\\.\"]").click()
    # Fill [placeholder="Enter your message\.\.\."]
    page.locator("[placeholder=\"Enter your message\\.\\.\\.\"]").fill("I am the unhappy playwright bot")
    # Click text=Send
    page.locator("text=Send").click()
    # expect(page).to_have_url("http://localhost:8080/step2?ModTotalpost=11&text=I+am+the+unhappy+playwright+bot&ThisPost=193&user=testuser2022&question0=How+did+you+like+the+service%3F&question1=How+do+you+think+we+can+improve%3F&question2=is+there+anything+else+you%27d+like+to+tell+us%3F+")
    # Click [placeholder="Enter your message\.\.\."]
    page.locator("[placeholder=\"Enter your message\\.\\.\\.\"]").click()
    # Fill [placeholder="Enter your message\.\.\."]
    page.locator("[placeholder=\"Enter your message\\.\\.\\.\"]").fill("Nope")
    # Click text=Send
    page.locator("text=Send").click()
    # expect(page).to_have_url("http://localhost:8080/step3?ThisPost=193&answer2=Nope&answer1=I+am+the+unhappy+playwright+bot&user=59&username=testuser2022&question0=How+did+you+like+the+service%3F&question1=How+do+you+think+we+can+improve%3F&question2=is+there+anything+else+you%27d+like+to+tell+us%3F+")
    # Click [placeholder="Enter your message\.\.\."]
    page.locator("[placeholder=\"Enter your message\\.\\.\\.\"]").click()
    # Fill [placeholder="Enter your message\.\.\."]
    page.locator("[placeholder=\"Enter your message\\.\\.\\.\"]").fill("nope")
    # Click text=Send
    # with page.expect_navigation(url="http://localhost:8080/send-feedback/59/2"):
    with page.expect_navigation():
        page.locator("text=Send").click()
    # expect(page).to_have_url("http://localhost:8080/thanks?publicname=testuser2022&answer1=I+am+the+unhappy+playwright+bot&answer2=Nope&answer3=nope&username=testuser2022&ThisPost=193&user=%3CUser+59%3E&question0=How+did+you+like+the+service%3F&question1=How+do+you+think+we+can+improve%3F&question2=is+there+anything+else+you%27d+like+to+tell+us%3F+")
    # Click [placeholder="Enter your message\.\.\."]
    
    context.close()
    browser.close()
with sync_playwright() as playwright:
    run(playwright)
