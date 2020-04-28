import os
import re

file_dir = os.path.dirname(os.path.realpath(__file__))
example_key_dir = os.path.join(file_dir, "examplekeys")
example_private_key = os.path.join(example_key_dir, "private.pem")
example_public_key = os.path.join(example_key_dir, "public.pem")

class Keys:
    def __init__(self):
        self.enable_example = False
        self._private_keys = {}
        self._public_keys = {}

    def load_keys(self, keyid, private_path, public_path):
        self.load_private_key(keyid, private_path)
        self.load_public_key(keyid, public_path)

    def load_private_key(self, keyid, private_path):
        if not self.enable_example:
            assert 'examplekeys' not in private_path
        self._private_keys[keyid] = private_path

    def load_public_key(self, keyid, public_path):
        if not self.enable_example:
            assert 'examplekeys' not in public_path
        self._public_keys[keyid] = public_path

    def load_example(self, keyid):
        assert self.enable_example
        self.load_keys(keyid, example_private_key, example_public_key)

    def get_private_key(self, keyid):
        if keyid not in self._private_keys:
            return None
        private_path = self._private_keys[keyid]
        with open(private_path, "r") as f:
            return f.read()

    def get_public_key(self, keyid):
        if keyid not in self._public_keys:
            return None
        public_path = self._public_keys[keyid]
        with open(public_path, "r") as f:
            return f.read()

    def load_keys_from_directory(self, dirname):
        files = os.listdir(dirname)
        print(files)
        for f in files:
            fpath = os.path.join(dirname, f)
            m = re.search(r'(.*)_priv.pem', f)
            if m:
                self.load_private_key(m[1], fpath)
            m = re.search(r'(.*)_pub.pem', f)
            if m:
                self.load_public_key(m[1], fpath)
