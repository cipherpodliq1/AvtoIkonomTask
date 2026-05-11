# AvtoIkonom QA Automation

![E2E Tests](https://github.com/cipherpodliq1/AvtoIkonomTask/actions/workflows/e2e.yml/badge.svg)

End-to-end automation suite for the [AvtoIkonom](https://dev.admin.avtoikonom.com) admin platform, built with **Playwright + Python**.

---

## Overview

This project was built as a QA automation assignment covering the partner management flow of the AvtoIkonom admin platform. The goal was not to write the most tests, but to build a framework that is stable, maintainable, and reflects how a real production automation project would be structured.

The suite covers two test scenarios:

- **TC-01** — Create a new partner with all required fields and verify persistence
- **TC-02** — Edit an existing partner and verify the changes are saved *(bonus)*

---

## Engineering Decisions

### Playwright + Python

Playwright was chosen over Cypress as it offers better support for complex UI interactions such as file uploads, custom dropdown components, and Google Maps autocomplete. Python was chosen for readability and natural language test structure.

### Page Object Model — Lean by Design

The project uses a three-file POM:

- `login_page.py`
- `partners_page.py`
- `partner_form_page.py`

No inheritance chains, no base class abstractions. Each page object exposes only what the tests actually need. Over-engineering a POM for a small suite makes the code harder to read, not easier.

### Centralised Selector File

Every selector in the suite lives exclusively in `selector/selectors.py`. No selector string appears anywhere else in the codebase.

**Why this matters in practice:**

When the UI changes (and it always does), you update one file and the entire suite is healed. No grep across the codebase, no risk of missing an occurrence. Selectors are also named semantically, which makes test code self-documenting — `PartnerFormSelectors.SAVE_BUTTON` tells you more than `"button.ant-btn-primary"` ever could.

**Selector priority:**

1. ID attributes (`#name-field`) — most stable, tied to developer intent
2. CSS with meaningful attributes (`input[name='file-upload']`)
3. CSS `:has()` scoping for Ant Design dropdowns
4. Text-based Playwright selectors (`:has-text()`) for buttons
5. XPath — only when no CSS hook exists

### Ant Design Dropdown Strategy

The platform uses Ant Design's virtual select component, which renders dropdown options in DOM portals. This means a global `.ant-select-item-option` selector matches options from all dropdowns simultaneously, causing instability.

The fix was to scope every dropdown interaction to its specific container using CSS `:has()`:

```python
container = page.locator("div.ant-select:has(#subscription-tier-field)")
container.click()
container.locator(".ant-select-item-option").first.click()
```

This ensures that clicking an option in the subscription dropdown never accidentally hits an option from the type or services dropdown.

### Session-Scoped Authentication

Login runs exactly once per test session. The browser state (cookies, localStorage) is saved to `auth.json` after the first login and restored for every subsequent test via Playwright's `storage_state`.

**Why this matters:**

- Faster test execution — no repeated login flows
- More realistic — mirrors how a real user session works
- Isolated failure point — if auth breaks, it breaks once, clearly

### Unique Test Data per Run

Partner names are generated with a timestamp and random suffix:

```
AutoTest Partner 20260509-171257-tvcluf
```

This prevents test collisions on the shared development environment. If two engineers run the suite simultaneously, their data never interferes. It also makes cleanup trivial — filter by `AutoTest` to find and remove all test-generated data.

### No `time.sleep()` Anywhere

All waiting is done through Playwright's built-in mechanisms:

- `wait_for_selector(state="visible")` — wait for an element to appear
- `wait_for_selector(state="hidden")` — wait for an element to disappear
- `expect(locator).to_be_visible()` — assertion with built-in retry
- `locator.wait_for(state="visible")` — pre-click stability check

Hard sleeps make tests slow and brittle. If the application is slow on a given day, a `sleep(2)` either wastes time when the app is fast or causes flakiness when it is slow.

### Google Maps Autocomplete Handling

The Address field uses Google Places Autocomplete (`pac-target-input`). Typing text alone is not enough — the form validates that an address was selected from the dropdown, not just typed.

The solution types the address string and then waits for and clicks the first `.pac-item` suggestion:

```python
self.page.locator(PartnerFormSelectors.ADDRESS_INPUT).fill(address)
self.page.wait_for_selector(".pac-item", state="visible", timeout=5000)
self.page.locator(".pac-item").first.click()
```

### Logo Upload and Crop Modal

The logo upload field is a hidden `input[type='file']` sibling of the visible upload button. After a file is set, the application opens a ReactCrop modal for image editing. The crop modal must be confirmed before the main form can be submitted.

The crop save button is identified by the absence of an `id` attribute on its inner span (unlike the main form save button which has `id="save-button"`), and filtered by text to distinguish it from the crop cancel button:

```python
crop_save = page.locator("button:has(span.J9zkR:not([id]))").filter(has_text="Save")
```

A committed `fixtures/test_logo.png` ensures the test is fully self-contained and reproducible on any machine.

### Persistence Assertions

Every write operation (create, edit) is followed by a `page.reload()` and a re-assertion of the data. This confirms that the data was actually saved to the backend and is not just held in frontend state.

---

## Project Structure

```
avtoikonom-qa/
│
├── selector/
│   └── selectors.py          # Every selector in the project lives here
│
├── pages/
│   ├── login_page.py         # Login flow and auth assertion
│   ├── partners_page.py      # Partners list navigation and assertions
│   └── partner_form_page.py  # Partner create/edit form interactions
│
├── tests/
│   ├── test_create_partner.py   # TC-01 core required test
│   └── test_edit_partner.py     # TC-02 bonus test
│
├── utils/
│   ├── test_data.py          # Environment constants and fixed spec values
│   └── helpers.py            # Reusable wait and assertion utilities
│
├── fixtures/
│   └── test_logo.png         # Committed test image for logo upload
│
├── .github/
│   └── workflows/
│       └── e2e.yml           # GitHub Actions CI/CD pipeline
│
├── conftest.py               # Session auth fixture, page fixture, test data factory
├── pytest.ini                # Timeout, markers, test settings
├── requirements.txt          # Pinned dependencies
├── .env.example              # Environment variable template
└── README.md
```

---

## Test Coverage

### TC-01 — Create Partner (`tests/test_create_partner.py`)

| Step | Action | Assertion |
|------|--------|-----------|
| 1 | Navigate to `/partners` | Partners table is visible |
| 2 | Click New partner | Form modal opens |
| 3 | Fill Name | — |
| 4 | Select Type = Service | — |
| 5 | Select first available Service | — |
| 6 | Select first available Subscription plan | — |
| 7 | Type address, select from autocomplete | — |
| 8 | Fill Telephone | — |
| 9 | Fill Contact person | — |
| 10 | Fill Description | — |
| 11 | Upload logo, confirm crop modal | — |
| 12 | Click Save | Form modal closes |
| 13 | — | Partner name visible in table |
| 14 | Reload page | Partner name still visible after reload |

### TC-02 — Edit Partner (`tests/test_edit_partner.py`) — Bonus

| Step | Action | Assertion |
|------|--------|-----------|
| 1 | Create a partner (same as TC-01) | Partner visible in table |
| 2 | Open three dot menu on partner row | — |
| 3 | Click Edit | Edit form opens pre-populated |
| 4 | Update Contact person field | — |
| 5 | Click Save | Form modal closes |
| 6 | — | Partner row still present |
| 7 | — | Updated contact person visible in row |
| 8 | Reload page | Updated value persists after reload |

---

## Prerequisites

- Python 3.11+
- pip

---

## Installation

```bash
pip install -r requirements.txt
playwright install chromium
```

---

## Configuration

```bash
cp .env.example .env
```

The `.env.example` already contains the test environment credentials. No changes needed.

---

## Running Tests

```bash
# Full suite
pytest tests/ -v

# Core test only
pytest tests/test_create_partner.py -v

# Bonus test only
pytest tests/test_edit_partner.py -v

# Watch mode — opens a real browser
pytest tests/ -v --headed

# Smoke tests only
pytest tests/ -v -m smoke
```

---

## CI/CD

The pipeline runs automatically on every push to `main` and every pull request. It can also be triggered manually from the **Actions** tab in GitHub using `workflow_dispatch` — useful for reviewers who want to see the tests run live without cloning the project.

**Pipeline steps:**

1. Checkout code
2. Set up Python 3.11
3. Install Python dependencies
4. Install Chromium browser
5. Run full test suite
6. Upload HTML report as artifact
7. Upload Playwright traces on failure

**Required GitHub Secrets:**

| Secret | Value |
|--------|-------|
| `BASE_URL` | `https://dev.admin.avtoikonom.com` |
| `QA_EMAIL` | `test_qa_1@example.com` |
| `QA_PASSWORD` | `test_qa_1@example.com` |

---

## QA Practices Applied

**Stable selectors** — ID-first selector strategy with all selectors centralised in one file. When the UI changes, one file changes.

**Test isolation** — Each test generates its own unique data and does not depend on state left by another test. TC-02 creates its own partner rather than relying on TC-01 having run first.

**Meaningful failure messages** — Assertions include descriptive messages so that when a test fails in CI, the log tells you exactly what was expected and what was missing, without opening the source code.

**No hard waits** — Zero `time.sleep()` calls. All synchronisation is done through Playwright's event-driven waiting mechanisms.

**Persistence verification** — Every create and edit operation is followed by a page reload to confirm the data survived a round trip to the backend.

**Session reuse** — Authentication runs once per session and is shared across all tests via `storage_state`, keeping the suite fast and the login flow as a single potential failure point.

**Committed test fixtures** — The `test_logo.png` file is committed to the repository, making the suite fully self-contained. A reviewer can clone and run without any additional setup beyond `pip install`.

**Pinned dependencies** — All packages in `requirements.txt` are version-pinned to ensure identical behaviour across local machines, CI runners, and reviewer environments.
