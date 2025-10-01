import pytest
from pages import HomePage, PricingPage, AccountPricingPage, LoginPage
from config import Config



PRICING_CASES = [
    # tab_name,              card_title,         btn_label,        plan,    product
    # Dating
    ("DATING/ALTERNATIVE ",     "FREE SCAN",        "SEARCH NOW",   "1",    "FREE"),
    ("DATING/ALTERNATIVE ",     "FLEX PACKAGE",     "BUY NOW",      "5",    "DS"),
    ("DATING/ALTERNATIVE ",     "MONTHLY",          "BUY NOW",      "11",   "DS"),
    ("DATING/ALTERNATIVE ",     "ULTIMATE",         "BUY NOW",      "26",   "DS"),

    # Social
    ("SOCIAL MEDIA & MOBILE ",  "FREE SCAN",        "SEARCH NOW",   "1",    "FREE"),
    ("SOCIAL MEDIA & MOBILE ",  "FLEX PACKAGE",     "BUY NOW",      "5",    "SM"),
    ("SOCIAL MEDIA & MOBILE ",  "MONTHLY",          "BUY NOW",      "11",   "SM"),
    ("SOCIAL MEDIA & MOBILE ",  "ULTIMATE",         "BUY NOW",      "26",   "SM"),

    # Listin Locator
    ("LISTING LOCATOR",         "LISTING LOCATOR",  "BUY NOW",      "8",    "LL"),
    ("LISTING LOCATOR",         "ULTIMATE",         "BUY NOW",      "26",   "LL"),

    #Cams
    ("LIVE ADULT STREAMS",      "XXX FLEX",         "BUY NOW",      "17",   "LC"),
    ("LIVE ADULT STREAMS",      "XXX MONTHLY",      "BUY NOW",      "20",   "LC"),
    ("LIVE ADULT STREAMS",      "ULTIMATE",         "BUY NOW",      "26",   "LC"),

    # XXX
    ("XXX WEBSITES",            "XXX FLEX",         "BUY NOW",      "17",   "XS"),
    ("XXX WEBSITES",            "XXX MONTHLY",      "BUY NOW",      "20",   "XS"),
    ("XXX WEBSITES",            "ULTIMATE",         "BUY NOW",      "26",   "XS"),

    # Tinder
    ("TINDER BLASTER",          "TINDER BLASTER",   "BUY NOW",      "2",    "TN"),
    ("TINDER BLASTER",          "ULTIMATE",         "BUY NOW",      "26",   "TN"),

]

# CASE_IDS = [
#     f"{t.strip()} -{c}-{b}-{p}-{pr}"
#     for (t, c, b, p, pr) in PRICING_CASES
# ]

PARAMS = pytest.mark.parametrize(
    "tab_name, card_title, btn_label, plan, product",
    PRICING_CASES,
    #ids=CASE_IDS,
)

@PARAMS
def test_pricing_redirect_home_page(page, tab_name, card_title, btn_label, plan, product):
    home = HomePage(page)
    page.goto(Config.BASE_URL)

    home.open_plan(tab_name, card_title, btn_label)

    page.wait_for_url("**/auth/register**", timeout=20_000)
    print("DEBUG URL after click:", page.url)

    url = page.url
    assert url.startswith(f"{Config.BASE_URL}/auth/register")
    assert f"plan={plan}" in url
    assert f"product={product}" in url
    page.wait_for_timeout(2000)


@PARAMS
def test_pricing_redirect_pricing_page(page, tab_name, card_title, btn_label, plan, product):
    pricing = PricingPage(page)
    page.goto(F"{Config.BASE_URL}/products-services/")

    pricing.open_plan(tab_name, card_title, btn_label)

    page.wait_for_url("**/auth/register**", timeout=20_000)
    print("DEBUG URL after click:", page.url)

    url = page.url
    assert url.startswith(f"{Config.BASE_URL}/auth/register")
    assert f"plan={plan}" in url
    assert f"product={product}" in url
    page.wait_for_timeout(2000)

# @PARAMS
# def test_pricing_redirect_account_pricing_page(page, config, tab_name, card_title, btn_label, plan, product):
#
#
#     # Login
#     page.goto(f"{config.BASE_URL}/auth/login/")
#
#     login_page = LoginPage(page)
#     login_page.login(config.USER_EMAIL, config.USER_PASSWORD)
#
#     page.wait_for_url("**/account/dashboard/**", timeout=20_000)
#     assert "dashboard" in page.url
#
#     # go to the dashboard pricing page (adjust path if different)
#     page.goto(F"{Config.BASE_URL}/products-services/")
#
#     pricing = AccountPricingPage(page)
#     pricing.open_plan(tab_name, card_title, btn_label)
#
#     page.wait_for_url("**/auth/register**", timeout=20_000)
#     print("DEBUG URL after click:", page.url)
#
#     url = page.url
#     assert url.startswith(f"{Config.BASE_URL}/auth/register")
#     assert f"plan={plan}" in url
#     assert f"product={product}" in url
#     page.wait_for_timeout(2000)

