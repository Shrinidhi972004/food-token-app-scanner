#!/usr/bin/env python3
"""
Production Email Distribution Script
Send QR codes to all students in the database when ready for deployment
"""
import os
import time
from datetime import datetime
from dotenv import load_dotenv
from send_qr_emails import EmailSender
import sqlite3
import glob

def get_all_students():
    """Get all students from the database"""
    try:
        conn = sqlite3.connect('database/food_tokens.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, name, email, usn, class_name, food_preference, qr_code_path 
            FROM users 
            ORDER BY class_name, name
        ''')
        students = cursor.fetchall()
        conn.close()
        return students
    except Exception as e:
        print(f"❌ Error accessing database: {e}")
        return []

def validate_qr_files(students):
    """Check which QR code files exist and find alternatives for missing ones"""
    valid_students = []
    missing_files = []
    
    for student in students:
        student_id, name, email, usn, class_name, food_preference, qr_code_path = student
        
        if os.path.exists(qr_code_path):
            valid_students.append(student)
        else:
            # Try to find alternative QR code files for this student
            safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).strip()
            
            # Try different patterns
            patterns = [
                f"qr_codes_jpeg/{safe_name}_*.jpg",
                f"qr_codes_jpeg/*{name}*.jpg",
                f"qr_codes_jpeg/{name.replace(' ', '_')}_*.jpg"
            ]
            
            found_file = None
            for pattern in patterns:
                matches = glob.glob(pattern)
                if matches:
                    found_file = matches[0]
                    break
            
            if found_file:
                # Update the student record with the found file
                updated_student = (student_id, name, email, usn, class_name, food_preference, found_file)
                valid_students.append(updated_student)
                print(f"📁 Found alternative QR for {name}: {found_file}")
            else:
                missing_files.append((name, email, qr_code_path))
    
    return valid_students, missing_files

def send_emails_by_batch(email_sender, students, batch_size=50):
    """Send emails in batches with progress tracking"""
    total_students = len(students)
    sent_count = 0
    failed_count = 0
    failed_students = []
    
    print(f"📧 Starting email distribution to {total_students} students...")
    print(f"📦 Processing in batches of {batch_size} students")
    print("=" * 60)
    
    start_time = datetime.now()
    
    for i in range(0, total_students, batch_size):
        batch = students[i:i + batch_size]
        batch_num = (i // batch_size) + 1
        total_batches = (total_students + batch_size - 1) // batch_size
        
        print(f"\n📦 BATCH {batch_num}/{total_batches} ({len(batch)} students)")
        print(f"⏰ Batch started: {datetime.now().strftime('%H:%M:%S')}")
        
        batch_sent = 0
        batch_failed = 0
        
        for j, student in enumerate(batch, 1):
            student_id, name, email, usn, class_name, food_preference, qr_code_path = student
            
            print(f"  📧 [{i+j:3d}/{total_students}] {name} ({class_name}) -> {email}")
            
            try:
                success = email_sender.send_email_with_qr(
                    email, name, class_name, usn, food_preference, qr_code_path
                )
                
                if success:
                    sent_count += 1
                    batch_sent += 1
                    print(f"     ✅ Sent successfully")
                else:
                    failed_count += 1
                    batch_failed += 1
                    failed_students.append((name, email, "Email sending failed"))
                    print(f"     ❌ Failed to send")
                
                # Delay between emails to avoid overwhelming the server
                time.sleep(2)
                
            except Exception as e:
                failed_count += 1
                batch_failed += 1
                failed_students.append((name, email, str(e)))
                print(f"     ❌ Error: {str(e)}")
        
        # Batch summary
        print(f"  📊 Batch {batch_num} complete: {batch_sent} sent, {batch_failed} failed")
        print(f"  ⏰ Batch duration: {(datetime.now() - start_time).seconds // 60} minutes")
        
        # Longer delay between batches
        if i + batch_size < total_students:
            print(f"  ⏸️  Waiting 30 seconds before next batch...")
            time.sleep(30)
    
    end_time = datetime.now()
    duration = end_time - start_time
    
    return sent_count, failed_count, failed_students, duration

def generate_report(sent_count, failed_count, failed_students, missing_files, duration, total_students):
    """Generate a detailed email distribution report"""
    report_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    report_file = f"email_distribution_report_{report_time}.txt"
    
    success_rate = (sent_count / total_students * 100) if total_students > 0 else 0
    
    report_content = f"""
📧 EMAIL DISTRIBUTION REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
==========================================

📊 SUMMARY STATISTICS:
- Total Students: {total_students}
- Emails Sent Successfully: {sent_count}
- Emails Failed: {failed_count}
- Missing QR Files: {len(missing_files)}
- Success Rate: {success_rate:.1f}%
- Total Duration: {duration.seconds // 3600}h {(duration.seconds % 3600) // 60}m {duration.seconds % 60}s

🎯 PERFORMANCE METRICS:
- Average per Email: {duration.total_seconds() / total_students:.1f} seconds
- Emails per Minute: {sent_count / (duration.total_seconds() / 60):.1f}

"""

    if failed_students:
        report_content += f"""
❌ FAILED EMAIL DELIVERIES ({len(failed_students)}):
{'='*50}
"""
        for name, email, error in failed_students:
            report_content += f"- {name} ({email}): {error}\n"

    if missing_files:
        report_content += f"""
📁 MISSING QR CODE FILES ({len(missing_files)}):
{'='*50}
"""
        for name, email, file_path in missing_files:
            report_content += f"- {name} ({email}): {file_path}\n"

    report_content += f"""
✅ SUCCESSFUL DELIVERIES ({sent_count}):
{'='*50}
All successfully sent emails are logged above in the console output.

📋 NEXT STEPS:
1. Review failed deliveries and retry if needed
2. Generate missing QR codes if any
3. Monitor student feedback and email bounces
4. Set up the scanning system at food counter
5. Test the QR scanner with received QR codes

🚀 SYSTEM READY FOR DEPLOYMENT!
"""

    # Save report to file
    with open(report_file, 'w') as f:
        f.write(report_content)
    
    return report_file, report_content

def main():
    print("🚀 PRODUCTION EMAIL DISTRIBUTION SYSTEM")
    print("=" * 60)
    print("This script will send QR codes to ALL students in the database.")
    print("Make sure you're ready for full deployment before proceeding!")
    print()
    
    # Load configuration
    load_dotenv()
    
    # Display configuration
    print(f"📧 Email Configuration:")
    print(f"   From: {os.getenv('EMAIL_USER')}")
    print(f"   SMTP: {os.getenv('EMAIL_HOST')}:{os.getenv('EMAIL_PORT')}")
    print(f"   Subject: {os.getenv('EMAIL_SUBJECT')}")
    print()
    
    # Get all students
    print("📋 Loading student data from database...")
    students = get_all_students()
    
    if not students:
        print("❌ No students found in database!")
        print("💡 Run 'python generate_qr_with_db.py' first to populate database")
        return
    
    print(f"✅ Found {len(students)} students in database")
    
    # Validate QR code files
    print("🔍 Validating QR code files...")
    valid_students, missing_files = validate_qr_files(students)
    
    print(f"✅ Valid students with QR codes: {len(valid_students)}")
    if missing_files:
        print(f"⚠️  Students with missing QR files: {len(missing_files)}")
        for name, email, file_path in missing_files:
            print(f"   - {name} ({email})")
    
    if not valid_students:
        print("❌ No valid students with QR codes found!")
        return
    
    # Initialize email sender
    print("\n📧 Initializing email system...")
    try:
        email_sender = EmailSender()
        print("✅ Email system ready")
    except Exception as e:
        print(f"❌ Email system initialization failed: {e}")
        return
    
    # Show breakdown by class
    class_counts = {}
    food_counts = {'Veg': 0, 'Non Veg': 0}
    
    for student in valid_students:
        _, name, email, usn, class_name, food_preference, qr_code_path = student
        class_counts[class_name] = class_counts.get(class_name, 0) + 1
        if 'veg' in food_preference.lower() and 'non' not in food_preference.lower():
            food_counts['Veg'] += 1
        else:
            food_counts['Non Veg'] += 1
    
    print(f"\n📊 Student Distribution:")
    for class_name, count in sorted(class_counts.items()):
        print(f"   {class_name}: {count} students")
    
    print(f"\n🍽️ Food Preferences:")
    for pref, count in food_counts.items():
        print(f"   {pref}: {count} students")
    
    # Final confirmation
    print(f"\n⚠️  FINAL CONFIRMATION:")
    print(f"   📧 Ready to send emails to {len(valid_students)} students")
    print(f"   ⏱️  Estimated time: {len(valid_students) * 2 // 60} minutes")
    print(f"   📨 From: {os.getenv('EMAIL_USER')}")
    
    confirm = input(f"\n🚨 PROCEED WITH SENDING EMAILS TO ALL STUDENTS? (type 'YES' to confirm): ").strip()
    
    if confirm != 'YES':
        print("❌ Email distribution cancelled")
        print("💡 Run this script again when ready for deployment")
        return
    
    # Send emails
    print(f"\n🚀 STARTING EMAIL DISTRIBUTION...")
    print(f"📅 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    sent_count, failed_count, failed_students, duration = send_emails_by_batch(
        email_sender, valid_students, batch_size=25
    )
    
    # Generate report
    print(f"\n📊 GENERATING DISTRIBUTION REPORT...")
    report_file, report_content = generate_report(
        sent_count, failed_count, failed_students, missing_files, duration, len(valid_students)
    )
    
    # Display final summary
    print(f"\n🎉 EMAIL DISTRIBUTION COMPLETED!")
    print("=" * 50)
    print(report_content)
    print(f"📄 Detailed report saved to: {report_file}")
    
    if sent_count == len(valid_students):
        print(f"\n🎊 PERFECT SUCCESS! All {sent_count} emails sent successfully!")
        print("🚀 Your food token system is now fully deployed!")
    else:
        print(f"\n⚠️  Partial success: {sent_count}/{len(valid_students)} emails sent")
        print("💡 Check the report for failed deliveries and retry if needed")
    
    print(f"\n📱 Next steps:")
    print(f"   1. Start the scanner server: npm start")
    print(f"   2. Open scanner interface: http://localhost:3000/scanner")
    print(f"   3. Test with received QR codes")
    print(f"   4. Monitor admin dashboard: http://localhost:3000/admin")

if __name__ == "__main__":
    main()
