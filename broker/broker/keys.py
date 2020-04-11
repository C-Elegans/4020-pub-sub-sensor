

class Keys:
    def __init__(self):
        self.enable_example = False
        self._keyfiles = {}

    def load_keys(self, keyid, private_path, public_path):
        if not self.enable_example:
            assert 'examplekeys' not in private_path
            assert 'examplekeys' not in public_path

        self._keyfiles[keyid] = (private_path, public_path)

    def get_private_key(self, keyid):
        assert keyid in self._keyfiles
        private_path, public_path = self._keyfiles[keyid]
        with open(private_path, "r") as f:
            return f.read()

    def get_public_key(self, keyid):
        assert keyid in self._keyfiles
        private_path, public_path = self._keyfiles[keyid]
        with open(public_path, "r") as f:
            return f.read()
