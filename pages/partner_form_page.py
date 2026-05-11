from pathlib import Path
from playwright.sync_api import Page
from selector.selectors import PartnerFormSelectors


class PartnerFormPage:
    def __init__(self, page: Page):
        self.page = page

    def fill_name(self, name: str) -> None:
        self.page.locator(PartnerFormSelectors.NAME_INPUT).fill(name)

    def select_type_service(self) -> None:
        container = self.page.locator(PartnerFormSelectors.TYPE_CONTAINER)
        container.click()
        container.locator(PartnerFormSelectors.TYPE_SERVICE_OPTION).click()

    def select_first_service(self) -> None:
        container = self.page.locator(PartnerFormSelectors.SERVICES_CONTAINER)
        container.click()
        container.locator(PartnerFormSelectors.DROPDOWN_OPTION).first.click()
        # Click name field to close the multi-select dropdown
        self.page.locator(PartnerFormSelectors.NAME_INPUT).click()

    def select_first_subscription(self) -> None:
        container = self.page.locator(PartnerFormSelectors.SUBSCRIPTION_CONTAINER)
        container.click()
        container.locator(PartnerFormSelectors.DROPDOWN_OPTION).first.click()

    def fill_address(self, address: str) -> None:
        self.page.locator(PartnerFormSelectors.ADDRESS_INPUT).fill(address)
        self.page.wait_for_selector(
            PartnerFormSelectors.ADDRESS_AUTOCOMPLETE,
            state="visible",
            timeout=5000,
        )
        self.page.locator(PartnerFormSelectors.ADDRESS_AUTOCOMPLETE).first.click()

    def fill_phone(self, phone: str) -> None:
        self.page.locator(PartnerFormSelectors.PHONE_INPUT).fill(phone)

    def fill_contact_person(self, name: str) -> None:
        self.page.locator(PartnerFormSelectors.CONTACT_INPUT).fill(name)

    def fill_description(self, text: str) -> None:
        self.page.locator(PartnerFormSelectors.DESCRIPTION_INPUT).fill(text)

    def upload_logo(self) -> None:
        logo_path = Path(__file__).parent.parent / "fixtures" / "test_logo.png"
        self.page.locator(PartnerFormSelectors.UPLOAD_INPUT).set_input_files(
            str(logo_path)
        )
        crop_save = self.page.locator(PartnerFormSelectors.CROP_MODAL_SAVE)
        crop_save.wait_for(state="visible", timeout=10000)
        crop_save.click()
        # Wait for crop modal to fully close before returning
        crop_save.wait_for(state="hidden", timeout=10000)

    def submit(self) -> None:
        save_btn = self.page.locator(PartnerFormSelectors.SAVE_BUTTON)
        save_btn.wait_for(state="visible", timeout=10000)
        save_btn.scroll_into_view_if_needed()
        save_btn.click()

    def wait_for_modal_close(self) -> None:
        self.page.wait_for_selector(
            PartnerFormSelectors.NAME_INPUT,
            state="hidden",
            timeout=15000,
        )
