import unittest
from formats import formats  # Import the formats dictionary containing encoding classes


class TestChainedEncodings(unittest.TestCase):
    def setUp(self):
        # Initialize encoding format classes
        self.base64 = formats["base64"]()
        self.url = formats["url"]()
        self.hex = formats["hex"]()

    def test_single_encoding_decoding(self):
        """Test single encoding and decoding for backward compatibility."""
        data = "Hello, World!"

        # Base64
        encoded = self.base64.encode(data)
        decoded = self.base64.decode(encoded)
        self.assertEqual(decoded, data)

        # URL
        encoded = self.url.encode(data)
        decoded = self.url.decode(encoded)
        self.assertEqual(decoded, data)

        # Hex
        encoded = self.hex.encode(data)
        decoded = self.hex.decode(encoded)
        self.assertEqual(decoded, data)

    def test_chained_encoding_decoding(self):
        """Test chained encoding and decoding with multiple formats."""
        data = "Hello, World!"

        # Encode: URL -> Base64 -> Hex
        encoded = self.hex.encode(self.base64.encode(self.url.encode(data)))

        # Decode: Hex -> Base64 -> URL
        decoded = self.url.decode(self.base64.decode(self.hex.decode(encoded)))

        self.assertEqual(decoded, data)

    def test_empty_string(self):
        """Test encoding and decoding of an empty string."""
        data = ""

        # Encode: URL -> Base64 -> Hex
        encoded = self.hex.encode(self.base64.encode(self.url.encode(data)))

        # Decode: Hex -> Base64 -> URL
        decoded = self.url.decode(self.base64.decode(self.hex.decode(encoded)))

        self.assertEqual(decoded, data)

    def test_special_characters(self):
        """Test encoding and decoding of special characters."""
        data = "!@#$%^&*()_+-=[]{}|;':,.<>?/`~"

        # Encode: URL -> Base64 -> Hex
        encoded = self.hex.encode(self.base64.encode(self.url.encode(data)))

        # Decode: Hex -> Base64 -> URL
        decoded = self.url.decode(self.base64.decode(self.hex.decode(encoded)))

        self.assertEqual(decoded, data)

    def test_numeric_data(self):
        """Test encoding and decoding of numeric strings."""
        data = "1234567890"

        # Encode: URL -> Base64 -> Hex
        encoded = self.hex.encode(self.base64.encode(self.url.encode(data)))

        # Decode: Hex -> Base64 -> URL
        decoded = self.url.decode(self.base64.decode(self.hex.decode(encoded)))

        self.assertEqual(decoded, data)

    def test_large_data(self):
        """Test performance with large input data."""
        data = "A" * 10 ** 6  # 1 million characters

        # Encode: URL -> Base64 -> Hex
        encoded = self.hex.encode(self.base64.encode(self.url.encode(data)))

        # Decode: Hex -> Base64 -> URL
        decoded = self.url.decode(self.base64.decode(self.hex.decode(encoded)))

        self.assertEqual(decoded, data)


# Run the tests
if __name__ == "__main__":
    unittest.main()
