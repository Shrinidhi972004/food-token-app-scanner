const express = require('express');
const multer = require('multer');
const csv = require('csv-parser');
const fs = require('fs');
const path = require('path');
const QRCode = require('qrcode');
const { v4: uuidv4 } = require('uuid');
const archiver = require('archiver');
const cors = require('cors');
const Database = require('./database');

const app = express();
const PORT = process.env.PORT || 3000;

const db = new Database();

app.use(cors());
app.use(express.json());
app.use(express.static('public'));
app.use('/qr-codes', express.static('qr-codes'));

const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, 'uploads/');
    },
    filename: (req, file, cb) => {
        cb(null, `${Date.now()}-${file.originalname}`);
    }
});
const upload = multer({ storage: storage });

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.get('/admin', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'admin.html'));
});

app.get('/scanner', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'scanner.html'));
});

app.post('/api/upload-csv', upload.single('csvFile'), async (req, res) => {
    try {
        if (!req.file) {
            return res.status(400).json({ error: 'No file uploaded' });
        }

        const results = [];
        const filePath = req.file.path;

        // Read and parse CSV
        fs.createReadStream(filePath)
            .pipe(csv())
            .on('data', (data) => {
                // Normalize column names (remove spaces, convert to lowercase)
                const normalizedData = {};
                Object.keys(data).forEach(key => {
                    const normalizedKey = key.toLowerCase().trim().replace(/\s+/g, '_');
                    normalizedData[normalizedKey] = data[key].trim();
                });
                results.push(normalizedData);
            })
            .on('end', async () => {
                try {
                    console.log('CSV parsing completed. Processing', results.length, 'records');
                    
                    const processedUsers = [];
                    
                    for (const row of results) {
                        const name = row.name || row.full_name || row.participant_name || row.your_name || row.student_name || '';
                        const email = row.email || row.email_address || row.email_id || '';
                        const phone = row.phone || row.mobile || row.contact || row.phone_number || '';
                        const foodPref = (row.food_preference || row.food_choice || row.preference || row.veg_non_veg || '').toLowerCase();
                        
                        let food_preference = '';
                        if (foodPref.includes('veg') && !foodPref.includes('non')) {
                            food_preference = 'veg';
                        } else if (foodPref.includes('non') || foodPref.includes('nonveg')) {
                            food_preference = 'non-veg';
                        } else {
                            food_preference = 'veg';
                        }

                        if (name) {
                            const token = uuidv4();
                            const userData = {
                                name,
                                email,
                                phone,
                                food_preference,
                                token,
                                qr_code_path: `qr-codes/${token}.png`
                            };

                            const userId = await db.addUser(userData);
                            processedUsers.push({ ...userData, id: userId });
                        }
                    }

                    fs.unlinkSync(filePath);

                    res.json({
                        message: 'CSV processed successfully',
                        count: processedUsers.length,
                        users: processedUsers
                    });

                } catch (error) {
                    console.error('Error processing CSV:', error);
                    res.status(500).json({ error: 'Error processing CSV data' });
                }
            });

    } catch (error) {
        console.error('Error uploading file:', error);
        res.status(500).json({ error: 'Error uploading file' });
    }
});

app.post('/api/generate-qr-codes', async (req, res) => {
    try {
        const users = await db.getAllUsers();
        const qrCodeDir = path.join(__dirname, 'qr-codes');
        
        if (!fs.existsSync(qrCodeDir)) {
            fs.mkdirSync(qrCodeDir, { recursive: true });
        }

        const generatedCodes = [];

        for (const user of users) {
            if (!user.is_scanned) {
                const qrData = {
                    token: user.token,
                    name: user.name,
                    type: 'food-token'
                };

                const qrCodePath = path.join(qrCodeDir, `${user.token}.png`);
                
                await QRCode.toFile(qrCodePath, JSON.stringify(qrData), {
                    color: {
                        dark: '#000000',
                        light: '#FFFFFF'
                    },
                    width: 300
                });

                generatedCodes.push({
                    name: user.name,
                    token: user.token,
                    food_preference: user.food_preference,
                    qr_path: `qr-codes/${user.token}.png`
                });
            }
        }

        res.json({
            message: 'QR codes generated successfully',
            count: generatedCodes.length,
            codes: generatedCodes
        });

    } catch (error) {
        console.error('Error generating QR codes:', error);
        res.status(500).json({ error: 'Error generating QR codes' });
    }
});

app.get('/api/download-qr-codes', (req, res) => {
    const qrCodeDir = path.join(__dirname, 'qr-codes');
    const archive = archiver('zip', { zlib: { level: 9 } });

    res.attachment('qr-codes.zip');
    archive.pipe(res);

    archive.directory(qrCodeDir, false);
    archive.finalize();
});

app.post('/api/scan', async (req, res) => {
    try {
        const { qrData } = req.body;
        
        if (!qrData) {
            return res.status(400).json({ error: 'No QR data provided' });
        }

        let user = null;
        let isUSNEntry = false;

        // First, try to parse as JSON (QR code format)
        try {
            const tokenData = JSON.parse(qrData);
            user = await db.getUserByToken(tokenData.token);
        } catch (e) {
            // If JSON parsing fails, check if it's a USN or direct token
            const cleanInput = qrData.trim().toUpperCase();
            
            // Check if it looks like a USN (contains letters and numbers, typical USN pattern)
            if (/^[A-Z0-9]{6,15}$/.test(cleanInput)) {
                // Try USN lookup first
                user = await db.getUserByUSN(cleanInput);
                isUSNEntry = true;
                
                // If USN not found, try as direct token
                if (!user) {
                    user = await db.getUserByToken(qrData.trim());
                    isUSNEntry = false;
                }
            } else {
                // Try as direct token
                user = await db.getUserByToken(qrData.trim());
            }
        }
        
        if (!user) {
            const errorMsg = isUSNEntry ? 'USN not found in database' : 'Invalid token';
            return res.status(404).json({ error: errorMsg });
        }

        if (user.is_scanned) {
            return res.status(409).json({ 
                error: 'Token already used',
                scanned_at: user.scanned_at,
                user: {
                    name: user.name,
                    food_preference: user.food_preference,
                    usn: user.usn,
                    class_name: user.class_name
                }
            });
        }

        await db.markAsScanned(user.token);
        await db.addScanHistory(user.id, req.ip);

        res.json({
            success: true,
            message: isUSNEntry ? 'USN validated successfully' : 'Token scanned successfully',
            user: {
                name: user.name,
                food_preference: user.food_preference,
                email: user.email,
                phone: user.phone,
                usn: user.usn,
                class_name: user.class_name,
                scanned_at: new Date().toISOString()
            }
        });

    } catch (error) {
        console.error('Error scanning token:', error);
        res.status(500).json({ error: 'Error processing scan' });
    }
});

app.get('/api/users', async (req, res) => {
    try {
        const users = await db.getAllUsers();
        res.json(users);
    } catch (error) {
        console.error('Error fetching users:', error);
        res.status(500).json({ error: 'Error fetching users' });
    }
});

app.get('/api/stats', async (req, res) => {
    try {
        const stats = await db.getScanStats();
        res.json(stats);
    } catch (error) {
        console.error('Error fetching stats:', error);
        res.status(500).json({ error: 'Error fetching statistics' });
    }
});

app.delete('/api/clear-data', async (req, res) => {
    try {
        await db.clearAllData();
        
        const qrCodeDir = path.join(__dirname, 'qr-codes');
        if (fs.existsSync(qrCodeDir)) {
            const files = fs.readdirSync(qrCodeDir);
            for (const file of files) {
                fs.unlinkSync(path.join(qrCodeDir, file));
            }
        }

        res.json({ message: 'All data cleared successfully' });
    } catch (error) {
        console.error('Error clearing data:', error);
        res.status(500).json({ error: 'Error clearing data' });
    }
});

app.listen(PORT, () => {
    console.log(`Food Token Scanner Server running on port ${PORT}`);
    console.log(`Admin Dashboard: http://localhost:${PORT}/admin`);
    console.log(`Scanner Interface: http://localhost:${PORT}/scanner`);
});

process.on('SIGINT', () => {
    console.log('Shutting down server...');
    db.close();
    process.exit(0);
});
