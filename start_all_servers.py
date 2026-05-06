import os
import sys
import time
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

AUTH_SERVER = os.path.join(BASE_DIR, "Login Module", "auth_server.py")
ARENA_SERVER = os.path.join(BASE_DIR, "ITM", "backend3ds.py")
MENTOR_APP = os.path.join(BASE_DIR, "Mentorr", "mentor.py")


def start_process(script_path, name, hide_window=False):
    if not os.path.exists(script_path):
        print(f"[skip] {name} not found at {script_path}")
        return None

    print(f"[start] {name}")
    
    # Hide console window for mentor app on Windows
    if hide_window and sys.platform == 'win32':
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        return subprocess.Popen(
            [sys.executable, script_path], 
            cwd=os.path.dirname(script_path),
            startupinfo=startupinfo,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
    else:
        return subprocess.Popen([sys.executable, script_path], cwd=os.path.dirname(script_path))


def main():
    processes = []
    processes.append(start_process(AUTH_SERVER, "auth_server"))
    processes.append(start_process(ARENA_SERVER, "backend3ds"))
    # Start mentor in background without showing console window
    # processes.append(start_process(MENTOR_APP, "mentor", hide_window=True))

    processes = [p for p in processes if p is not None]
    if not processes:
        print("No servers started.")
        return

    print("\n✓ All servers started successfully!")
    print("  - Auth Server: Running")
    print("  - Arena Server: Running")
    print("  - Mentor Chatbot: Opens only when mentor button is clicked")
    print("\nPress Ctrl+C to stop all servers...\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping servers...")
        for process in processes:
            process.terminate()


if __name__ == "__main__":
    main()



