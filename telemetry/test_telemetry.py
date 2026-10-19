# Created by 11Hopem
# Copyright (c) 2026 11Hopem. All rights reserved.
# Licensed under 11Hopem Proprietary License.

import unittest
import tempfile
import os
import json
import sys

# Ensure root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from telemetry.firebase_config import FIREBASE_ECOSYSTEM_CONFIG
from telemetry.logger import TelemetryLogger, scrub_sensitive_data, to_firestore_fields

class TestTelemetryLogger(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.logger = TelemetryLogger(
            app_name="git-bot-test",
            app_version="1.0.0",
            log_dir=self.temp_dir.name
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_firebase_config(self):
        self.assertEqual(FIREBASE_ECOSYSTEM_CONFIG["account"], "umutocgdr@gmail.com")
        self.assertEqual(FIREBASE_ECOSYSTEM_CONFIG["project_id"], "hopem-software-cloud")
        self.assertTrue("hopem-software-cloud" in FIREBASE_ECOSYSTEM_CONFIG["firestore_base_url"])

    def test_log_writing_and_local_custody(self):
        entry = self.logger.info("Auto sync cycle completed", {"sync_count": 5})
        self.assertEqual(entry["level"], "INFO")
        self.assertEqual(entry["app_name"], "git-bot-test")
        self.assertEqual(entry["context"]["sync_count"], 5)
        self.assertEqual(entry["target_collection"], "app_logs")

        error_entry = self.logger.error("Git push rejected", {"remote": "origin"})
        self.assertEqual(error_entry["level"], "ERROR")

        # Verify JSONL file exists and is populated
        self.assertTrue(os.path.exists(self.logger.log_file))
        with open(self.logger.log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 2)
            parsed = json.loads(lines[0])
            self.assertEqual(parsed["message"], "Auto sync cycle completed")

    def test_scrub_sensitive_data(self):
        dirty = {
            "password": "SuperSecretPassword",
            "api_key": "AIzaSySecret",
            "token": "Bearer eyJhbGciOi...",
            "user": {
                "tckn": "12345678901",
                "credit_card": "4543 1234 5678 9012"
            },
            "msg": "Found TCKN 12345678901 and card 4543 1234 5678 9012 with Bearer token-xyz"
        }
        clean = scrub_sensitive_data(dirty)
        self.assertEqual(clean["password"], "***REDACTED***")
        self.assertEqual(clean["api_key"], "***REDACTED***")
        self.assertEqual(clean["token"], "***REDACTED***")
        self.assertEqual(clean["user"]["tckn"], "***REDACTED***")
        self.assertEqual(clean["user"]["credit_card"], "***REDACTED***")
        self.assertNotIn("12345678901", clean["msg"])
        self.assertNotIn("4543 1234 5678 9012", clean["msg"])
        self.assertNotIn("token-xyz", clean["msg"])

    def test_to_firestore_fields(self):
        fields = to_firestore_fields({
            "appName": "git-bot",
            "commits": 10,
            "rate": 2.5,
            "active": True,
            "empty": None,
            "nested": {"key": "val"}
        })
        self.assertEqual(fields["appName"], {"stringValue": "git-bot"})
        self.assertEqual(fields["commits"], {"integerValue": "10"})
        self.assertEqual(fields["rate"], {"doubleValue": 2.5})
        self.assertEqual(fields["active"], {"booleanValue": True})
        self.assertEqual(fields["empty"], {"nullValue": None})
        self.assertIn("key", fields["nested"]["stringValue"])

    def test_multi_collection_routing(self):
        sec = self.logger.security("SSH key change detected", {"ip": "10.0.0.1"})
        self.assertEqual(sec["target_collection"], "security_audit_logs")

        tel = self.logger.telemetry("Repository sync latency", {"latency_ms": 150})
        self.assertEqual(tel["target_collection"], "telemetry_logs")

        vis = self.logger.visitor("User accessed git web dashboard", {"user": "admin"})
        self.assertEqual(vis["target_collection"], "visitor_logs")

        cr = self.logger.crash("Daemon thread crashed", {"thread_id": 1})
        self.assertEqual(cr["target_collection"], "crash_logs")

        perf = self.logger.performance("git_status", 45)
        self.assertEqual(perf["target_collection"], "telemetry_logs")

    def test_zero_crash_guarantee(self):
        res1 = self.logger.log(None, None)
        self.assertIsNotNone(res1)
        res2 = self.logger.error(Exception("Test failure"))
        self.assertIsNotNone(res2)

if __name__ == "__main__":
    unittest.main()
