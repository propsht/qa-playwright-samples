from playwright.sync_api import Page
from pages.components.pricing_section import PricingSection

class PricingPage:
    def __init__(self, page: Page):
        self.page = page
        self.pricing = PricingSection(page, root=page.locator("div.pricing"))

    def open_plan(self, tab_name, card_title, btn_label):
        self.pricing.open_plan(tab_name, card_title, btn_label)
