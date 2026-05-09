class LoginSelectors:
    EMAIL_INPUT     = "input[autocomplete='email']"
    PASSWORD_INPUT  = "input[type='password']"
    SUBMIT_BUTTON   = "button[type='submit']"


class NavSelectors:
    # Navigating directly via URL - the span is display:none
    PARTNERS_PATH   = "/partners"


class PartnersPageSelectors:
    NEW_PARTNER_BUTTON  = "button:has-text('New partner')"
    SEARCH_INPUT        = "#search-partners"
    TABLE_ROW           = "tr.ant-table-row"
    PARTNER_NAME_CELL   = "span.Cq6YF"
    ACTION_BUTTON       = "#action-button"


class PartnerFormSelectors:
    # Text inputs - all have real IDs, CSS is clean
    NAME_INPUT          = "#name-field"
    ADDRESS_INPUT       = "#address-field"
    PHONE_INPUT         = "#phone-field"
    CONTACT_INPUT       = "#contact-person-field"
    DESCRIPTION_INPUT   = "#description-field"

    # Ant Design Select dropdowns - click the input to open
    TYPE_DROPDOWN       = "#partner-type-field"
    SERVICES_DROPDOWN   = "#service-types-field"
    SUBSCRIPTION_DROP   = "#subscription-tier-field"

    # Dropdown options
    TYPE_SERVICE_OPTION = "div[label='Service']"
    SERVICES_FIRST_OPT  = "span.fh8br"   # unique class to service type items only
    FIRST_DROPDOWN_OPT  = ".ant-select-dropdown:not(.ant-select-dropdown-hidden) .ant-select-item-option"

    # File upload - hidden input inside the upload div
    UPLOAD_INPUT        = "#image-upload-button input[type='file']"

    # Modal actions
    SAVE_BUTTON         = "#save-button"
    CANCEL_BUTTON       = "#cancel-button"

    # Modal container - used to wait for close
    MODAL_WRAPPER       = ".ant-modal-wrap"


class EditMenuSelectors:
    EDIT_BUTTON         = "#edit-button"
    DELETE_BUTTON       = "#delete-button"