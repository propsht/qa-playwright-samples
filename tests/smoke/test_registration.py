from playwright.sync_api import expect
from pages import RegistrationPage


def test_user_can_register(page, config, unique_email: str):
    page.goto(f"{config.BASE_URL}/auth/register?plan=1&product=FREE")

    registration_page = RegistrationPage(page)
    registration_page.register(
        config.TEST_USER_FIRST_NAME,
        config.TEST_USER_LAST_NAME,
        unique_email,
        
        config.TEST_USER_PASSWORD
    )

    # 1) Verify we land on the thank-you page
    expect(page).to_have_url(f"{config.BASE_URL}/thankyou", timeout=20_000)
    # 2) Then verify we finally end up on the dashboard
    expect(page).to_have_url(f"{config.BASE_URL}/account/dashboard", timeout=20_000)

