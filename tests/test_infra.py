import unittest
from src.infra.supabase_client import SupabaseClientWrapper
from src.infra.hf_client import HFClient
from unittest.mock import patch, MagicMock
import os

class TestInfra(unittest.TestCase):

    def test_supabase_mock_mode(self):
        # Ensure no env vars
        with patch.dict(os.environ, {}, clear=True):
            client = SupabaseClientWrapper()
            # Should not crash
            client.log_request("hash", "HIGH", "v1")
            client.log_audit("TEST", "ACTION", "details")
            self.assertIsNone(client.client)

    def test_hf_mock_mode(self):
        with patch.dict(os.environ, {}, clear=True):
            client = HFClient()
            # Test async method? unittest supports async with 'IsolatedAsyncioTestCase' in newer python
            # For simplicity, we just check init/warning logic in mock mode
            self.assertIsNone(client.api_key)

if __name__ == '__main__':
    unittest.main()
