# CodeWarrior Arena Server

This server connects the `backend3ds.py` file with the `arena.html` file, providing a complete web-based experience for the CodeWarrior Arena.

## Features

- 🌐 Serves `arena.html` as the main page at `http://localhost:5000`
- 🚀 Automatically opens the arena in your browser when server starts
- ⚡ Provides backend API for game challenges and code evaluation
- 📁 Serves all static files (CSS, JS, images, videos) from the project
- 🔗 Handles navigation between different pages (loading, login, game levels)

## How to Run

### Method 1: Using the Batch File (Windows)
```bash
# Double-click or run from command prompt
start_server.bat
```

### Method 2: Using Python Launcher
```bash
python run_arena.py
```

### Method 3: Direct Python Execution
```bash
python backend3ds.py
```

## What Happens When You Run

1. **Server Starts**: Flask server starts on `http://localhost:5000`
2. **Browser Opens**: Your default browser automatically opens to the arena page
3. **Full Navigation**: All links and navigation work properly
4. **Game Backend**: API endpoints are ready for game challenges

## Server Endpoints

- `GET /` - Serves the main arena.html page
- `GET /Home Page/<file>` - Serves files from Home Page directory
- `GET /Loading Page Animation/<file>` - Serves loading page files
- `GET /Login Module/<file>` - Serves login module files
- `GET /kings-and-pigs-main/<file>` - Serves game files
- `GET /video.mp4` - Serves the background video
- `POST /evaluate` - Evaluates C code submissions
- `GET /get-challenge` - Gets coding challenges
- `POST /reset` - Resets game progress
- `POST /store_error` - Stores error data

## File Structure Expected

```
project_root/
├── ITM/
│   ├── backend3ds.py          # Main server file
│   ├── start_server.bat       # Windows batch launcher
│   └── run_arena.py           # Python launcher
├── Home Page/
│   ├── arena.html             # Main arena page
│   ├── arena-styles.css       # Arena styles
│   └── arena-script.js        # Arena JavaScript
├── Loading Page Animation/    # Loading page files
├── Login Module/             # Login system files
├── kings-and-pigs-main/      # Game files
└── video.mp4                 # Background video
```

## Troubleshooting

### Server Won't Start
- Make sure Python is installed and in PATH
- Check that all required files exist in the correct directories
- Ensure port 5000 is not already in use

### Browser Doesn't Open
- The server will still work at `http://localhost:5000`
- Manually navigate to the URL in your browser

### Files Not Loading
- Check the console output for file path errors
- Ensure all directories and files exist as expected
- Check file permissions

### Game Challenges Not Working
- Make sure you have a C compiler (g++) installed
- Check that MinGW is in your PATH (for Windows)
- Verify the ITM directory has write permissions for temporary files

## Dependencies

- Python 3.6+
- Flask
- Flask-CORS
- A C compiler (g++ recommended)

Install Python dependencies:
```bash
pip install flask flask-cors
```

## Notes

- The server automatically handles CORS for cross-origin requests
- All file paths are configured to work with the Flask server
- The server includes detailed logging for debugging
- Browser opens automatically after a 1.5-second delay to ensure server is ready