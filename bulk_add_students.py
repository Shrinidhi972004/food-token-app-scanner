import qrcode
import os

# Folder to save all QR codes
output_folder = "qr_codes_jpeg"
os.makedirs(output_folder, exist_ok=True)

# Student details list
students = [
    {
        "name": "Akshay Ks",
        "usn": "4SF24IS008",
        "email": "akshay.ks.is24@sahyadri.edu.in",
        "section": "ISE 3A",
        "food": "Non-Veg"
    },
    {
        "name": "Madeeha Zahoor",
        "usn": "4SF23IS055",
        "email": "madeeha.is23@sahyadri.edu.in",
        "section": "ISE 5B",
        "food": "Non-Veg"
    },
    {
        "name": "Shivaraj Sadashiv Chigare",
        "usn": "4SF23CD404",
        "email": "shivaraj.ds22@sahyadri.edu.in",
        "section": "7DS",
        "food": "Veg"
    },
    {
        "name": "SINCHANA S NAIK",
        "usn": "4SF22CD044",
        "email": "sinchanas.ds22@sahaydri.edu.in",
        "section": "7DS",
        "food": "Non-Veg"
    },
    {
        "name": "Rm Raja Subramanian",
        "usn": "4SF24IS081",
        "email": "raja.rm.ise@sahyadri.edu.in",
        "section": "ISE 3A",
        "food": "Non-Veg"
    },
    {
        "name": "Shifa Kouser",
        "usn": "4SF22CD041",
        "email": "shifakouser8618@gmail.com",
        "section": "7DS",
        "food": "Veg"
    },
    {
        "name": "Abdul Shaz",
        "usn": "4SF23IS002",
        "email": "abdulshaz.is23@sahyadri.edu.in",
        "section": "ISE 5A",
        "food": "Non-Veg"
    },
    {
        "name": "Tarun G",
        "usn": "4SF22CD053",
        "email": "tarun.ds22@sahyadri.edu.in",
        "section": "7DS",
        "food": "Non-Veg"
    },
    {
        "name": "Rushil",
        "usn": "4SF23IS014",
        "email": "amin.is23@sahyadri.edu.in",
        "section": "ISE 5B",
        "food": "Veg"
    },
    {
        "name": "Winston Felix Fernandes",
        "usn": "4SF22CD059",
        "email": "Winstonfelixfernandes@gmail.com",
        "section": "7DS",
        "food": "Non-Veg"
    }
]

# Generate QR for each student
for student in students:
    data = (
        f"Name: {student['name']}\n"
        f"USN: {student['usn']}\n"
        f"Email: {student['email']}\n"
        f"Section: {student['section']}\n"
        f"Food Preference: {student['food']}"
    )
    img = qrcode.make(data)
    filename = f"{student['name'].replace(' ', '_')}.png"
    filepath = os.path.join(output_folder, filename)
    img.save(filepath)
    print(f"✅ QR code saved: {filepath}")

print("\nAll QR codes generated successfully in the 'qrcodes' folder.")

