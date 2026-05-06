# 🚀 XAMPP Setup Guide for C Programming Game

## 📋 Prerequisites
- XAMPP installed on your system
- Web browser
- Text editor (optional)

## 🔧 Step-by-Step Setup

### 1. Start XAMPP Services
1. Open XAMPP Control Panel
2. Start **Apache** service
3. Start **MySQL** service
4. Ensure both services show "Running" status

### 2. Setup Database
1. Open your web browser
2. Go to `http://localhost/phpmyadmin`
3. Click "SQL" tab
4. Copy and paste the contents of `database_setup.sql`
5. Click "Go" to execute the SQL commands
6. Verify that database `c_game_db` is created with all tables

### 3. Place Project Files
1. Copy your entire project folder to `C:\xampp\htdocs\` (Windows) or `/Applications/XAMPP/htdocs/` (Mac)
2. Your project structure should look like:
   ```
   htdocs/
   └── your-project-name/
       ├── Home Page/
       ├── Login Module/
       ├── kings-and-pigs-main/
       └── other folders...
   ```

### 4. Test Database Connection
1. Open browser and go to `http://localhost/your-project-name/Login Module/admin_dashboard.php`
2. If you see the admin dashboard, the connection is working!
3. If you see errors, check the database setup and file paths

### 5. Access Your Game
- **Game Homepage**: `http://localhost/your-project-name/Home Page/arena.html`
- **Admin Dashboard**: `http://localhost/your-project-name/Login Module/admin_dashboard.php`
- **phpMyAdmin**: `http://localhost/phpmyadmin`

## 🗄️ Database Tables Created

### Core Tables:
- **users** - User accounts (username, email, password)
- **user_progress** - Game progress (levels, XP, player data)
- **player_stats** - Detailed player statistics
- **level_completions** - Level completion records
- **task_submissions** - Individual task submissions
- **code_submissions** - Code submissions with compile results
- **game_sessions** - Session tracking data

## 📊 What Data is Stored

### User Registration/Login:
- ✅ Username and email
- ✅ Encrypted passwords
- ✅ Registration and login timestamps

### Game Progress:
- ✅ Current level and unlocked levels
- ✅ Completed levels and tasks
- ✅ XP points and health status
- ✅ Player statistics and achievements

### Code Submissions:
- ✅ All code submitted by users
- ✅ Compilation results
- ✅ Execution results
- ✅ Success/failure status

### Session Tracking:
- ✅ Game session duration
- ✅ Levels played per session
- ✅ User activity patterns

## 🔍 Viewing Data in XAMPP

### Method 1: Admin Dashboard
- Go to `http://localhost/your-project-name/Login Module/admin_dashboard.php`
- View user statistics, progress, and leaderboards
- Real-time data with refresh functionality

### Method 2: phpMyAdmin
- Go to `http://localhost/phpmyadmin`
- Select `c_game_db` database
- Browse individual tables to see raw data
- Run custom SQL queries

### Method 3: Direct Database Queries
Example queries you can run in phpMyAdmin:

```sql
-- View all users with their progress
SELECT u.username, u.email, u.created_at, ps.xp, ps.current_level
FROM users u
LEFT JOIN player_stats ps ON u.id = ps.user_id;

-- View level completion statistics
SELECT level, COUNT(*) as completions
FROM level_completions
GROUP BY level
ORDER BY level;

-- View recent code submissions
SELECT u.username, cs.level, cs.task_number, cs.submitted_at
FROM code_submissions cs
JOIN users u ON cs.user_id = u.id
ORDER BY cs.submitted_at DESC
LIMIT 10;
```

## 🛠️ Troubleshooting

### Common Issues:

1. **"Connection failed" error**
   - Check if MySQL service is running in XAMPP
   - Verify database credentials in `config.php`

2. **"Access denied" error**
   - Ensure Apache service is running
   - Check file permissions

3. **"Database not found" error**
   - Run the `database_setup.sql` script in phpMyAdmin
   - Verify database name matches `config.php`

4. **CORS errors in browser console**
   - Files are already configured for local development
   - Ensure you're accessing via `http://localhost/`

### File Permissions:
- Ensure all PHP files have read permissions
- Database files should be writable by MySQL service

## 🔐 Security Notes

### For Development:
- Default MySQL user is `root` with no password
- This is fine for local development only

### For Production:
- Change database credentials in `config.php`
- Use strong passwords
- Enable SSL/HTTPS
- Implement proper user authentication

## 📈 Monitoring Your Game

### Real-time Statistics:
- Total registered users
- Active players
- Level completion rates
- Average session duration
- Most popular levels

### User Analytics:
- Registration trends
- Player progression patterns
- Code submission frequency
- Error patterns in submissions

## 🎯 Next Steps

1. **Test the complete flow**:
   - Register a new user
   - Play through levels
   - Check data appears in admin dashboard

2. **Customize as needed**:
   - Modify database schema if required
   - Add new tracking features
   - Enhance admin dashboard

3. **Monitor performance**:
   - Check database size growth
   - Monitor query performance
   - Optimize as needed

## 📞 Support

If you encounter issues:
1. Check XAMPP error logs
2. Verify all services are running
3. Test database connection separately
4. Check browser console for JavaScript errors

Your C Programming Game is now fully integrated with XAMPP and ready to store all user data! 🎉