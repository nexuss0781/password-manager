import sys
from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch()
    context = browser.new_context()
    page = context.new_page()

    page.goto(sys.argv[2])

    # Login
    page.fill('input[name="email"]', 'testuser@example.com')
    page.fill('input[name="password"]', 'password')
    page.click('button[type="submit"]')
    page.wait_for_url("**/dashboard")

    page.screenshot(path=f"/home/jules/verification/{sys.argv[1]}.png")
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
