class Entry:
    # Metadata
    uid: str
    name: str
    description: str

    # Login
    username: str
    password: str  # encrypted

    # Encryption metadata
    nonce: str
    tag: str

    def __init__(self, uid: str, name: str, description: str, username: str, password: str, nonce: str, tag: str):
        self.uid = uid
        self.name = name
        self.description = description
        self.username = username
        self.password = password
        self.nonce = nonce
        self.tag = tag

    def __str__(self):
        return f'''Account Entry:
- Uid: {self.uid}
- Name: {self.name}
- Description: {self.description}
- Username: {self.username}
- Password: {self.password}'''
