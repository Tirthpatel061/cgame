import subprocess
import os
import json
import sys
import time
import webbrowser
import threading
from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
from datetime import datetime

try:
    from mysql.connector import connect, Error as MySQLError
except Exception:
    connect = None
    MySQLError = Exception

try:
    from dotenv import load_dotenv
except Exception:
    load_dotenv = None

app = Flask(__name__)
CORS(app, origins='*', methods=['GET', 'POST', 'OPTIONS'], allow_headers=['Content-Type'])

# Enable logging
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Get the script directory for setting working directory
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)  # Go up one level to access Home Page folder

if load_dotenv:
    load_dotenv(os.path.join(project_root, 'Login Module', '.env'))

MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_DB = os.getenv("MYSQL_DB", "c_game_db")


def store_mentor_entry(entry_type, content, role=None, task_number=None):
    if not connect:
        return
    try:
        with connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB
        ) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS mentor_history (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    entry_type VARCHAR(20) NOT NULL,
                    role VARCHAR(20) NULL,
                    task_number INT NULL,
                    content TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            cursor.execute(
                """
                INSERT INTO mentor_history (entry_type, role, task_number, content)
                VALUES (%s, %s, %s, %s)
                """,
                (entry_type, role, task_number, content)
            )
            conn.commit()
            cursor.close()
    except MySQLError:
        return

# Use simple filenames since we'll set cwd
temp_cpp = "battle_code.cpp"
temp_exe = "battle_program.exe" if os.name == 'nt' else "battle_program"

# Function to open browser after server starts
def open_browser():
    time.sleep(1.5)  # Wait for server to start
    webbrowser.open('http://localhost:5000/')

# Route to serve the arena.html file as the main page
@app.route('/')
def serve_arena():
    try:
        arena_path = os.path.join(project_root, 'Home Page', 'arena.html')
        if os.path.exists(arena_path):
            return send_file(arena_path)
        else:
            return f"Arena file not found at: {arena_path}", 404
    except Exception as e:
        logger.error(f"Error serving arena.html: {e}")
        return f"Error loading arena: {str(e)}", 500

# Route to serve static files from Home Page directory
@app.route('/Home Page/<path:filename>')
def serve_home_page_files(filename):
    try:
        home_page_dir = os.path.join(project_root, 'Home Page')
        return send_from_directory(home_page_dir, filename)
    except Exception as e:
        logger.error(f"Error serving file {filename}: {e}")
        return f"File not found: {filename}", 404

# Route to serve static files from other directories
@app.route('/static/<path:filename>')
def serve_static_files(filename):
    try:
        # Try to serve from various directories
        possible_dirs = [
            os.path.join(project_root, 'Loading Page Animation'),
            os.path.join(project_root, 'Login Module'),
            os.path.join(project_root, 'kings-and-pigs-main'),
            project_root
        ]
        
        for directory in possible_dirs:
            file_path = os.path.join(directory, filename)
            if os.path.exists(file_path):
                return send_file(file_path)
        
        return f"File not found: {filename}", 404
    except Exception as e:
        logger.error(f"Error serving static file {filename}: {e}")
        return f"Error serving file: {str(e)}", 500

# Route to serve video files
@app.route('/video.mp4')
def serve_video():
    try:
        video_path = os.path.join(project_root, 'video.mp4')
        if os.path.exists(video_path):
            return send_file(video_path)
        else:
            return "Video file not found", 404
    except Exception as e:
        logger.error(f"Error serving video: {e}")
        return f"Error serving video: {str(e)}", 500

# Route to serve tutorial videos (level1_tutorial.mp4 to level8_tutorial.mp4)
@app.route('/tutorial/<filename>')
def serve_tutorial_video(filename):
    try:
        # Validate filename to prevent directory traversal
        if not filename.endswith('.mp4') or '/' in filename or '\\' in filename:
            return "Invalid filename", 400
        
        # Check if it's a valid level tutorial (level1_tutorial.mp4 to level8_tutorial.mp4)
        valid_tutorials = [f'level{i}_tutorial.mp4' for i in range(1, 9)]
        if filename not in valid_tutorials:
            return f"Invalid tutorial video: {filename}", 400
        
        video_path = os.path.join(project_root, filename)
        if os.path.exists(video_path):
            logger.info(f"Serving tutorial video: {filename}")
            return send_file(video_path, mimetype='video/mp4')
        else:
            logger.warning(f"Tutorial video not found: {video_path}")
            return f"Tutorial video not found: {filename}", 404
    except Exception as e:
        logger.error(f"Error serving tutorial video {filename}: {e}")
        return f"Error serving tutorial video: {str(e)}", 500

# Route to serve files from Loading Page Animation
@app.route('/Loading Page Animation/<path:filename>')
def serve_loading_files(filename):
    try:
        loading_dir = os.path.join(project_root, 'Loading Page Animation')
        return send_from_directory(loading_dir, filename)
    except Exception as e:
        logger.error(f"Error serving loading file {filename}: {e}")
        return f"File not found: {filename}", 404

# Route to serve files from Login Module
@app.route('/Login Module/<path:filename>')
def serve_login_files(filename):
    try:
        login_dir = os.path.join(project_root, 'Login Module')
        return send_from_directory(login_dir, filename)
    except Exception as e:
        logger.error(f"Error serving login file {filename}: {e}")
        return f"File not found: {filename}", 404

# Route to serve files from kings-and-pigs-main
@app.route('/kings-and-pigs-main/<path:filename>')
def serve_game_files(filename):
    try:
        game_dir = os.path.join(project_root, 'kings-and-pigs-main')
        return send_from_directory(game_dir, filename)
    except Exception as e:
        logger.error(f"Error serving game file {filename}: {e}")
        return f"File not found: {filename}", 404

challenges = {
    1: [  # Level 1 - Basics of C
        {
            'desc': "1. Print 'Hello C!' using printf()",
            'expected': "Hello C!"
        },
        {
            'desc': "2. Declare two integers a=5, b=10 and print their sum using arithmetic operator",
            'expected': "15"
        },
        {
            'desc': "3. Declare a character variable with value 'A' and print it using printf()",
            'expected': "A"
        },
        {
            'desc': "4. Swap two variables: a=20, b=30. Print b then a after swapping (space separated)",
            'expected': "20 30"
        },
        {
            'desc': "5. Declare float variable with value 2.5 and int variable with value 4. Print their product using * operator ",
            'expected': "10.000000"
        }
    ],
    
    2: [  # Level 2 - Variables
        {
            'desc': "1. Declare an integer variable x=42 and print it",
            'expected': "42"
        },
        {
            'desc': "2. Declare float variable pi=3.14 and print it",
            'expected': "3.140000"
        },
        {
            'desc': "3. Declare char variable grade='B' and print it",
            'expected': "B"
        },
        {
            'desc': "4. Declare three variables: int a=10, b=20, c=30. Print their sum",
            'expected': "60"
        },
        {
            'desc': "5. Declare double variable price=99.99 and int quantity=3. Print total (price * quantity)",
            'expected': "299.970000"
        }
    ],
    
    3: [  # Level 3 - Loops
        {
            'desc': "1. Print numbers from 1 to 5 using for loop (each on new line)",
            'expected': "1\n2\n3\n4\n5"
        },
        {
            'desc': "2. Print even numbers from 2 to 10 using while loop (space separated)",
            'expected': "2 4 6 8 10"
        },
        {
            'desc': "3. Calculate sum of numbers from 1 to 10 using loop",
            'expected': "55"
        },
        {
            'desc': "4. Print multiplication table of 3 up to 3x3 (format: 3x1=3)",
            'expected': "3x1=3\n3x2=6\n3x3=9"
        },
        {
            'desc': "5. Count and print how many times digit 2 appears in number 2222",
            'expected': "4"
        }
    ],
    
    4: [  # Level 4 - Functions
        {
            'desc': "1. Create function to add two numbers. Call with 8 and 12, print result",
            'expected': "20"
        },
        {
            'desc': "2. Create function to find square of number. Call with 7, print result",
            'expected': "49"
        },
        {
            'desc': "3. Create function to check if number is even. Call with 6, print 1 if even, 0 if odd",
            'expected': "1"
        },
        {
            'desc': "4. Create function to find factorial of number. Call with 4, print result",
            'expected': "24"
        },
        {
            'desc': "5. Create function to find maximum of two numbers. Call with 15 and 25, print result",
            'expected': "25"
        }
    ],
    
    5: [  # Level 5 - Pointers
        {
            'desc': "1. Declare int variable x=100, create pointer to it, print value using pointer",
            'expected': "100"
        },
        {
            'desc': "2. Use pointer to swap two variables a=40, b=60. Print a then b after swap (space separated)",
            'expected': "60 40"
        },
        {
            'desc': "3. Create array {5,10,15}, use pointer to print second element",
            'expected': "10"
        },
        {
            'desc': "4. Print size of integer pointer using sizeof operator",
            'expected': "8"
        },
        {
            'desc': "5. Use pointer arithmetic to access third element of array {11,22,33,44}",
            'expected': "33"
        }
    ],
    
    6: [  # Level 6 - Strings
        {
            'desc': "1. Declare string 'Hello' and print its length using strlen()",
            'expected': "5"
        },
        {
            'desc': "2. Copy string 'World' to another string and print the copied string",
            'expected': "World"
        },
        {
            'desc': "3. Concatenate strings 'Good' and 'Morning' and print result",
            'expected': "GoodMorning"
        },
        {
            'desc': "4. Compare strings 'Apple' and 'Apple' using strcmp(), print 0 if equal",
            'expected': "0"
        },
        {
            'desc': "5. Convert string 'hello' to uppercase and print result",
            'expected': "HELLO"
        }
    ],
    
    7: [  # Level 7 - Arrays
        {
            'desc': "1. Declare array {1,2,3,4,5} and print sum of all elements",
            'expected': "15"
        },
        {
            'desc': "2. Find and print the largest element in array {10,5,8,20,3}",
            'expected': "20"
        },
        {
            'desc': "3. Print array {7,14,21} in reverse order (space separated)",
            'expected': "21 14 7"
        },
        {
            'desc': "4. Count how many even numbers are in array {1,2,3,4,5,6}",
            'expected': "3"
        },
        {
            'desc': "5. Find and print the index of element 15 in array {10,15,20,25} (0-based)",
            'expected': "1"
        }
    ],
    
    8: [  # Level 8 - Advanced
        {
            'desc': "1. Create recursive function to find factorial of 5",
            'expected': "120"
        },
        {
            'desc': "2. Implement binary search in sorted array {1,3,5,7,9} to find element 5, print index",
            'expected': "2"
        },
        {
            'desc': "3. Sort array {64,34,25,12} using bubble sort and print sorted array (space separated)",
            'expected': "12 25 34 64"
        },
        {
            'desc': "4. Create linked list with nodes 10->20->30, print sum of all nodes",
            'expected': "60"
        },
        {
            'desc': "5. Implement matrix multiplication of 2x2 matrices [[1,2],[3,4]] and [[5,6],[7,8]], print element at [0][0]",
            'expected': "19"
        }
    ]
}

current_level = 0
current_game_level = 1  # Which level (1-8) the player is currently on

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'Server is running!', 'message': 'Backend is connected and ready.'})

@app.route('/get-challenge', methods=['GET', 'OPTIONS'])
def get_challenge():
    # Handle preflight requests
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'OK'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET, OPTIONS')
        return response
        
    global current_level, current_game_level
    
    try:
        # Get level parameter from request (default to current game level)
        level = request.args.get('level', current_game_level, type=int)
        
        # If switching to a different level, reset to challenge 1
        if level != current_game_level:
            current_level = 0  # Reset to challenge 1
            current_game_level = level
            logger.info(f"Switched to Level {level} - starting from challenge 1")
        
        logger.debug(f"Requested level: {level}, current challenge: {current_level + 1}")
        
        # Check if level exists and has challenges
        if level not in challenges:
            logger.error(f"Level {level} not available")
            return jsonify({'message': f'Level {level} not available!'}), 400
            
        if current_level >= len(challenges[level]):
            logger.info(f"All challenges completed for level {level}")
            return jsonify({'message': f'All challenges completed for Level {level}!'}), 200
        
        challenge_data = {
            'challenge': challenges[level][current_level]['desc'],
            'level': level,
            'challenge_number': current_level + 1,
            'total_challenges': len(challenges[level])
        }
        
        logger.debug(f"Returning challenge data: {challenge_data}")
        return jsonify(challenge_data)
        
    except Exception as e:
        logger.error(f"Error in get_challenge: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/evaluate', methods=['POST', 'OPTIONS'])
def evaluate_code():
    # Handle preflight requests
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'OK'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        return response
    
    global current_level, current_game_level
    
    try:
        data = request.json
        logger.debug(f"Received request data: {data}")
        code = data.get('code') if data else None
        
        if not code:
            logger.error("No code provided in request")
            return jsonify({'result': "Error: No code to execute!"})

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({'result': f"Server error: {str(e)}"})

    # Write code to temporary file
    logger.debug(f"Writing code to {temp_cpp}:")
    logger.debug(f"Code content:\n{code}")
    try:
        with open(os.path.join(script_dir, temp_cpp), 'w') as f:
            f.write(code)
        logger.debug(f"File written successfully")
        # Verify file was written
        with open(os.path.join(script_dir, temp_cpp), 'r') as f:
            written_content = f.read()
        logger.debug(f"File content verification:\n{written_content}")
    except Exception as e:
        logger.error(f"Error writing file: {e}")
        return jsonify({'result': f"Error writing file: {str(e)}"})
    
    # Delete old executable if it exists to avoid Windows file locking issues
    output_file_path = os.path.join(script_dir, temp_exe)
    if os.path.exists(output_file_path):
        import time
        for attempt in range(3):
            try:
                os.remove(output_file_path)
                logger.debug(f"Deleted old executable: {output_file_path}")
                break
            except PermissionError:
                if attempt < 2:
                    logger.warning(f"File locked, waiting... (attempt {attempt+1}/3)")
                    time.sleep(0.5)
                else:
                    logger.warning(f"Could not delete old executable after 3 attempts, will overwrite")
            except Exception as e:
                logger.warning(f"Could not delete old executable: {e}")
                break

    # Compile and execute
    # Use full path to g++ to avoid PATH issues
    gpp_path = r"C:\msys64\mingw64\bin\g++.exe"
    if not os.path.exists(gpp_path):
        gpp_path = 'g++'  # Fallback to PATH if not in default location
    
    try:
        # Try compilation with detailed debugging
        logger.debug(f"Working directory: {script_dir}")
        logger.debug(f"g++ path exists: {os.path.exists(gpp_path)}")
        logger.debug(f"Input file exists: {os.path.exists(os.path.join(script_dir, temp_cpp))}")
        logger.debug(f"Compile command: {gpp_path} {temp_cpp} -o {temp_exe}")
        
        # Set up environment with MinGW in PATH
        env = os.environ.copy()
        mingw_bin = r"C:\msys64\mingw64\bin"
        if mingw_bin not in env.get('PATH', ''):
            env['PATH'] = mingw_bin + os.pathsep + env.get('PATH', '')
        logger.debug(f"PATH includes MinGW: {mingw_bin in env['PATH']}")
        
        # Try with explicit working directory and capture all output
        compile_result = subprocess.run(
            [gpp_path, temp_cpp, '-o', temp_exe],
            stderr=subprocess.STDOUT,  # Combine stderr with stdout
            stdout=subprocess.PIPE,
            text=True,
            cwd=script_dir,
            env=env,
            encoding='utf-8',
            errors='replace'
        )
        
        logger.debug(f"Compile return code: {compile_result.returncode}")
        logger.debug(f"Compile output: '{compile_result.stdout}'")
        logger.debug(f"Output file exists after compile: {os.path.exists(os.path.join(script_dir, temp_exe))}")
        
        # List files in directory to debug
        files_in_dir = os.listdir(script_dir)
        logger.debug(f"Files in directory after compile: {[f for f in files_in_dir if 'battle' in f.lower()]}")
        sys.stdout.flush()
    except FileNotFoundError as e:
        logger.error(f"FileNotFoundError: {e}")
        return jsonify({'result': "Error: g++ compiler not found!\n\nPlease install MinGW:\n1. Download from: https://sourceforge.net/projects/mingw/\n2. Install and add to PATH\n3. Restart the server"})
    except Exception as e:
        logger.error(f"Exception during compilation: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return jsonify({'result': f"Error during compilation: {str(e)}"})

    # Check if compilation succeeded by verifying output file exists
    # (g++ sometimes returns non-zero even on successful compilation with warnings)
    output_file_path = os.path.join(script_dir, temp_exe)
    if not os.path.exists(output_file_path):
        error_msg = compile_result.stdout if compile_result.stdout else ""
        if not error_msg.strip():
            error_msg = f"Compilation failed with exit code {compile_result.returncode}.\nThis may be a g++ configuration issue.\nPlease try restarting the server or check if g++ is working properly."
        logger.error(f"Compilation failed with error: {error_msg}")
        return jsonify({'result': f"Compilation Failed:\n{error_msg}"})
    
    logger.debug("Compilation successful! Executable created.")

    try:
        exec_cmd = [f'./{temp_exe}'] if os.name != 'nt' else [temp_exe]
        logger.debug(f"Executing: {exec_cmd} in {script_dir}")
        result = subprocess.run(
            exec_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=5,
            cwd=script_dir
        )
        output = result.stdout.strip()
        error = result.stderr.strip()
        logger.debug(f"Execution output: '{output}'")
        logger.debug(f"Execution error: '{error}'")
    except subprocess.TimeoutExpired:
        logger.error("Execution timeout")
        return jsonify({'result': "Timeout: Execution took too long!"})

    if error:
        logger.error(f"Runtime error: {error}")
        return jsonify({'result': f"Runtime Error: {error}"})

    if current_game_level not in challenges:
        logger.error(f"Invalid level: {current_game_level}")
        return jsonify({'result': f"Error: Level {current_game_level} not available"}), 400

    if current_level >= len(challenges[current_game_level]):
        logger.info(f"All challenges already completed for level {current_game_level}")
        return jsonify({
            'result': f"🎉 Level {current_game_level} Completed! All challenges conquered!\nYour warrior is victorious! 🏹",
            'success': True,
            'level_completed': True
        })

    expected = challenges[current_game_level][current_level]['expected']
    logger.debug(f"Comparing output '{output}' with expected '{expected}'")
    
    if output == expected:
        current_level += 1
        logger.info(f"✅ SUCCESS! Task {current_level} completed in Level {current_game_level}")
        logger.info(f"Progress: {current_level}/{len(challenges[current_game_level])} tasks completed")
        
        # Check if all challenges in current level are completed
        if current_level >= len(challenges[current_game_level]):
            logger.info(f"🎉 LEVEL {current_game_level} COMPLETED! All {len(challenges[current_game_level])} tasks conquered!")
            return jsonify({
                'result': f"🎉 Level {current_game_level} Completed! All challenges conquered!\nYour warrior is victorious! 🏹",
                'success': True,
                'level_completed': True
            })
        else:
            logger.info(f"Moving to next task: {current_level + 1}/{len(challenges[current_game_level])}")
            return jsonify({
                'result': "Success! Your warrior shoots the enemy! 🏹\nProceed to the next challenge.",
                'success': True
            })
    else:
        logger.warning(f"❌ FAILED! Task {current_level + 1} in Level {current_game_level}")
        logger.warning(f"Output mismatch. Got '{output}', expected '{expected}'")
        return jsonify({
            'result': f"Wrong Output!\n\nYour output: '{output}'\nExpected: '{expected}'\n\nTip: Check for exact match (including punctuation and spacing)"
        })

@app.route('/reset', methods=['POST'])
def reset_game():
    global current_level, current_game_level
    
    try:
        # Get level parameter from request (optional)
        data = request.json if request.json else {}
        level = data.get('level', current_game_level)
        
        # Reset to challenge 1 of the specified level
        current_level = 0  # This means challenge 1 (0-indexed)
        current_game_level = level
        
        logger.info(f"Game reset for Level {level} - starting from challenge 1")
        return jsonify({
            'message': f'Level {level} reset successfully. Starting from challenge 1.',
            'level': level,
            'challenge_number': 1,
            'total_challenges': len(challenges.get(level, []))
        })
        
    except Exception as e:
        logger.error(f"Error in reset_game: {str(e)}")
        return jsonify({'error': f'Reset failed: {str(e)}'}), 500

@app.route('/store_error', methods=['POST'])
def store_error():
    try:
        error_data = request.json.get('error')
        task_number = request.json.get('task_number', 0)
        
        # Use project-relative path for mentor_memory.json
        memory_file_path = os.path.join(project_root, 'Mentorr', 'mentor_memory.json')
        
        # Load existing errors
        try:
            with open(memory_file_path, 'r') as f:
                memory = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            memory = {'errors': [], 'error_frequency': {}}

        # Initialize sections if they don't exist
        if 'errors' not in memory:
            memory['errors'] = []
        if 'error_frequency' not in memory:
            memory['error_frequency'] = {}

        # Add new error with timestamp and task number
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        memory['errors'].append({
            'timestamp': timestamp,
            'task_number': task_number,
            'error': error_data
        })

        # Track error frequency
        error_key = f"Task {task_number}: {error_data}"
        memory['error_frequency'][error_key] = memory['error_frequency'].get(error_key, 0) + 1

        # Save back to file with proper indentation
        with open(memory_file_path, 'w') as f:
            json.dump(memory, f, indent=4)

        store_mentor_entry("error", error_data, task_number=task_number)

        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting CodeWarrior Arena Server...")
    print("📍 Server will be available at: http://localhost:5000")
    print("🌐 Arena page will open automatically in your browser")
    print("⚡ Backend API ready for game challenges")
    print("-" * 50)
    
    # Start browser in a separate thread
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Start the Flask server
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)