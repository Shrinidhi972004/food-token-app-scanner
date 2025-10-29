#!/usr/bin/env python3
import pandas as pd

def clean_csv():
    # Read the CSV file
    df = pd.read_csv('food_pref.csv')
    
    print(f"📊 Original CSV: {len(df)} rows")
    print(f"📋 Columns: {list(df.columns)}")
    
    # Remove the timestamp column
    if 'Timestamp' in df.columns:
        df = df.drop('Timestamp', axis=1)
        print("🗑️ Removed Timestamp column")
    
    # Clean up whitespace in all string columns
    string_columns = ['Enter Your Name', 'Enter Your College Mail ID', 'Enter Your USN', 'Class', 'What kind of food do you prefer']
    for col in string_columns:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
    
    # Remove duplicates based on email and USN (students should have unique email and USN)
    initial_count = len(df)
    df = df.drop_duplicates(subset=['Enter Your College Mail ID', 'Enter Your USN'], keep='first')
    removed_duplicates = initial_count - len(df)
    
    if removed_duplicates > 0:
        print(f"🗑️ Removed {removed_duplicates} duplicate entries")
    
    # Sort by class and then by name
    df = df.sort_values(['Class', 'Enter Your Name'])
    
    # Save cleaned CSV (remove any existing file/directory first)
    cleaned_filename = 'food_pref_cleaned.csv'
    import os
    import shutil
    
    # Remove existing file or directory if it exists
    if os.path.exists(cleaned_filename):
        if os.path.isfile(cleaned_filename):
            os.remove(cleaned_filename)
        elif os.path.isdir(cleaned_filename):
            shutil.rmtree(cleaned_filename)
            
    df.to_csv(cleaned_filename, index=False)
    
    print(f"✅ Cleaned CSV saved as: {cleaned_filename}")
    print(f"📊 Final count: {len(df)} students")
    
    # Show sample of cleaned data
    print(f"\n📋 Sample of cleaned data:")
    print(df.head().to_string(index=False))
    
    # Show statistics
    veg_count = len(df[df['What kind of food do you prefer'].str.contains('Veg', case=False, na=False) & 
                     ~df['What kind of food do you prefer'].str.contains('Non', case=False, na=False)])
    non_veg_count = len(df[df['What kind of food do you prefer'].str.contains('Non', case=False, na=False)])
    
    print(f"\n📈 Food preferences:")
    print(f"🥗 Vegetarian: {veg_count}")
    print(f"🍖 Non-Vegetarian: {non_veg_count}")
    print(f"📊 Total: {len(df)}")

if __name__ == "__main__":
    clean_csv()
