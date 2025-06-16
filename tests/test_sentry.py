from sentry_sdk import capture_message, capture_exception, set_user, set_context
from dotenv import load_dotenv
import sentry_sdk
import unittest
import os


load_dotenv()

SENTRY_DSN = os.getenv("SENTRY_DSN")

if not SENTRY_DSN:
    print("SENTRY_DSN is not defined. Sentry will not be initialized.")
else:
    print("Sentry initialized successfully.")

sentry_sdk.init(dsn=SENTRY_DSN, traces_sample_rate=1.0)


class TestSentryIntegration(unittest.TestCase):

    def test_caputure_message(self):
        try:
            capture_message("Test message: Sentry is working correctly")
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Failed to capture message: {e}")

    def test_capture_exception(self):
        try:
            try:
                1 / 0  # type: ignore
            except Exception as e:
                capture_exception(e)
                self.assertTrue(True)
        except Exception as e:
            self.fail(f"Failed to capture exception: {e}")

    def test_user_context(self):
        try:
            set_user(
                {"id": "12345", "email": "test_user@gmail.com", "username": "test_user"}
            )
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Failed to set user context: {e}")

    def test_custom_context(self):
        try:
            set_context(
                "custom_data",
                {"key1": "value1", "key2": "value2", "important_flag": True},
            )
            capture_message("Test message with custom context")
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Failed to set custom context: {e}")


if __name__ == "__main__":
    unittest.main()
