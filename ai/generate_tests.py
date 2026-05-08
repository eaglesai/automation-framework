# generate_tests.py
# ---------------------------------------------------------------
# AI-powered BDD test generator
#
# HOW TO USE:
#   python ai/generate_tests.py --page pages/cart_page.py
#
# WHAT IT DOES:
#   1. Reads your page object file
#   2. Logs the start of generation with timestamp
#   3. Sends the page object to Claude API
#   4. Claude generates a .feature file and step definitions
#   5. Saves both files directly into your BDD folders
#   6. Logs every step with timestamps
# ---------------------------------------------------------------

import os
import sys
import json
import argparse
from datetime import datetime
import anthropic
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------
# CONFIGURATION
# Where generated files are saved
# ---------------------------------------------------------------
FEATURES_DIR    = "tests/bdd/features"
STEP_DEFS_DIR   = "tests/bdd/step_defs"
LOG_DIR         = "ai/logs"
LOG_FILE        = "ai/logs/generation_log.txt"
BACKUP_DIR      = "ai/generated"


# ---------------------------------------------------------------
# LOGGER
# Writes timestamped messages to both the console and log file
# ---------------------------------------------------------------
def log(message: str):
    """
    Writes a timestamped message to:
      - The terminal (so you can watch it run)
      - ai/logs/generation_log.txt (permanent record)
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_message = f"[{timestamp}] {message}"

    # Print to terminal
    print(full_message)

    # Append to log file
    os.makedirs(LOG_DIR, exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(full_message + "\n")


# ---------------------------------------------------------------
# READ PAGE OBJECT FILE
# ---------------------------------------------------------------
def read_page_file(page_path: str) -> str:
    """
    Reads the page object Python file and returns its content
    as a string. This is what gets sent to Claude.
    """
    if not os.path.exists(page_path):
        log(f"ERROR: File not found: {page_path}")
        sys.exit(1)

    with open(page_path, "r", encoding="utf-8") as f:
        content = f.read()

    log(f"Read page object file: {page_path} ({len(content)} characters)")
    return content


# ---------------------------------------------------------------
# BUILD THE PROMPT
# This is the instruction we send to Claude
# ---------------------------------------------------------------
def build_prompt(page_content: str, page_name: str) -> str:
    """
    Builds the prompt that tells Claude exactly what to generate
    and in what format.
    """
    return f"""
You are a senior test automation engineer.

I will give you a Selenium Page Object Model class written in Python.
Your job is to generate two things:

1. A pytest-bdd Gherkin .feature file
2. A pytest-bdd step definitions .py file

RULES FOR THE FEATURE FILE:
- Use pure business language — no mention of Selenium, Python, or APIs
- Include a Feature description with As a / I want / So that
- Include a Background section if there is a common setup step
- Write 3 to 4 meaningful Scenario blocks
- Cover: happy path, failure case, and edge cases
- Use Given / When / Then / And format correctly

RULES FOR THE STEP DEFINITIONS FILE:
- Import allure, pytest_bdd, and the page object class
- Every step function must have an @allure.step decorator
- Use the driver and test_data fixtures as parameters where needed
- Keep code at intermediate level — clear and readable
- Add a short comment above each step explaining what it does
- Match the coding style of this example step:

@when("I add a product to the cart")
@allure.step("User adds product to cart")
def add_product_to_cart(driver):
    # UI STEP - Selenium clicks the add to cart button
    cart_page = CartPage(driver)
    cart_page.add_to_cart()

OUTPUT FORMAT — respond with ONLY this JSON structure, nothing else:
{{
  "feature_file": "full content of the .feature file here",
  "step_file": "full content of the step definitions .py file here"
}}

Here is the page object file named {page_name}:

{page_content}
"""


# ---------------------------------------------------------------
# CALL CLAUDE API
# ---------------------------------------------------------------
def call_claude(prompt: str) -> dict:
    """
    Sends the prompt to Claude API and returns the parsed JSON
    response containing the feature file and step definitions.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        log("ERROR: ANTHROPIC_API_KEY not found in .env file")
        sys.exit(1)

    log("Connecting to Claude API...")

    client = anthropic.Anthropic(api_key=api_key)

    log("Sending page object to Claude — waiting for response...")

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4000,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    log("Claude API responded successfully")

    # Extract the raw text response
    raw_response = message.content[0].text

    # Parse the JSON from the response
    try:
        result = json.loads(raw_response)
    except json.JSONDecodeError:
        # Sometimes the model wraps JSON in markdown code blocks
        # Strip them out and try again
        cleaned = raw_response.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("```")[1]
            if cleaned.startswith("json"):
                cleaned = cleaned[4:]
        result = json.loads(cleaned.strip())

    return result


# ---------------------------------------------------------------
# SAVE GENERATED FILES
# ---------------------------------------------------------------
def save_files(result: dict, page_name: str):
    """
    Saves the generated files to:
      - tests/bdd/features/         (live location, ready to run)
      - tests/bdd/step_defs/        (live location, ready to run)
      - ai/generated/               (backup copy with timestamp)
    """
    # Build file names from the page name
    # e.g. cart_page.py → cart
    base_name = page_name.replace("_page.py", "").replace(".py", "")
    feature_filename  = f"{base_name}.feature"
    step_filename     = f"test_{base_name}_steps.py"
    timestamp         = datetime.now().strftime("%Y%m%d_%H%M%S")

    # ── Save feature file ──────────────────────────────────────
    feature_path = os.path.join(FEATURES_DIR, feature_filename)
    os.makedirs(FEATURES_DIR, exist_ok=True)

    with open(feature_path, "w", encoding="utf-8") as f:
        f.write(result["feature_file"])

    log(f"Saved feature file: {feature_path}")

    # ── Save step definitions file ─────────────────────────────
    step_path = os.path.join(STEP_DEFS_DIR, step_filename)
    os.makedirs(STEP_DEFS_DIR, exist_ok=True)

    with open(step_path, "w", encoding="utf-8") as f:
        f.write(result["step_file"])

    log(f"Saved step definitions: {step_path}")

    # ── Save backup copies with timestamp ──────────────────────
    backup_path = os.path.join(BACKUP_DIR, timestamp)
    os.makedirs(backup_path, exist_ok=True)

    with open(os.path.join(backup_path, feature_filename), "w", encoding="utf-8") as f:
        f.write(result["feature_file"])

    with open(os.path.join(backup_path, step_filename), "w", encoding="utf-8") as f:
        f.write(result["step_file"])

    log(f"Backup saved to: {backup_path}")

    return feature_path, step_path


# ---------------------------------------------------------------
# MAIN — entry point
# ---------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="AI BDD Test Generator — powered by Claude"
    )
    parser.add_argument(
        "--page",
        required=True,
        help="Path to the page object file. Example: pages/cart_page.py"
    )
    args = parser.parse_args()

    page_path = args.page
    page_name = os.path.basename(page_path)

    # ── Log session start ──────────────────────────────────────
    log("=" * 60)
    log(f"AI Test Generation Started")
    log(f"Input file : {page_path}")
    log("=" * 60)

    # ── Step 1: Read the page object file ─────────────────────
    page_content = read_page_file(page_path)

    # ── Step 2: Build the prompt ───────────────────────────────
    log("Building prompt for Claude...")
    prompt = build_prompt(page_content, page_name)

    # ── Step 3: Call Claude API ────────────────────────────────
    result = call_claude(prompt)

    # ── Step 4: Save the generated files ──────────────────────
    feature_path, step_path = save_files(result, page_name)

    # ── Log session end ────────────────────────────────────────
    log("=" * 60)
    log("Generation Complete")
    log(f"Feature file : {feature_path}")
    log(f"Step defs    : {step_path}")
    log(f"Run with     : pytest {step_path} -v")
    log("=" * 60)


if __name__ == "__main__":
    main()
