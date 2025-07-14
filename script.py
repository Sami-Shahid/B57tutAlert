from playwright.sync_api import sync_playwright
import re
import requests
import os


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)  
    page = browser.new_page()
    page.goto("https://ttb.utoronto.ca")

    # Grab some text

    page.get_by_text("Select an option").nth(0).click()
    page.get_by_text("University of Toronto Scarborough").click()
    page.get_by_label("Session (Required)").get_by_text("Summer First Sub-Session 2025 (F)Summer Second Sub-Session 2025 (S)Summer Full").click()
    page.get_by_role("checkbox", name="Fall-Winter 2025-2026, Fall 2025 (F)").click()
    page.get_by_role("combobox", name="Course Code, Course Title, or").click()
    page.get_by_role("combobox", name="Course Code, Course Title, or").fill("stab")
    page.get_by_role("option", name=re.compile("STAB57")).first.click()
    page.get_by_role("button", name="Search").click()
    page.get_by_role("button", name=re.compile("STAB57")).first.click()
    



    sections = page.locator(".item-value")
    count = sections.count()
    for i in range(count):
        name = sections.nth(i).inner_text()
        if ("of 34" in name):
            if (int(name[0])!=0):
                data = {
                    "accountKey": os.environ.get("ALERTZY_KEY"),
                    "title": "UofT Timetable",
                    "message": "TUT0002 has an open spot!"
                }
                requests.post("https://alertzy.app/send", data=data)


            browser.close()
            break





    browser.close()