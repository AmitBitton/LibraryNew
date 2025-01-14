import hashlib

class User:

    def __init__(self, username,password:str):
        self.username=username
        self.password_hash=self._hash_password(password)

    @property
    def password_hash(self):
        return self._password_hash

    @password_hash.setter
    def password_hash(self, hash_value: str):
        self._password_hash = hash_value

    def _hash_password(self,password: str)->str:
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password: str) -> bool:
        return self._hash_password(password) == self.password_hash


