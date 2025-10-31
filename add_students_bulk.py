#!/usr/bin/env python3
import sqlite3, qrcode, json, uuid, os
from datetime import datetime

students = [
    ("Akshay Ks","4SF24IS008","akshay.ks.is24@sahyadri.edu.in","ISE 3A","non-veg"),
    ("Madeeha Zahoor","4SF23IS055","madeeha.is23@sahyadri.edu.in","ISE 5B","non-veg"),
    ("Shivaraj Sadashiv Chigare","4SF23CD404","shivaraj.ds22@sahyadri.edu.in","7DS","veg"),
    ("SINCHANA S NAIK","4SF22CD044","sinchanas.ds22@sahaydri.edu.in","7DS","non-veg"),
    ("Rm Raja Subramanian","4SF24IS081","raja.rm.ise@sahyadri.edu.in","ISE 3A","non-veg"),
    ("Shifa Kouser","4SF22CD041","shifakouser8618@gmail.com","7DS","veg"),
    ("Abdul shaz","4SF23IS002","abdulshaz.is23@sahyadri.edu.in","ISE 5A","non-veg"),
    ("Tarun G","4SF22CD053","tarun.ds22@sahyadri.edu.in","7DS","non-veg"),
    ("Rushil","4SF23IS014","amin.is23@sahyadri.edu.in","IS 5B","veg"),
    ("Winston Felix Fernandes","4SF22CD059","Winstonfelixfernandes@gmail.com","7DS","non-veg"),
]

os.makedirs('qr_codes_jpeg', exist_ok=True)
conn = sqlite3.connect('database/food_tokens.db')
cursor = conn.cursor()

added = []
skipped = []

for name, usn, email, class_name, food_pref in students:
    # Normalize food preference
    fp = food_pref.strip().lower()
    if fp in ['veg','vegetarian']:
        fp_db = 'veg'
    else:
        fp_db = 'non-veg'

    # Check existing
    cursor.execute('SELECT id FROM users WHERE usn = ? OR email = ?', (usn, email))
    if cursor.fetchone():
        skipped.append((name, usn, email, 'exists'))
        continue

    token = str(uuid.uuid4())
    created_at = datetime.now().isoformat()
    qr_data = json.dumps({
        'token': token,
        'name': name,
        'email': email,
        'food_preference': fp_db,
        'class': class_name,
    })

    safe_name = ''.join(c for c in name if c.isalnum() or c in (' ', '-', '_')).rstrip().replace(' ', '_')
    filename = f'qr_codes_jpeg/{safe_name}_{usn}.jpg'

    # Generate QR image
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(qr_data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color='black', back_color='white')
    qr_img.save(filename)

    # Insert into DB
    cursor.execute('''INSERT INTO users (name, email, usn, class_name, food_preference, token, qr_code_path, is_scanned, created_at)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                   (name, email, usn, class_name, fp_db, token, filename, 0, created_at))
    conn.commit()
    added.append((name, usn, email, filename))

conn.close()

print('Added:')
for a in added:
    print('  ', a)
print('\nSkipped:')
for s in skipped:
    print('  ', s)
