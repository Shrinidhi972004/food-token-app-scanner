#!/usr/bin/env python3
import csv
import qrcode
from PIL import Image, ImageDraw, ImageFont
import uuid
import os
import json

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

def main():
    csv_file = 'classwise_sorted_all_emails_final.csv'
    output_dir = 'qr_codes_jpeg'
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print(f"📊 Reading CSV file: {csv_file}")
    
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
    
    print(f"✅ Found {len(rows)} students")
    print(f"📁 Creating QR codes in directory: {output_dir}")
    
    tokens_data = []
    
    for i, row in enumerate(rows):
        name = row['Enter Your Name'].strip()
        email = row['Enter Your College Mail ID'].strip()
        class_name = row['Class'].strip()
        food_pref = row['What kind of food do you prefer'].strip()
        
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
        
        create_qr_with_text(json.dumps(qr_data), filename, name, food_pref, class_name)
        
        tokens_data.append({
            'name': name,
            'email': email,
            'class': class_name,
            'food_preference': food_pref,
            'token': token,
            'filename': filename
        })
        
        if (i + 1) % 50 == 0:
            print(f"⏳ Generated {i + 1}/{len(rows)} QR codes...")
    
    with open(f'{output_dir}/tokens_list.json', 'w') as f:
        json.dump(tokens_data, f, indent=2)
    
    print(f"✅ Successfully generated {len(rows)} QR codes!")
    print(f"📁 Files saved in: {output_dir}/")
    print(f"📋 Token list saved as: {output_dir}/tokens_list.json")
    
    veg_count = sum(1 for row in rows if 'veg' in row['What kind of food do you prefer'].lower() and 'non' not in row['What kind of food do you prefer'].lower())
    non_veg_count = sum(1 for row in rows if 'non' in row['What kind of food do you prefer'].lower())
    
    print(f"\n📈 SUMMARY:")
    print(f"🥗 Veg QR codes: {veg_count}")
    print(f"🍖 Non-Veg QR codes: {non_veg_count}")
    print(f"📊 Total QR codes: {len(rows)}")

if __name__ == "__main__":
    main()
