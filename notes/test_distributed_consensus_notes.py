"""Tests for distributed consensus notes."""
import unittest
try:
    from .distributed_consensus_notes import get_consensus_summary
except ImportError:
    from distributed_consensus_notes import get_consensus_summary


class TestNotes(unittest.TestCase):
    def test_summary_keys(self):
        summary = get_consensus_summary()
        self.assertIn("Leader Election", summary)
        self.assertIn("Log Replication", summary)


if __name__ == "__main__":
    unittest.main()
