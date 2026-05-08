import requests
import os
from dotenv import load_dotenv
from conftest import API_BASE_URL
from conftest import API_BASE_URL
load_dotenv()
API_BASE_URL = (
    os.getenv("BASE_URL") or
    os.getenv("API_BASE_URL") or
    "https://automationexercise.com"
)
class APIClient:
    """
    Reusable HTTP client for automationexercise.com API.
    Handles GET, POST, PUT, DELETE with status validation.
    Used across all API tests via pytest fixture.
    """

    def __init__(self):
        self.session = requests.Session()
        self.api_base_url = API_BASE_URL
        self.session.headers.update({
            "Content-Type":
                "application/x-www-form-urlencoded",
            "Accept": "application/json"
        })

    # ─────────────────────────────────────────
    # CORE HTTP METHODS
    # ─────────────────────────────────────────

    def get(self, endpoint, params=None):
        """
        HTTP GET request.
        Returns the full response object so tests
        can validate status_code, headers and body.
        """
        url = f"{self.api_base_url}{endpoint}"
        response = self.session.get(
            url, params=params
        )
        self._log(response)
        return response

    def post(self, endpoint, data=None):
        """
        HTTP POST request with form data.
        automationexercise API uses form encoding
        not JSON — important difference.
        """
        url = f"{self.api_base_url}{endpoint}"
        response = self.session.post(
            url, data=data
        )
        self._log(response)
        return response

    def put(self, endpoint, data=None):
        """HTTP PUT — update existing resource"""
        url = f"{self.api_base_url}{endpoint}"
        response = self.session.put(
            url, data=data
        )
        self._log(response)
        return response

    def delete(self, endpoint, data=None):
        """HTTP DELETE — remove a resource"""
        url = f"{self.api_base_url}{endpoint}"
        response = self.session.delete(
            url, data=data
        )
        self._log(response)
        return response

    # ─────────────────────────────────────────
    # STATUS CODE VALIDATORS
    # ─────────────────────────────────────────

    def assert_status(self, response, expected_code):
        """
        Core assertion — validates HTTP status code.
        Provides descriptive message on failure
        showing actual vs expected.
        """
        actual = response.status_code
        assert actual == expected_code, (
            f"\nURL:      {response.url}"
            f"\nExpected: {expected_code}"
            f"\nActual:   {actual}"
            f"\nBody:     {response.text[:200]}"
        )

    def assert_ok(self, response):
        """Assert 200 OK"""
        self.assert_status(response, 200)

    def assert_created(self, response):
        """Assert 201 Created"""
        self.assert_status(response, 201)

    def assert_bad_request(self, response):
        """Assert 400 Bad Request"""
        self.assert_status(response, 400)

    def assert_unauthorized(self, response):
        """Assert 401 Unauthorized"""
        self.assert_status(response, 401)

    def assert_not_found(self, response):
        """Assert 404 Not Found"""
        self.assert_status(response, 404)

    # ─────────────────────────────────────────
    # RESPONSE HELPERS
    # ─────────────────────────────────────────

    def get_json(self, response):
        """
        Parse response body as JSON.
        Returns None if body is not valid JSON.
        """
        try:
            return response.json()
        except ValueError:
            return None

    def get_response_code(self, response):
        """
        automationexercise API returns its own
        responseCode inside the JSON body —
        different from HTTP status code.
        e.g. {"responseCode": 200, "message": "..."}
        """
        body = self.get_json(response)
        if body and "responseCode" in body:
            return body["responseCode"]
        return None

    # ─────────────────────────────────────────
    # PRIVATE
    # ─────────────────────────────────────────

    def _log(self, response):
        """Log each request for debugging"""
        print(
            f"\n[API] {response.request.method} "
            f"{response.url} "
            f"→ {response.status_code}"
        )