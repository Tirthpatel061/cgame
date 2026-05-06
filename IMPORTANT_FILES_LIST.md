# Important Files for Running start_all_servers.py

This document lists ALL important files needed to run the complete game system.

## Core Server Files

### 1. Main Launcher
- `start_all_servers.py` - Main file that starts all servers
- `START_SERVERS.bat` - Windows batch file to easily start servers

---

## LOGIN MODULE (Authentication System - Port 5002)

### Server Files
- `Login Module/auth_server.py` - Authentication backend server
- `Login Module/.env` - Environment configuration (MySQL, SMTP, ports)

### Frontend Files
- `Login Module/login.html` - Login/Signup page
- `Login Module/login.css` - Styling for login page
- `Login Module/login.js` - Login/Signup logic and validation

### Database Files
- `Login Module/database_setup.sql` - Database schema
- `Login Module/user_store.json` - JSON backup of users (auto-created)

### Documentation
- `Login Module/PASSWORD_VALIDATION_INFO.md` - Password requirements info

---

## ITM FOLDER (Arena/Game Backend - Port 5000)

### Server Files
- `ITM/backend3ds.py` - Main game backend server (code compilation, battles)
- `ITM/app.py` - Alternative backend (if used)
- `ITM/run_arena.py` - Arena runner script

### Executable Files (C++ Compilation)
- `ITM/battle_program.exe` - Compiled battle program
- `ITM/test_battle.exe` - Test battle executable
- `ITM/test_compile.exe` - Test compilation executable
- `ITM/test_output.exe` - Test output executable

### C++ Source Files
- `ITM/battle_code.cpp` - Battle code template
- `ITM/temp_code.cpp` - Temporary code file (auto-generated)

### Configuration Files
- `ITM/expected_output.txt` - Expected output for tests
- `ITM/README_ARENA_SERVER.md` - Arena server documentation
- `ITM/start_server.bat` - Batch file to start arena server

---

## MENTORR FOLDER (AI Mentor - Optional)

### Server Files
- `Mentorr/mentor.py` - AI mentor application (requires OpenAI API)

### Data Files
- `mentor_memory.json` - Mentor conversation history (auto-created)

---

## HOME PAGE (Arena Frontend)

### Main Files
- `Home Page/arena.html` - Arena game interface
- `Home Page/arena-styles.css` - Arena styling
- `Home Page/arena-script.js` - Arena game logic

---

## KINGS-AND-PIGS-MAIN (Game Levels)

### HTML Game Files
- `kings-and-pigs-main/index.html` - Main game page
- `kings-and-pigs-main/index - Copy.html` - Backup game page
- `kings-and-pigs-main/index3.html` to `index8.html` - Different game levels
- `kings-and-pigs-main/indexgame1.html` to `indexgame8.html` - Game variations
- `kings-and-pigs-main/indexshoot.html` - Shooting game variant

### JavaScript Files
- `kings-and-pigs-main/index.js` - Main game logic
- `kings-and-pigs-main/index2.js` to `index8.js` - Level-specific logic
- `kings-and-pigs-main/indexshoot.js` - Shooting game logic
- `kings-and-pigs-main/game.js` - Core game engine

### Authentication Pages
- `kings-and-pigs-main/login.html` - Game login page
- `kings-and-pigs-main/login.css` - Login styling
- `kings-and-pigs-main/login.js` - Login logic
- `kings-and-pigs-main/sign-up.html` - Signup page
- `kings-and-pigs-main/sign-up.css` - Signup styling

### Map & Navigation
- `kings-and-pigs-main/map.html` - Level selection map
- `kings-and-pigs-main/start.html` - Start screen

### Assets Folders (IMPORTANT!)
- `kings-and-pigs-main/img/` - Game images and sprites
- `kings-and-pigs-main/img2/` - Additional images
- `kings-and-pigs-main/js/` - JavaScript libraries
- `kings-and-pigs-main/js2/` - Additional JS files
- `kings-and-pigs-main/src/` - Source files

### Configuration Files
- `kings-and-pigs-main/package.json` - Node.js dependencies
- `kings-and-pigs-main/package-lock.json` - Dependency lock file
- `kings-and-pigs-main/vite.config.ts` - Vite configuration
- `kings-and-pigs-main/tsconfig.json` - TypeScript configuration
- `kings-and-pigs-main/tailwind.config.js` - Tailwind CSS config
- `kings-and-pigs-main/postcss.config.js` - PostCSS config
- `kings-and-pigs-main/eslint.config.js` - ESLint config

### Server Files
- `kings-and-pigs-main/serve.py` - Python server for game

---

## LOADING PAGE ANIMATION

### Files
- `Loading Page Animation/loading_page_animation.html` - Loading screen
- `Loading Page Animation/` (folder with all loading assets)

---

## ROOT LEVEL FILES

### Media
- `video.mp4` - Background video for login page

### Test Files
- `connection_test.html` - Connection testing
- `login_flow_test.html` - Login flow testing
- `test_5th_task_demo.html` - Task demo
- `test_login_scroll.html` - Login scroll test

### Documentation
- `START_ALL_SERVERS.md` - Server startup documentation

---

## DATABASE REQUIREMENTS

### MySQL Database: `c_game_db`

Required Tables:
- `users` - User accounts
- `pending_users` - Users awaiting OTP verification
- `email_otps` - OTP codes for verification
- `user_progress` - Game progress data
- `player_stats` - Player statistics
- `level_completions` - Completed levels
- `task_submissions` - Code task submissions
- `code_submissions` - Code submission history
- `code_runs` - Code execution history
- `game_sessions` - Game session tracking
- `mentor_history` - Mentor conversation history

---

## PYTHON DEPENDENCIES

Required packages (install via pip):
```
flask
flask-cors
mysql-connector-python
python-dotenv
werkzeug
openai (optional, for mentor)
```

---

## MINIMAL FILE SET FOR DEPLOYMENT

If you want to create a minimal deployment folder, you MUST include:

### Essential Core Files:
1. `start_all_servers.py`
2. `START_SERVERS.bat`

### Login Module (Complete Folder):
3. `Login Module/` - ALL files in this folder

### ITM Folder (Complete Folder):
4. `ITM/` - ALL files in this folder

### Home Page (Complete Folder):
5. `Home Page/` - ALL files in this folder

### Kings-and-Pigs-Main (Complete Folder):
6. `kings-and-pigs-main/` - ALL files and subfolders

### Loading Page (Complete Folder):
7. `Loading Page Animation/` - ALL files in this folder

### Mentorr (Optional):
8. `Mentorr/` - Only if you want AI mentor feature

### Root Files:
9. `video.mp4` - Background video
10. `mentor_memory.json` - Auto-created, but include if exists

---

## FOLDER STRUCTURE FOR DEPLOYMENT

```
YourGameFolder/
├── start_all_servers.py
├── START_SERVERS.bat
├── video.mp4
├── Login Module/
│   ├── auth_server.py
│   ├── .env
│   ├── login.html
│   ├── login.css
│   ├── login.js
│   ├── database_setup.sql
│   └── user_store.json
├── ITM/
│   ├── backend3ds.py
│   ├── battle_program.exe
│   ├── battle_code.cpp
│   ├── test_*.exe files
│   └── (all other ITM files)
├── Home Page/
│   ├── arena.html
│   ├── arena-styles.css
│   └── arena-script.js
├── kings-and-pigs-main/
│   ├── All HTML files
│   ├── All JS files
│   ├── img/ (complete folder)
│   ├── img2/ (complete folder)
│   ├── js/ (complete folder)
│   ├── js2/ (complete folder)
│   ├── src/ (complete folder)
│   └── (all config files)
├── Loading Page Animation/
│   └── (all files)
└── Mentorr/ (optional)
    └── mentor.py
```

---

## IMPORTANT NOTES

1. **DO NOT separate files** - Keep folder structures intact
2. **Database must be running** - MySQL with `c_game_db` database
3. **Environment variables** - Configure `Login Module/.env` properly
4. **Python packages** - Install all required packages
5. **Port availability** - Ensure ports 5000 and 5002 are free
6. **File paths** - All paths are relative, don't change folder structure

---

## HOW TO DEPLOY

1. Copy the entire folder structure as shown above
2. Install Python dependencies: `pip install flask flask-cors mysql-connector-python python-dotenv`
3. Set up MySQL database using `Login Module/database_setup.sql`
4. Configure `Login Module/.env` with your database credentials
5. Run `START_SERVERS.bat` or `python start_all_servers.py`
6. Access login page: Open `Login Module/login.html` in browser
7. Access arena: Open `Home Page/arena.html` in browser

---

## SERVERS STARTED BY start_all_servers.py

1. **Auth Server** (Port 5002) - `Login Module/auth_server.py`
2. **Arena Server** (Port 5000) - `ITM/backend3ds.py`
3. **Mentor App** (Optional) - `Mentorr/mentor.py`
