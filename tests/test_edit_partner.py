import pytest
from faker import Faker
from playwright.sync_api import expect
from pages.partners_page import PartnersPage
from pages.partner_form_page import PartnerFormPage
from selector.selectors import PartnersPageSelectors
from utils.helpers import reload_and_assert_visible

fake = Faker()


@pytest.mark.bonus
@pytest.mark.partners
def test_edit_partner(page, partner_data):
    """
    TC-02 | Edit Partner (Bonus)
    Covers: create a partner, open edit form, update contact person field,
    save changes, verify update visible in table, persistence after reload.
    """
    partners_page = PartnersPage(page)
    form_page = PartnerFormPage(page)

    # ── Setup: create a partner to edit ──────────────────────────────────────
    partners_page.navigate()
    partners_page.open_create_form()

    form_page.fill_name(partner_data["name"])
    form_page.select_type_service()
    form_page.select_first_service()
    form_page.select_first_subscription()
    form_page.fill_address(partner_data["address"])
    form_page.fill_phone(partner_data["phone"])
    form_page.fill_contact_person(partner_data["contact_person"])
    form_page.fill_description(partner_data["description"])
    form_page.upload_logo()
    form_page.submit()
    form_page.wait_for_modal_close()

    partners_page.assert_partner_visible(partner_data["name"])

    # ── Edit: update contact person ───────────────────────────────────────────
    updated_contact = fake.name()

    partners_page.open_edit_for_partner(partner_data["name"])
    form_page.fill_contact_person(updated_contact)
    form_page.submit()
    form_page.wait_for_modal_close()

    # ── Assert: partner row still present after edit ──────────────────────────
    partners_page.assert_partner_visible(partner_data["name"])

    # ── Assert: updated contact person visible in the correct row ─────────────
    row = partners_page.get_row_by_name(partner_data["name"])
    expect(
        row.locator(PartnersPageSelectors.CONTACT_PERSON_COLUMN)
    ).to_have_text(
        updated_contact,
        timeout=10000
    )

    # ── Assert: changes persist after reload ──────────────────────────────────
    reload_and_assert_visible(
        page,
        f"span.Cq6YF:has-text('{partner_data['name']}')",
        f"Edited partner '{partner_data['name']}' should persist after reload"
    )