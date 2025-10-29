#!/usr/bin/env python3
import os
import sqlite3
import json
from collections import defaultdict

def cleanup_duplicates():
    print("🧹 Cleaning up duplicate QR codes and database entries...")
    
    # 1. Clean up QR code files (keep only newer ones)
    qr_dir = 'qr_codes_jpeg'
    if os.path.exists(qr_dir):
        files = os.listdir(qr_dir)
        jpg_files = [f for f in files if f.endswith('.jpg')]
        
        # Group files by name pattern (without the unique token part)
        file_groups = defaultdict(list)
        for filename in jpg_files:
            # Extract name pattern (everything before the last underscore and token)
            parts = filename.split('_')
            if len(parts) >= 3:
                # Take all parts except the last one (which is the token)
                base_name = '_'.join(parts[:-1])
                file_groups[base_name].append(filename)
        
        duplicates_removed = 0
        for base_name, files_list in file_groups.items():
            if len(files_list) > 1:
                # Sort by modification time, keep the newest
                files_with_time = [(f, os.path.getmtime(os.path.join(qr_dir, f))) for f in files_list]
                files_with_time.sort(key=lambda x: x[1], reverse=True)
                
                # Remove older files
                for filename, _ in files_with_time[1:]:
                    file_path = os.path.join(qr_dir, filename)
                    os.remove(file_path)
                    duplicates_removed += 1
                    print(f"  🗑️ Removed duplicate: {filename}")
        
        print(f"✅ Removed {duplicates_removed} duplicate QR code files")
    
    # 2. Clean up database duplicates
    db_path = 'database/food_tokens.db'
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Find duplicates by name and email
        cursor.execute('''
            SELECT name, email, MIN(id) as keep_id, COUNT(*) as count
            FROM users 
            GROUP BY name, email 
            HAVING count > 1
        ''')
        
        duplicates = cursor.fetchall()
        total_removed = 0
        
        for name, email, keep_id, count in duplicates:
            # Delete all entries except the one with minimum ID
            cursor.execute('''
                DELETE FROM users 
                WHERE name = ? AND email = ? AND id != ?
            ''', (name, email, keep_id))
            
            removed = cursor.rowcount
            total_removed += removed
            print(f"  🗑️ Removed {removed} duplicate entries for: {name}")
        
        conn.commit()
        
        # Get final counts
        cursor.execute('SELECT COUNT(*) FROM users')
        final_count = cursor.fetchone()[0]
        
        print(f"✅ Removed {total_removed} duplicate database entries")
        print(f"📊 Final user count: {final_count}")
        
        conn.close()
    
    # 3. Update tokens_list.json
    tokens_file = os.path.join(qr_dir, 'tokens_list.json')
    if os.path.exists(tokens_file):
        with open(tokens_file, 'r') as f:
            tokens_data = json.load(f)
        
        # Remove duplicates based on name and email
        seen = set()
        unique_tokens = []
        
        for token_info in tokens_data:
            key = (token_info['name'], token_info['email'])
            if key not in seen:
                seen.add(key)
                unique_tokens.append(token_info)
        
        # Save cleaned tokens list
        with open(tokens_file, 'w') as f:
            json.dump(unique_tokens, f, indent=2)
        
        removed_tokens = len(tokens_data) - len(unique_tokens)
        print(f"✅ Cleaned tokens_list.json: removed {removed_tokens} duplicate entries")
    
    print(f"\n🎉 Cleanup completed!")
    print(f"   - Unique QR codes ready for distribution")
    print(f"   - Database cleaned of duplicates")
    print(f"   - Each student now has exactly one QR code")

if __name__ == "__main__":
    cleanup_duplicates()
