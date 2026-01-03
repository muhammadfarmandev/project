# Script to create/update admin user in database
# Uses backend/config.py for database connection
# Generates proper bcrypt password hash

import sys
import os

# Add backend to path so we can import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

try:
    import bcrypt
    import pyodbc
    from config import get_connection_string
    
    print("=" * 60)
    print("Admin User Creator/Updater")
    print("=" * 60)
    print()
    
    # Get admin details
    username = input("Enter admin username (default: admin): ").strip() or "admin"
    password = input("Enter admin password (default: admin123): ").strip() or "admin123"
    
    print()
    print("Generating password hash...")
    
    # Generate password hash
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    hash_string = hashed.decode('utf-8')
    
    print(f"✓ Hash generated: {hash_string[:50]}...")
    print()
    
    # Connect to database
    print("Connecting to database...")
    try:
        conn = pyodbc.connect(get_connection_string())
        cursor = conn.cursor()
        print("✓ Connected to database")
        print()
        
        # Check if admin exists
        cursor.execute("SELECT admin_id, username FROM Admin WHERE username = ?", (username,))
        existing = cursor.fetchone()
        
        if existing:
            print(f"Admin '{username}' already exists (ID: {existing[0]})")
            update = input("Update password? (y/n): ").strip().lower()
            
            if update == 'y':
                cursor.execute("""
                    UPDATE Admin 
                    SET password_hash = ? 
                    WHERE username = ?
                """, (hash_string, username))
                conn.commit()
                print(f"✓ Password updated for admin '{username}'")
            else:
                print("Cancelled. No changes made.")
                conn.close()
                sys.exit(0)
        else:
            # Insert new admin
            print(f"Creating new admin user '{username}'...")
            cursor.execute("""
                INSERT INTO Admin (username, password_hash)
                OUTPUT INSERTED.admin_id
                VALUES (?, ?)
            """, (username, hash_string))
            admin_id = cursor.fetchone()[0]
            conn.commit()
            
            print(f"✓ Admin created successfully!")
            print(f"  ID: {admin_id}")
            print(f"  Username: {username}")
        
        # Verify the admin
        cursor.execute("SELECT admin_id, username, password_hash FROM Admin WHERE username = ?", (username,))
        admin = cursor.fetchone()
        
        if admin:
            print()
            print("=" * 60)
            print("Verification:")
            print("=" * 60)
            print(f"  Admin ID: {admin[0]}")
            print(f"  Username: {admin[1]}")
            print(f"  Password Hash: {admin[2][:50]}...")
            
            # Test password
            test_result = bcrypt.checkpw(password.encode('utf-8'), admin[2].encode('utf-8'))
            print(f"  Password Test: {'✓ PASS' if test_result else '✗ FAIL'}")
            print()
            print("=" * 60)
            print("✓ Admin user is ready to use!")
            print(f"  Username: {username}")
            print(f"  Password: {password}")
            print("=" * 60)
        
        conn.close()
        
    except pyodbc.Error as e:
        print(f"✗ Database error: {e}")
        print()
        print("Make sure:")
        print("  1. SQL Server is running")
        print("  2. Database 'NSOS' exists")
        print("  3. Admin table exists (run schema.sql)")
        print("  4. Connection settings in backend/config.py are correct")
        sys.exit(1)
        
except ImportError as e:
    print(f"✗ Import error: {e}")
    print()
    print("Please install required packages:")
    print("  pip install bcrypt pyodbc")
    sys.exit(1)
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

