class LoginSelectors:
    EMAIL_INPUT     = "input[autocomplete='email']"
    PASSWORD_INPUT  = "input[type='password']"
    SUBMIT_BUTTON   = "button[type='submit']"


class NavSelectors:
    PARTNERS_PATH   = "/partners"


class PartnersPageSelectors:
    NEW_PARTNER_BUTTON  = "button:has-text('New partner')"
    SEARCH_INPUT        = "#search-partners"
    TABLE_ROW           = "tr.ant-table-row"
    # Application-generated class for the partner name cell.
    # Not ideal — a data-testid would be more stable — but this is
    # the only identifier available in the current UI build.
    PARTNER_NAME_CELL   = "span.Cq6YF"
    CONTACT_PERSON_CELL = "td.testid-pickUpDateColumn"
    ACTION_BUTTON       = "#action-button"


class PartnerFormSelectors:
    # Text inputs
    NAME_INPUT          = "#name-field"
    ADDRESS_INPUT       = "#address-field"
    ADDRESS_AUTOCOMPLETE = ".pac-item"
    PHONE_INPUT         = "#phone-field"
    CONTACT_INPUT       = "#contact-person-field"
    DESCRIPTION_INPUT   = "#description-field"

    # Each dropdown scoped to its own container via :has()
    # This prevents cross-dropdown option matching entirely
    TYPE_CONTAINER          = "div.ant-select:has(#partner-type-field)"
    SERVICES_CONTAINER      = "div.ant-select:has(#service-types-field)"
    SUBSCRIPTION_CONTAINER  = "div.ant-select:has(#subscription-tier-field)"

    # Options — always used scoped inside their container
    TYPE_SERVICE_OPTION = "div[label='Service']"
    DROPDOWN_OPTION     = ".ant-select-item-option"

    # File upload
    UPLOAD_INPUT = "input[name='file-upload']"
    LOGO_CROP_SAVE = "button:has(span.J9zkR:not([id]))"

    # Modal actions
    SAVE_BUTTON = "button:has(#save-button)"
    CANCEL_BUTTON       = "#cancel-button"
    MODAL_WRAPPER       = ".ant-modal-wrap"

class EditMenuSelectors:
    EDIT_BUTTON         = "#edit-button"
    DELETE_BUTTON       = "#delete-button"