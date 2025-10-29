const sqlite3 = require('sqlite3').verbose();
const path = require('path');

class Database {
    constructor() {
        this.dbPath = path.join(__dirname, 'database', 'food_tokens.db');
        this.db = new sqlite3.Database(this.dbPath);
        this.init();
    }

    init() {
        this.db.run(`
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
                class_name TEXT
            )
        `);
        
        this.db.run(`
            ALTER TABLE users ADD COLUMN class_name TEXT
        `, (err) => {
            if (err && !err.message.includes('duplicate column name')) {
                console.error('Error adding class_name column:', err);
            }
        });

        this.db.run(`
            ALTER TABLE users ADD COLUMN usn TEXT
        `, (err) => {
            if (err && !err.message.includes('duplicate column name')) {
                console.error('Error adding usn column:', err);
            }
        });

        this.db.run(`
            CREATE TABLE IF NOT EXISTS scan_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                scanned_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                scanner_info TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        `);

        console.log('Database initialized successfully');
    }

    addUser(userData) {
        return new Promise((resolve, reject) => {
            const { name, email, phone, food_preference, token, qr_code_path, class_name, usn } = userData;
            const stmt = this.db.prepare(`
                INSERT INTO users (name, email, phone, food_preference, token, qr_code_path, class_name, usn)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            `);
            
            stmt.run([name, email, phone, food_preference, token, qr_code_path, class_name, usn], function(err) {
                if (err) {
                    reject(err);
                } else {
                    resolve(this.lastID);
                }
            });
            stmt.finalize();
        });
    }

    getUserByToken(token) {
        return new Promise((resolve, reject) => {
            this.db.get(
                'SELECT * FROM users WHERE token = ?',
                [token],
                (err, row) => {
                    if (err) {
                        reject(err);
                    } else {
                        resolve(row);
                    }
                }
            );
        });
    }

    getUserByUSN(usn) {
        return new Promise((resolve, reject) => {
            this.db.get(
                'SELECT * FROM users WHERE usn = ? COLLATE NOCASE',
                [usn],
                (err, row) => {
                    if (err) {
                        reject(err);
                    } else {
                        resolve(row);
                    }
                }
            );
        });
    }

    markAsScanned(token) {
        return new Promise((resolve, reject) => {
            this.db.run(
                'UPDATE users SET is_scanned = 1, scanned_at = CURRENT_TIMESTAMP WHERE token = ?',
                [token],
                function(err) {
                    if (err) {
                        reject(err);
                    } else {
                        resolve(this.changes);
                    }
                }
            );
        });
    }

    addScanHistory(userId, scannerInfo = '') {
        return new Promise((resolve, reject) => {
            this.db.run(
                'INSERT INTO scan_history (user_id, scanner_info) VALUES (?, ?)',
                [userId, scannerInfo],
                function(err) {
                    if (err) {
                        reject(err);
                    } else {
                        resolve(this.lastID);
                    }
                }
            );
        });
    }

    getAllUsers() {
        return new Promise((resolve, reject) => {
            this.db.all('SELECT * FROM users ORDER BY created_at DESC', (err, rows) => {
                if (err) {
                    reject(err);
                } else {
                    resolve(rows);
                }
            });
        });
    }

    getScanStats() {
        return new Promise((resolve, reject) => {
            this.db.get(`
                SELECT 
                    COUNT(*) as total_users,
                    SUM(CASE WHEN is_scanned = 1 THEN 1 ELSE 0 END) as scanned_count,
                    SUM(CASE WHEN food_preference = 'veg' THEN 1 ELSE 0 END) as veg_count,
                    SUM(CASE WHEN food_preference = 'non-veg' THEN 1 ELSE 0 END) as nonveg_count,
                    SUM(CASE WHEN food_preference = 'veg' AND is_scanned = 1 THEN 1 ELSE 0 END) as veg_scanned,
                    SUM(CASE WHEN food_preference = 'non-veg' AND is_scanned = 1 THEN 1 ELSE 0 END) as nonveg_scanned
                FROM users
            `, (err, row) => {
                if (err) {
                    reject(err);
                } else {
                    resolve(row);
                }
            });
        });
    }

    clearAllData() {
        return new Promise((resolve, reject) => {
            this.db.serialize(() => {
                this.db.run('DELETE FROM scan_history');
                this.db.run('DELETE FROM users', (err) => {
                    if (err) {
                        reject(err);
                    } else {
                        resolve('All data cleared');
                    }
                });
            });
        });
    }

    close() {
        this.db.close();
    }
}

module.exports = Database;
