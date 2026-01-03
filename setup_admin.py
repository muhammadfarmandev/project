# Simple script to generate admin password hash
# Run this to get the hash for admin123 password
# Usage: python setup_admin.py

import bcrypt

password = "admin123"
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
hash_string = hashed.decode('utf-8')

print("=" * 60)
print("Admin Password Hash Generator")
print("=" * 60)
print(f"\nPassword: {password}")
print(f"\nGenerated Hash:")
print(hash_string)
print("\n" + "=" * 60)
print("\nTo use this hash:")
print("1. Run the schema.sql file in SQL Server")
print("2. Update the Admin table with this hash:")
print(f"   UPDATE Admin SET password_hash = '{hash_string}' WHERE username = 'admin';")
print("\nOr update the INSERT statement in schema.sql before running it.")
print("=" * 60)

