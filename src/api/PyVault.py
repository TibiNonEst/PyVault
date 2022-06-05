import uuid

import argon2.exceptions
from Crypto.Cipher import ChaCha20_Poly1305
from argon2 import PasswordHasher

import src.api.Utils as Utils
from src.api.Config import Config
from src.api.Database import Database
from src.api.Entry import Entry
from src.api.State import State


class PyVault:
    """The main PyVault class"""
    def __init__(self, config_file):
        self.config = Config(config_file)
        self.db = Database(self.config)
        self.hasher = PasswordHasher()
        self.state = State()

    def signup(self, username: str, password: str):
        """Create a PyVault account"""
        if self.db.get_user_by_username(username):
            return print('Signup failed: A user with that username already exists.')

        uid = uuid.uuid4().hex

        self.db.add_user(uid, username, self.hasher.hash(password))

        print(f'Successfully signed up as {username}.')
        self.login(username, password)

    def login(self, username: str, password: str):
        """Login to a PyVault account"""
        if not self.db.get_user_by_username(username):
            return print('Login failed: User could not be found.')

        uid, username, hashed = self.db.get_user_by_username(username)

        try:
            self.hasher.verify(hashed, password)
        except argon2.exceptions.VerificationError:
            return print('Login failed: Password is incorrect.')

        if self.hasher.check_needs_rehash(hashed):
            p_hash = self.hasher.hash(password)
            self.db.update_hash(uid, p_hash)

        self.state.logged_in = True
        self.state.uid = uid
        self.state.username = username
        self.state.hashed = hashed
        self.state.key = Utils.hash_to_bytes(hashed)

        print(f'Successfully logged in as {username}.')

    def logout(self):
        self.state = State()
        print('Logged out.')

    def add_account(self, name: str, description: str, username: str, password: str):
        """Add an account to the vault"""
        if not self.state.logged_in:
            return print('Error: Not logged in.')

        cipher = ChaCha20_Poly1305.new(key=self.state.key)

        uid = uuid.uuid4().hex
        password, tag = cipher.encrypt_and_digest(password.encode('utf-8'))
        entry = Entry(uid, name, description, username, password.hex(), cipher.nonce.hex(), tag.hex())

        self.db.add_account(self.state.uid, entry)

    # TODO: account editing
    def edit_account(self):
        """Edit an account in the vault"""
        pass

    def delete_account(self, uid: str):
        """Delete an account from the vault"""
        if not self.state.logged_in:
            return print('Error: Not logged in.')

        self.db.delete_account(self.state.uid, uid)

    def get_account(self, uid: str):
        """Get an account by its uid"""
        account = Entry(*self.db.get_account_by_uid(self.state.uid, uid))
        cipher = ChaCha20_Poly1305.new(key=self.state.key, nonce=bytes.fromhex(account.nonce))
        account.password = cipher.decrypt_and_verify(bytes.fromhex(account.password), bytes.fromhex(account.tag)).decode('utf-8')

        return account

    def query_accounts(self, query: str):
        """Query all accounts from the vault"""
        if not self.state.logged_in:
            return print('Error: Not logged in.')

        return self.db.get_accounts(self.state.uid, query)
