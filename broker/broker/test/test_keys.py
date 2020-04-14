import unittest
import os
from broker.keys import Keys

file_dir = os.path.dirname(os.path.realpath(__file__))
example_key_dir = os.path.join(os.path.basename(file_dir), "examplekeys")
example_private_key = os.path.join(example_key_dir, "private.pem")
example_public_key = os.path.join(example_key_dir, "public.pem")

class KeysTestCase(unittest.TestCase):

    def test_disabled_example(self):
        keys = Keys()
        with self.assertRaises(AssertionError):
            keys.load_keys("ex", example_private_key, example_public_key)

    def test_enabled_example(self):
        keys = Keys()
        keys.enable_example = True
        keys.load_keys("ex", example_private_key, example_public_key)
        assert('ex' in keys._private_keys)
        assert('ex' in keys._public_keys)

if __name__ == "__main__":
    unittest.main()
