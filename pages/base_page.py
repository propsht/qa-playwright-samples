from playwright.sync_api import Locator, Page


class BasePage:
    def __init__(self, page):
        self.page = page

    def fill(self, what, text):
        if isinstance(what, Locator):
            what.fill(text)
        else:
            self.page.fill(what, text)

    def click(self, what):
        if isinstance(what, Locator):
            what.click()
        else:
            self.page.click(what)
