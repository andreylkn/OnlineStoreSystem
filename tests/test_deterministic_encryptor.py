import unittest
from services.deterministic_encryptor import DeterministicEncryptor


class TestDeterministicEncryptor(unittest.TestCase):
    def setUp(self):
        self.key = b'1234567890123456'
        self.encryptor = DeterministicEncryptor(self.key)

    def test_encrypt_decrypt(self):
        plaintext = "HelloWorld"
        encrypted = self.encryptor.encrypt(plaintext)
        decrypted = self.encryptor.decrypt(encrypted)
        self.assertEqual(plaintext, decrypted)

if __name__ == '__main__':
    unittest.main()
