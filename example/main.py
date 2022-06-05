from src.api.PyVault import PyVault

# Create a new PyVault object
vault = PyVault('config.toml')

# Signup with a PyVault account
vault.signup('test', 'password')
# vault.login('test', 'password')  # Uncomment to login instead

# Add an account to the vault
vault.add_account('test_account', 'this account is a test', 'username', 'pswd')

# Query 'test_account' from all accounts
print(vault.query_accounts('test_account'))

# Get and print the first test account
uid = vault.query_accounts('test_account')[0][0]
print(vault.get_account(uid))

# Logout of PyVault
vault.logout()
print(vault.query_accounts('test_account'))  # This should fail, no longer logged in
