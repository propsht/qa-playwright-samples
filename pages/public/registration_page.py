from pages.base_page import BasePage

from playwright.sync_api import expect


class RegistrationPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page = page
        self.first_name_input = page.locator('input[placeholder="First Name"]')
        self.last_name_input = page.locator('input[placeholder="Last Name"]')
        self.email_input = page.locator('input[placeholder="Email Address"]')
        self.password_input = page.locator('input[placeholder="Password"]')
        self.confirm_password_input = page.locator('input[placeholder="Confirm Password"]')
        self.accept_chk = page.locator('label.checkbox').nth(0)
        self.registration_button = page.get_by_role('button', name='Get Started')

        # FrameLocator for the first reCAPTCHA iframe
        self.captcha_frame = page.frame_locator('iframe[title="reCAPTCHA"]').first
        # Inside that frame, target the anchor by its ID
        self.captcha_anchor = self.captcha_frame.locator('#recaptcha-anchor')

    def register(self, first_name: str, last_name: str, email: str, password: str):
        # 1) Fill out the form
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.confirm_password_input.fill(password)
        self.accept_chk.click()

        # 2) Wait for the checkbox anchor, click it
        expect(self.captcha_anchor).to_be_visible(timeout=15_000)
        self.captcha_anchor.click()

        # 3) Verify it's checked via aria-checked="true"
        expect(self.captcha_anchor).to_have_attribute('aria-checked', 'true', timeout=15_000)

        # 4) Now the submit button should be enabled
        expect(self.registration_button).to_be_enabled()

        # 5) Submit
        self.registration_button.click()
