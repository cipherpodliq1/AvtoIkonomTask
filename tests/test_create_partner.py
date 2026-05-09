import pytest
from pages.partners_page import PartnersPage
from pages.partner_form_page import PartnerFormPage
from utils.helpers import reload_and_assert_visible


@pytest.mark.smoke
@pytest.mark.partners
def test_create_partner(page, partner_data):
    """
    TC-01 | Create Partner
    Covers: navigation to partners, form fill with all required fields,
    successful save, visibility in table, persistence after page reload.
    """
    partners_page = PartnersPage(page)
    form_page = PartnerFormPage(page)

    # ── Navigate ──────────────────────────────────────────────────────────────
    partners_page.navigate()

    # ── Open form ─────────────────────────────────────────────────────────────
    partners_page.open_create_form()

    # ── Fill all required fields ──────────────────────────────────────────────
    form_page.fill_name(partner_data["name"])
    form_page.select_type_service()
    form_page.select_first_service()
    form_page.select_first_subscription()
    form_page.fill_address(partner_data["address"])
    form_page.fill_phone(partner_data["phone"])
    form_page.fill_contact_person(partner_data["contact_person"])
    form_page.fill_description(partner_data["description"])
    form_page.upload_logo()

    # ── Submit ────────────────────────────────────────────────────────────────
    form_page.submit()
    form_page.wait_for_modal_close()

    # ── Assert: partner appears in the table ──────────────────────────────────
    partners_page.assert_partner_visible(partner_data["name"])

    # ── Assert: partner persists after reload ─────────────────────────────────
    reload_and_assert_visible(
        page,
        f"span.Cq6YF:has-text('{partner_data['name']}')",
        f"Partner '{partner_data['name']}' should persist after page reload"
    )