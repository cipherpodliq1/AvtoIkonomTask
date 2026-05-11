from playwright.sync_api import Page, expect


def wait_for_url_contains(page: Page, fragment: str, timeout: int = 10000) -> None:
    """Wait until the current URL contains the given fragment."""
    expect(page).to_have_url(
        lambda url: fragment in url,
        timeout=timeout
    )


def assert_element_visible(page: Page, selector: str, message: str = "") -> None:
    """Assert a single element is visible with a clear failure message."""
    expect(
        page.locator(selector)
    ).to_be_visible(
        timeout=10000
    )


def reload_and_assert_visible(page: Page, selector: str, message: str = "") -> None:
    """
    Reload the page and assert the element is still visible.
    Used for persistence checks after create/edit operations.
    """
    page.reload()
    page.wait_for_load_state("networkidle")
    assert_element_visible(page, selector, message)
