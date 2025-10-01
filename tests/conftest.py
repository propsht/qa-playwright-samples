import os, pytest, sqlite3
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, Playwright, APIRequestContext
from config import Config
from seo.parsing import fetch_all_page_urls, init_db

# --- 1) Project root & .env load ---
ROOT = Path(__file__).parent.parent
env_path = ROOT / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)


# --- 2) Config class ---
@pytest.fixture(scope="session")
def config():
    """
    Returns the Config class loaded with environment variables
    (BASE_URL, TEST_USER_EMAIL_BASE, TEST_USER_FIRST_NAME, etc.).
    """
    return Config


# --- 3) Prepare output directories ---
@pytest.fixture(scope="session")
def output_dirs():
    """
    Creates and returns a dict of output directories for test artifacts:
      {
        "videos": Path("test-results/videos"),
        "screenshots": Path("test-results/screenshots")
      }
    Ensures these directories exist.
    """
    dirs = {
        "videos": ROOT / "test-results" / "videos",
        "screenshots": ROOT / "test-results" / "screenshots",
    }
    for d in dirs.values():
        d.mkdir(parents=True, exist_ok=True)
    return dirs


# --- 4) Single browser context with optional HTTP auth ---
@pytest.fixture(scope="session")
def context(output_dirs):
    """
    Yields a single Playwright BrowserContext for the entire session:
    - Records video to output_dirs["videos"] at 1280×720.
    - Applies HTTP Basic Auth if AUTH_USER and AUTH_PASS are set.
    Closes the browser when all tests are done.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=bool(os.getenv("CI")))

        args = {
            "record_video_dir": str(output_dirs["videos"]),
            "record_video_size": {"width": 1280, "height": 720},
        }

        user = os.getenv("AUTH_USER")
        pwd = os.getenv("AUTH_PASS")
        if user and pwd:
            args["http_credentials"] = {"username": user, "password": pwd}

        ctx = browser.new_context(**args)
        yield ctx
        browser.close()


# --- 5) New Page for each test ---
@pytest.fixture(scope="function")
def page(context):
    """
    Yields a fresh Playwright Page for each test, then closes it afterward.
    """
    page = context.new_page()
    yield page
    page.close()


# --- 6) Unique email fixture ---
@pytest.fixture
def unique_email():
    """
    Generates a unique email address based on a base:
      igottest+YYYYMMDDHHMMSS@gmail.com
    Gmail will still deliver to igottest@gmail.com via plus-addressing.
    """
    base = os.getenv("TEST_USER_EMAIL")
    if not base or "@" not in base:
        raise RuntimeError("Set TEST_USER_EMAIL in your environment")
    local, domain = base.split("@", 1)

    ts = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    return f"{local}+{ts}@{domain}"


# --- 7) On failure, capture screenshot ---
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Pytest hook that runs after each test call.
    If a test fails, grabs a full-page screenshot into:
      test-results/screenshots/<test_name>.png
    """
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        page = item.funcargs.get("page")
        dirs = item.funcargs.get("output_dirs")
        if page and dirs:
            path = dirs["screenshots"] / f"{item.name}.png"
            page.screenshot(path=str(path), full_page=True)


# --- 8) Pre-session cleanup ---
def pytest_sessionstart(session):
    """
    Before the test session starts, remove any existing
    test-results/email_code.txt file to start fresh.
    """
    email_code = ROOT / "test-results" / "email_code.txt"
    if email_code.exists():
        email_code.unlink()


DB_PATH = "seo.db"


@pytest.fixture(scope="session")
def all_page_urls() -> list[str]:
    """
    Initialize the database (if not already), then fetch all page URLs
    from the sitemap and return them as a list.
    """
    # Ensure the SEO database and table exist
    init_db(DB_PATH)
    # Fetch and return all URLs from the sitemap index
    sitemap_url = f"{Config.BASE_URL}/sitemap.xml"
    return fetch_all_page_urls(sitemap_url)


@pytest.fixture(scope="session")
def baseline_data() -> dict[str, dict[str, str]]:
    """
    Read baseline SEO data from the database into a dict:
    { url: {"title":…, "description":…, "h1":…}, … }
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT url, title, description, h1 FROM seo_pages")
    rows = cur.fetchall()
    conn.close()

    return {
        url: {"title": title, "description": description, "h1": h1}
        for url, title, description, h1 in rows
    }

@pytest.fixture(scope="session")
def api_base_url():
    return Config.HREF.rstrip("/") + "/" + Config.SUXIF.lstrip("/")

@pytest.fixture(scope="session")
def auth_header():
    token = Config.AUTH_TOKEN
    if not token:
        pytest.skip("AUTH_TOKEN env var not set")
    bearer = token if token.lower().startswith("bearer ") else f"Bearer {token}"
    return {"Authorization": bearer, "Accept": "application/json", "Content-Type": "application/json"}

@pytest.fixture(scope="session")
def api(playwright: Playwright, api_base_url, auth_header):
    ctx = playwright.request.new_context(
        base_url=api_base_url,
        extra_http_headers=auth_header,
        ignore_https_errors=True,
    )
    yield ctx
    ctx.dispose()