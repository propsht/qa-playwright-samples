from playwright.sync_api import Locator, Page, expect

class PricingSection:
    def __init__(self, page: Page, root: Locator):
        self.page = page
        self.root = root

        self.tabs = self.root.locator("div.tabs .tab") # list of tabs
        self.panels = self.root.locator("div.item-tab") # panel of tabs
        self.active_panel = self.root.locator("div.item-tab:visible") # active panel

        self.cards_in_active = self.active_panel.locator("div.redbox-container") # cards inside active panel

        self.card_title_in = ".redbox-container-head .main-h2" # sub elements inside the card
        self.card_cta_btn_in = "div.pricing-btn button"  # BUY NOW / SEARCH NOW
        self.card_more_link_in = "a:has-text('More About Plan')" # more about link


#____________ Pricing Plan Actions

    # Find the right tab and Click on the right tab
    def choose_tab(self, tab_name: str):
        self.tabs.filter(
            has=self.page.locator("h3", has_text=tab_name)
        ).click()

        expect(self.active_panel).to_be_visible()
        expect(self.cards_in_active.first).to_be_visible()

    # Search right card
    def card(self, card_title: str):
        return self.cards_in_active.filter(
            has=self.page.locator(self.card_title_in, has_text=card_title)
        )


    # Choose and click on button
    def cta_btn_in_card(self, card_title: str, btn_label: str):
        card = self.card(card_title)
        return card.get_by_role("button", name=btn_label)

    def open_plan(self, tab_name: str, card_title: str, btn_label: str):
        self.choose_tab(tab_name)
        expect(self.card(card_title)).to_be_visible()
        self.cta_btn_in_card(card_title, btn_label).click()