#!/usr/bin/env python3
"""
Complete Docker Automation Script
Handles: CSV cleaning, QR generation, email sending - all in one go
"""
import os
import sys
import subprocess
import time
from datetime import datetime

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    print(f"Command: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed!")
        print(f"Error: {e.stderr}")
        return False

def check_file_exists(filepath, description):
    """Check if required file exists"""
    if os.path.exists(filepath):
        print(f"✅ {description} found: {filepath}")
        return True
    else:
        print(f"❌ {description} not found: {filepath}")
        return False

def main():
    print("🚀 COMPLETE DOCKER AUTOMATION")
    print("=" * 50)
    print("This script will handle everything:")
    print("1. CSV cleaning and duplicate removal")
    print("2. QR code generation")
    print("3. Email configuration testing")
    print("4. Mass email distribution")
    print()
    
    # Check prerequisites
    print("📋 Checking prerequisites...")
    
    # Check if we have CSV data
    has_original_csv = check_file_exists("food_pref.csv", "Original CSV file")
    has_cleaned_csv = check_file_exists("food_pref_cleaned.csv", "Cleaned CSV file")
    
    if not has_original_csv and not has_cleaned_csv:
        print("❌ No CSV data found! Please upload food_pref.csv first.")
        return
    
    # Check environment configuration
    if not check_file_exists(".env", "Environment configuration"):
        print("❌ Please create .env file with email credentials first.")
        return
    
    print("\n🎯 Starting complete automation process...")
    
    # Step 1: Clean CSV (if original exists and cleaned doesn't)
    if has_original_csv and not has_cleaned_csv:
        if not run_command("python3 clean_csv.py", "CSV cleaning and duplicate removal"):
            print("❌ CSV cleaning failed. Cannot continue.")
            return
    else:
        print("✅ Using existing cleaned CSV file")
    
    # Step 2: Generate QR codes and populate database
    if not run_command("python3 generate_qr_with_db.py", "QR code generation and database setup"):
        print("❌ QR code generation failed. Cannot continue.")
        return
    
    # Step 3: Test email configuration
    print("\n📧 Testing email configuration...")
    email_test = input("Do you want to send a test email first? (y/n): ").strip().lower()
    
    if email_test == 'y':
        if not run_command("python3 test_shrinidhi_email.py", "Email configuration testing"):
            print("⚠️ Email test failed. Check your .env configuration.")
            continue_anyway = input("Continue with mass email anyway? (y/n): ").strip().lower()
            if continue_anyway != 'y':
                print("❌ Stopping due to email test failure.")
                return
    
    # Step 4: Mass email distribution
    print("\n📮 Ready for mass email distribution...")
    
    # Show summary
    try:
        result = subprocess.run("python3 -c \"import sqlite3; conn = sqlite3.connect('database/food_tokens.db'); cursor = conn.cursor(); cursor.execute('SELECT COUNT(*) FROM users'); count = cursor.fetchone()[0]; conn.close(); print(f'Total students: {count}')\"", 
                              shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"📊 {result.stdout.strip()}")
    except:
        print("📊 Student count check failed")
    
    # Final confirmation
    send_emails = input("\n🚨 Send emails to ALL students? (type 'YES' to confirm): ").strip()
    
    if send_emails == 'YES':
        if not run_command("python3 deploy_email_distribution.py", "Mass email distribution"):
            print("❌ Email distribution failed.")
            return
    else:
        print("📧 Email distribution skipped.")
        print("💡 You can run it later with: docker-compose exec food-token-scanner python3 deploy_email_distribution.py")
    
    # Final status
    print("\n🎉 AUTOMATION COMPLETED!")
    print("=" * 30)
    print("✅ CSV cleaned and duplicates removed")
    print("✅ QR codes generated")
    print("✅ Database populated")
    if send_emails == 'YES':
        print("✅ Emails sent to all students")
    print("✅ System ready for production!")
    
    print("\n🌐 Access your application:")
    print("Scanner: http://localhost:3000/scanner")
    print("Admin: http://localhost:3000/admin")
    
    print("\n🔧 Management commands:")
    print("View logs: docker-compose logs -f")
    print("Restart: docker-compose restart")
    print("Stop: docker-compose down")

if __name__ == "__main__":
    main()
