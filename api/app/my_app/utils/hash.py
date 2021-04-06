import os
import hashlib
from hashids import Hashids


FLASK_SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")

def hash_id(seed: int):
    hashids = Hashids(salt=FLASK_SECRET_KEY, min_length=16)
    return hashids.encode(seed)

def sha256(hash_string):
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature