from unittest import TestCase
from unittest.mock import patch, AsyncMock
from asyncio import run, Future
# Import des classes
from main import DataRingRequest, Config, Notification, Errors, Logs


class TestDataRingRequests(TestCase):
    def test_test_dns(self):
        data1 = {
            "label": "Google",
            "enable": True,
            "dns": "google.fr",
            "priority": 4,
            "period": 5
        }
        data2 = {
            "label": "Googlo",
            "enable": True,
            "dns": "googlo.fro",
            "priority": 4,
            "period": 5
        }

        expected = {
            "label": "Google",
            "dns": "google.fr",
            "dns_exist": True,
            "dns_reachable": True,
            "ms": 50,
            "priority": 4,
            "period": 5
        }

        expected_error = {
            "label": "Googlo",
            "dns": "googlo.fro",
            "dns_reachable": False,
            "priority": 4,
            "period": 5
        }

        # Exécutez la méthode test_dns
        result = DataRingRequest().test_dns(label=data1["label"], dns=data1)

        # Supposer que ms vaut 50
        result["ms"] = 50

        # Vérifiez que le résultat est conforme aux attentes
        self.assertEqual(result, expected)
        result = DataRingRequest().test_dns(label=data2["label"], dns=data2)

        self.assertEqual(result, expected_error)


class TestConfig(TestCase):
    def test_tag_exist(self):
        self.assertEqual(Config().tag_exist(label="EPHEC"), True)

    def test_add_entry(self):
        c = Config()
        self.assertEqual(c.add_entry(label="to_delete", enable=1, dns="test.com", priority=1, period=5), None)
        self.assertEqual(c.save_config(), None)
        self.assertEqual(Config().tag_exist(label="to_delete"), True)

    def test_delete_entry(self):
        c = Config()
        self.assertEqual(c.delete_entry(label="to_delete"), None)
        self.assertEqual(c.save_config(), None)
        self.assertEqual(Config().tag_exist(label="to_delete"), False)


class TestNotification(TestCase):
    def test_send_notification(self):
        data = {
            "label": "TestUnitaire",
            "dns": "test.unitaire",
            "dns_exist": False,
            "dns_reachable": False,
            "ms": 999999,
            "priority": 4,
            "period": 5
        }
        self.assertEqual(Notification().send_discord_notif(label="TestUnitaire", data=data), 200)


class TestErrors(TestCase):
    def test_add(self):
        e = Errors()
        self.assertEqual(e.add(label="Google"), None)
        self.assertEqual("Google" in e.errors, True)
        self.assertEqual("France" in e.errors, False)

    def test_rem(self):
        e = Errors()
        self.assertEqual(e.add(label="France"), None)
        self.assertEqual("France" in e.errors, True)
        self.assertEqual(e.rem(label="France"), None)
        self.assertEqual("France" in e.errors, False)


class TestLogs(TestCase):
    def test_add(self):
        log = Logs()
        data = {
            "label": "TestUnitaire",
            "dns": "test.unitaire",
            "dns_exist": False,
            "dns_reachable": False,
            "ms": 999999,
            "priority": 4,
            "period": 5
        }
        data2 = {
            "label": "TestUnitaire2",
            "dns": "test.unitaire2",
            "dns_exist": True,
            "dns_reachable": True,
            "ms": 999999,
            "priority": 4,
            "period": 5
        }
        self.assertEqual(log.add(label="France", result=data), None)
        self.assertEqual(log.add(label="France2", result=data2), None)
