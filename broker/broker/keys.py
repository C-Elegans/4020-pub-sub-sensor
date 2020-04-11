import os

file_dir = os.path.dirname(os.path.realpath(__file__))
example_key_dir = os.path.join(file_dir, "examplekeys")
example_private_key = os.path.join(example_key_dir, "private.pem")
example_public_key = os.path.join(example_key_dir, "public.pem")

class Keys:
    def __init__(self):
        self.enable_example = False
        self._keyfiles = {}

    def load_keys(self, keyid, private_path, public_path):
        if not self.enable_example:
            assert 'examplekeys' not in private_path
            assert 'examplekeys' not in public_path

        self._keyfiles[keyid] = (private_path, public_path)

    def load_example(self, keyid):
        assert self.enable_example
        self.load_keys(keyid, example_private_key, example_public_key)

    def get_private_key(self, keyid):
        if keyid not in self._keyfiles:
            return None
        private_path, public_path = self._keyfiles[keyid]
        with open(private_path, "r") as f:
            return f.read()

    def get_public_key(self, keyid):
        if keyid not in self._keyfiles:
            return None
        private_path, public_path = self._keyfiles[keyid]
        with open(public_path, "r") as f:
            return f.read()
