#!/usr/bin/env python3
import sqlite3
import json

def test_database_tokens():
    db_path = 'database/food_tokens.db'
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get first 5 tokens from database
        cursor.execute('SELECT name, token, food_preference, class_name, is_scanned FROM users LIMIT 5')
        users = cursor.fetchall()
        
        print("🔍 Database Test - First 5 Users:")
        print("=" * 60)
        
        for i, user in enumerate(users, 1):
            name, token, food_pref, class_name, is_scanned = user
            status = "✅ Available" if not is_scanned else "❌ Already Scanned"
            
            print(f"{i}. Name: {name}")
            print(f"   Class: {class_name}")
            print(f"   Food: {food_pref}")
            print(f"   Token: {token[:16]}...")
            print(f"   Status: {status}")
            print("-" * 40)
        
        # Get total counts
        cursor.execute('SELECT COUNT(*) FROM users')
        total_users = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM users WHERE is_scanned = 1')
        scanned_users = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM users WHERE food_preference = "veg"')
        veg_users = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM users WHERE food_preference = "non-veg"')
        nonveg_users = cursor.fetchone()[0]
        
        print(f"\n📊 Database Statistics:")
        print(f"   Total Users: {total_users}")
        print(f"   Scanned: {scanned_users}")
        print(f"   Available: {total_users - scanned_users}")
        print(f"   Vegetarian: {veg_users}")
        print(f"   Non-Vegetarian: {nonveg_users}")
        
        # Show sample QR data
        if users:
            sample_user = users[0]
            name, token, food_pref, class_name, is_scanned = sample_user
            
            qr_data = {
                "token": token,
                "name": name,
                "food_preference": food_pref,
                "class": class_name,
                "type": "food-token"
            }
            
            print(f"\n📱 Sample QR Code Data:")
            print(json.dumps(qr_data, indent=2))
            print(f"\n✅ This QR data should work with your scanner!")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_database_tokens()
