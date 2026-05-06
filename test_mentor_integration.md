# Mentor Integration Test Guide

## What Was Changed

### 1. `start_all_servers.py`
- Added `hide_window` parameter to `start_process()` function
- Mentor app now starts with `CREATE_NO_WINDOW` flag on Windows
- Console window is hidden when servers start
- Mentor runs in background, ready to be shown when button is clicked

### 2. `Login Module/auth_server.py`
- Added new endpoint: `/mentor/show` (POST/GET)
- Endpoint launches mentor.py with visible window using `CREATE_NEW_CONSOLE`
- Returns JSON response indicating success/failure

### 3. `kings-and-pigs-main/index - Copy.html`
- Removed web-based chat modal (HTML, CSS, JavaScript)
- Updated `toggleMentorChat()` to call backend endpoint
- Button now launches actual Python Tkinter application
- Simplified code - no more fake chat responses

## How It Works

1. When you run `start_all_servers.py`:
   - Auth server starts on port 5002
   - Arena server starts
   - Mentor.py starts in HIDDEN mode (no console window)

2. When user clicks "💬 Mentor" button:
   - JavaScript calls `http://localhost:5002/mentor/show`
   - Backend launches a NEW instance of mentor.py with VISIBLE window
   - Tkinter GUI appears on screen
   - User can interact with the AI mentor

## Testing Steps

1. Start all servers:
   ```cmd
   python start_all_servers.py
   ```
   
2. Verify output shows:
   ```
   [start] auth_server
   [start] backend3ds
   [start] mentor
   
   ✓ All servers started successfully!
     - Auth Server: Running
     - Arena Server: Running
     - Mentor App: Running in background (click Mentor button to open)
   ```

3. Open `kings-and-pigs-main/index - Copy.html` in browser

4. Click the "💬 Mentor" button in bottom-right corner

5. Verify:
   - Mentor Tkinter window appears
   - No console window is visible
   - You can type messages and get AI responses

## Troubleshooting

### Mentor button doesn't work
- Check browser console for errors
- Verify auth server is running on port 5002
- Check CORS is enabled

### Mentor window doesn't appear
- Check if Python is in PATH
- Verify mentor.py exists at `Mentorr/mentor.py`
- Check OpenAI API key is valid in mentor.py

### Multiple mentor windows open
- This is expected behavior - each click launches a new instance
- Close extra windows manually if needed
- Future enhancement: track process and bring existing window to front

## Files Modified
1. `start_all_servers.py` - Added hide_window functionality
2. `Login Module/auth_server.py` - Added /mentor/show endpoint
3. `kings-and-pigs-main/index - Copy.html` - Simplified to launch Python app
