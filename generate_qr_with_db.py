#!/usr/bin/env python3
import csv
import qrcode
from PIL import Image, ImageDraw, ImageFont
import uuid
import os
import json
import sqlite3
from datetime import datetime

def create_qr_with_text(data, filename, student_name, food_preference, class_name):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    qr_img = qr.make_image(fill_color="black", back_color="white")
    
    img_width = 600
    img_height = 700
    
    final_img = Image.new('RGB', (img_width, img_height), 'white')
    
    qr_img = qr_img.resize((400, 400))
    
    qr_x = (img_width - 400) // 2
    qr_y = 50
    final_img.paste(qr_img, (qr_x, qr_y))
    
    draw = ImageDraw.Draw(final_img)
    
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
        font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    text_y = 470
    
    draw.text((img_width//2, text_y), student_name, font=font_large, fill='black', anchor='mm')
    text_y += 40
    
    draw.text((img_width//2, text_y), f"Class: {class_name}", font=font_medium, fill='black', anchor='mm')
    text_y += 30
    
    food_color = 'green' if 'veg' in food_preference.lower() and 'non' not in food_preference.lower() else 'red'
    food_text = f"Food: {food_preference}"
    draw.text((img_width//2, text_y), food_text, font=font_medium, fill=food_color, anchor='mm')
    text_y += 40
    
    draw.text((img_width//2, text_y), "Food Token - Sahyadri College", font=font_small, fill='gray', anchor='mm')
    text_y += 25
    
    draw.text((img_width//2, text_y), "Scan at food counter", font=font_small, fill='gray', anchor='mm')
    
    final_img.save(filename, 'JPEG', quality=95)

def extract_usn_from_email(email):
    """Extract USN from email address"""
    if not email:
        return None
    
    # Remove @sahyadri.edu.in part and get the username
    username = email.split('@')[0]
    
    # Convert to uppercase for consistency
    usn = username.upper()
    
    # Remove dots and common separators to get clean USN
    usn = usn.replace('.', '').replace('-', '').replace('_', '')
    
    # If it looks like a valid USN pattern, return it
    if len(usn) >= 6 and any(c.isdigit() for c in usn) and any(c.isalpha() for c in usn):
        return usn
    
    return None

def setup_database():
    db_path = 'database/food_tokens.db'
    os.makedirs('database', exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            food_preference TEXT NOT NULL CHECK(food_preference IN ('veg', 'non-veg')),
            token TEXT UNIQUE NOT NULL,
            qr_code_path TEXT,
            is_scanned BOOLEAN DEFAULT 0,
            scanned_at DATETIME,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            class_name TEXT,
            usn TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scan_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            scanned_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            scanner_info TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    print("✅ Database tables created/verified")
    return conn

def clear_existing_data(conn):
    cursor = conn.cursor()
    cursor.execute('DELETE FROM scan_history')
    cursor.execute('DELETE FROM users')
    conn.commit()
    print("🗑️ Cleared existing data from database")

def insert_user_to_db(conn, user_data):
    cursor = conn.cursor()
    
    food_pref = user_data['food_preference'].lower()
    if 'veg' in food_pref and 'non' not in food_pref:
        normalized_food_pref = 'veg'
    else:
        normalized_food_pref = 'non-veg'
    
    cursor.execute('''
        INSERT INTO users (name, email, food_preference, token, qr_code_path, class_name, usn)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        user_data['name'],
        user_data['email'],
        normalized_food_pref,
        user_data['token'],
        user_data['qr_code_path'],
        user_data['class'],
        user_data['usn']
    ))
    
    conn.commit()
    return cursor.lastrowid

def main():
    csv_file = 'food_pref_cleaned.csv'
    output_dir = 'qr_codes_jpeg'
    
    # Check if QR codes already exist
    if os.path.exists(output_dir) and os.listdir(output_dir):
        existing_files = [f for f in os.listdir(output_dir) if f.endswith('.jpg')]
        if existing_files:
            print(f"⚠️  Found {len(existing_files)} existing QR code files in {output_dir}/")
            response = input("🗑️ Delete existing QR codes and regenerate? (y/N): ").lower()
            if response != 'y':
                print("❌ Operation cancelled. Existing QR codes preserved.")
                return
            else:
                # Clear existing QR codes
                for file in existing_files:
                    os.remove(os.path.join(output_dir, file))
                print("🗑️ Cleared existing QR codes")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print(f"📊 Reading CSV file: {csv_file}")
    
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
    
    print(f"✅ Found {len(rows)} students")
    print(f"📁 Creating QR codes in directory: {output_dir}")
    
    conn = setup_database()
    
    # Check if database already has data
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM users')
    existing_users = cursor.fetchone()[0]
    
    if existing_users > 0:
        print(f"⚠️  Found {existing_users} existing users in database")
        response = input("🗑️ Clear existing database data? (y/N): ").lower()
        if response == 'y':
            clear_existing_data(conn)
        else:
            print("❌ Operation cancelled. Existing database data preserved.")
            conn.close()
            return
    
    tokens_data = []
    processed_students = set()  # Track processed students to avoid duplicates
    
    for i, row in enumerate(rows):
        name = row['Enter Your Name'].strip()
        email = row['Enter Your College Mail ID'].strip()
        usn = row['Enter Your USN'].strip().upper()  # Get USN directly from CSV
        class_name = row['Class'].strip()
        food_pref = row['What kind of food do you prefer'].strip()
        
        # Create unique identifier for student to avoid processing duplicates
        student_key = (name.lower(), email.lower(), usn.lower())
        
        if student_key in processed_students:
            print(f"⚠️  Skipping duplicate student: {name} ({email})")
            continue
        
        processed_students.add(student_key)
        
        # Use USN directly from CSV (no need to extract from email)
        # usn is already set above
        
        token = str(uuid.uuid4())
        
        qr_data = {
            "token": token,
            "name": name,
            "email": email,
            "food_preference": food_pref,
            "class": class_name,
            "type": "food-token"
        }
        
        sanitized_name = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).strip()
        sanitized_name = sanitized_name.replace(' ', '_')
        
        filename = f"{output_dir}/{sanitized_name}_{class_name.replace(' ', '_')}_{token[:8]}.jpg"
        qr_code_path = f"qr_codes_jpeg/{sanitized_name}_{class_name.replace(' ', '_')}_{token[:8]}.jpg"
        
        create_qr_with_text(json.dumps(qr_data), filename, name, food_pref, class_name)
        
        user_data = {
            'name': name,
            'email': email,
            'class': class_name,
            'food_preference': food_pref,
            'token': token,
            'qr_code_path': qr_code_path,
            'usn': usn
        }
        
        user_id = insert_user_to_db(conn, user_data)
        
        tokens_data.append({
            'id': user_id,
            'name': name,
            'email': email,
            'class': class_name,
            'food_preference': food_pref,
            'token': token,
            'filename': filename,
            'qr_code_path': qr_code_path
        })
        
        if len(tokens_data) % 50 == 0:
            print(f"⏳ Generated {len(tokens_data)}/{len(rows)} QR codes and saved to database...")
    
    with open(f'{output_dir}/tokens_list.json', 'w') as f:
        json.dump(tokens_data, f, indent=2)
    
    conn.close()
    
    unique_students = len(tokens_data)
    total_rows = len(rows)
    duplicates_skipped = total_rows - unique_students
    
    print(f"✅ Successfully generated {unique_students} QR codes!")
    if duplicates_skipped > 0:
        print(f"⚠️  Skipped {duplicates_skipped} duplicate entries from CSV")
    print(f"📁 Files saved in: {output_dir}/")
    print(f"📋 Token list saved as: {output_dir}/tokens_list.json")
    print(f"💾 All data saved to database: database/food_tokens.db")
    print(f"\n📈 SUMMARY:")
    
    veg_count = sum(1 for token in tokens_data if 'veg' in token['food_preference'].lower() and 'non' not in token['food_preference'].lower())
    non_veg_count = sum(1 for token in tokens_data if 'non' in token['food_preference'].lower())
    
    print(f"🥗 Veg QR codes: {veg_count}")
    print(f"🍖 Non-Veg QR codes: {non_veg_count}")
    print(f"📊 Total QR codes: {unique_students}")
    print(f"\n🚀 Ready to use with your Node.js application!")
    print(f"   - Start server: npm start")
    print(f"   - Scanner: http://localhost:3000/scanner")
    print(f"   - Admin: http://localhost:3000/admin")

if __name__ == "__main__":
    main()
