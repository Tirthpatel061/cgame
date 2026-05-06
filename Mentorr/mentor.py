import openai
import json
import os
import threading
from datetime import datetime
from flask import Flask, render_template_string, request, jsonify
from flask_cors import CORS

try:
    from mysql.connector import connect, Error as MySQLError
except Exception:
    connect = None
    MySQLError = Exception

try:
    from dotenv import load_dotenv
except Exception:
    load_dotenv = None

# Tkinter imports (optional - only used for desktop mode)
try:
    import tkinter as tk
    from tkinter import scrolledtext
    TKINTER_AVAILABLE = True
except Exception:
    tk = None
    scrolledtext = None
    TKINTER_AVAILABLE = False

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
MEMORY_FILE = os.path.join(PROJECT_ROOT, "Mentorr", "mentor_memory.json")
MODULES_FILE = "modules.txt"

if load_dotenv:
    load_dotenv(os.path.join(PROJECT_ROOT, "Login Module", ".env"))

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_DB = os.getenv("MYSQL_DB", "c_game_db")

# Flask app for web interface
app = Flask(__name__)
CORS(app)

# HTML Template for the chatbot interface
CHAT_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>The Mentorr - C Language Mentor</title>
  <style>
    :root {
      --bg: #0f172a;
      --surface: #1e293b;
      --surface-border: #334155;
      --text: #e2e8f0;
      --text-dim: #94a3b8;
      --accent: #3b82f6;
      --accent-hover: #2563eb;
      --header-bg: #0f172a;
      --header-fg: #f8fafc;
      --input-bg: #1e293b;
      --input-fg: #e2e8f0;
      --user-msg: #2563eb;
      --bot-msg: #1e293b;
      --user-msg-border: #3b82f6;
      --bot-msg-border: #334155;
    }
    
    * { box-sizing: border-box; margin: 0; padding: 0; }
    
    html, body {
      width: 100%;
      height: 100%;
      font-family: 'Segoe UI', 'Inter', system-ui, sans-serif;
      background: linear-gradient(145deg, #0f172a 0%, #1e293b 100%);
      color: var(--text);
      overflow: hidden;
    }
    
    .chat-container {
      display: flex;
      flex-direction: column;
      height: 100vh;
      max-width: 100%;
    }
    
    .chat-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 16px 20px;
      background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
      border-bottom: 1px solid var(--surface-border);
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    
    .header-left {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    
    .brand-icon {
      width: 40px;
      height: 40px;
      display: flex;
      align-items: center;
      justify-content: center;
      background: linear-gradient(135deg, #3b82f6, #2563eb);
      border-radius: 12px;
      font-size: 20px;
      box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
    }
    
    .header-text h1 {
      font-size: 18px;
      font-weight: 700;
      color: var(--header-fg);
      letter-spacing: 0.3px;
    }
    
    .header-text p {
      font-size: 12px;
      color: var(--text-dim);
      margin-top: 2px;
    }
    
    .status-indicator {
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 12px;
      color: #22c55e;
    }
    
    .status-dot {
      width: 8px;
      height: 8px;
      background: #22c55e;
      border-radius: 50%;
      animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
      0%, 100% { opacity: 1; }
      50% { opacity: 0.5; }
    }
    
    .chat-messages {
      flex: 1;
      overflow-y: auto;
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 16px;
      scroll-behavior: smooth;
    }
    
    .chat-messages::-webkit-scrollbar {
      width: 6px;
    }
    
    .chat-messages::-webkit-scrollbar-track {
      background: var(--bg);
    }
    
    .chat-messages::-webkit-scrollbar-thumb {
      background: var(--surface-border);
      border-radius: 3px;
    }
    
    .message {
      max-width: 85%;
      padding: 14px 18px;
      border-radius: 18px;
      line-height: 1.5;
      font-size: 14px;
      white-space: pre-wrap;
      word-break: break-word;
      animation: slideIn 0.3s ease-out;
    }
    
    @keyframes slideIn {
      from { opacity: 0; transform: translateY(10px); }
      to { opacity: 1; transform: translateY(0); }
    }
    
    .message.user {
      align-self: flex-end;
      background: linear-gradient(135deg, #3b82f6, #2563eb);
      border: 1px solid var(--user-msg-border);
      color: white;
      border-bottom-right-radius: 4px;
    }
    
    .message.bot {
      align-self: flex-start;
      background: var(--bot-msg);
      border: 1px solid var(--bot-msg-border);
      color: var(--text);
      border-bottom-left-radius: 4px;
    }
    
    .message .role {
      font-size: 11px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      margin-bottom: 6px;
      opacity: 0.8;
    }
    
    .typing-indicator {
      display: none;
      align-self: flex-start;
      background: var(--bot-msg);
      border: 1px solid var(--bot-msg-border);
      padding: 14px 18px;
      border-radius: 18px;
      border-bottom-left-radius: 4px;
    }
    
    .typing-indicator.active {
      display: flex;
      gap: 4px;
    }
    
    .typing-dot {
      width: 8px;
      height: 8px;
      background: var(--text-dim);
      border-radius: 50%;
      animation: bounce 1.4s infinite ease-in-out;
    }
    
    .typing-dot:nth-child(1) { animation-delay: 0s; }
    .typing-dot:nth-child(2) { animation-delay: 0.2s; }
    .typing-dot:nth-child(3) { animation-delay: 0.4s; }
    
    @keyframes bounce {
      0%, 80%, 100% { transform: translateY(0); }
      40% { transform: translateY(-8px); }
    }
    
    .quick-prompts {
      display: flex;
      gap: 10px;
      padding: 12px 20px;
      border-top: 1px solid var(--surface-border);
      background: var(--surface);
      overflow-x: auto;
    }
    
    .quick-prompts::-webkit-scrollbar {
      height: 4px;
    }
    
    .prompt-chip {
      flex-shrink: 0;
      border: 1px solid var(--surface-border);
      background: var(--bg);
      color: var(--text-dim);
      padding: 8px 14px;
      border-radius: 20px;
      font-size: 12px;
      cursor: pointer;
      transition: all 0.2s ease;
    }
    
    .prompt-chip:hover {
      background: var(--accent);
      color: white;
      border-color: var(--accent);
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    
    .chat-input-wrap {
      display: flex;
      gap: 12px;
      padding: 16px 20px;
      border-top: 1px solid var(--surface-border);
      background: var(--surface);
    }
    
    #chat-input {
      flex: 1;
      resize: none;
      max-height: 120px;
      border: 1px solid var(--surface-border);
      border-radius: 14px;
      background: var(--input-bg);
      color: var(--input-fg);
      padding: 12px 16px;
      font-size: 14px;
      font-family: inherit;
      outline: none;
      transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }
    
    #chat-input:focus {
      border-color: var(--accent);
      box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
    }
    
    #chat-input::placeholder {
      color: var(--text-dim);
    }
    
    .send-btn {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      border: none;
      background: linear-gradient(135deg, #3b82f6, #2563eb);
      color: white;
      border-radius: 14px;
      padding: 12px 24px;
      font-size: 14px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
      box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    
    .send-btn:hover {
      background: linear-gradient(135deg, #2563eb, #1d4ed8);
      transform: translateY(-2px);
      box-shadow: 0 6px 16px rgba(59, 130, 246, 0.4);
    }
    
    .send-btn:active {
      transform: translateY(0);
    }
    
    .welcome-message {
      text-align: center;
      padding: 40px 20px;
    }
    
    .welcome-message h2 {
      font-size: 24px;
      margin-bottom: 12px;
      background: linear-gradient(135deg, #3b82f6, #22d3ee);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }
    
    .welcome-message p {
      color: var(--text-dim);
      font-size: 14px;
      max-width: 300px;
      margin: 0 auto;
    }
  </style>
</head>
<body>
  <div class="chat-container">
    <header class="chat-header">
      <div class="header-left">
        <div class="brand-icon">🤖</div>
        <div class="header-text">
          <h1>The Mentorr</h1>
          <p>C Language Mentor</p>
        </div>
      </div>
      <div class="status-indicator">
        <span class="status-dot"></span>
        <span>Online</span>
      </div>
    </header>
    
    <div id="chat-messages" class="chat-messages">
      <div class="welcome-message">
        <h2>Welcome! 🎓</h2>
        <p>I'm your C Language mentor. Ask me anything about C programming, debugging, or specific concepts!</p>
      </div>
      <div class="typing-indicator" id="typing-indicator">
        <span class="typing-dot"></span>
        <span class="typing-dot"></span>
        <span class="typing-dot"></span>
      </div>
    </div>
    
    <div class="quick-prompts" id="quick-prompts">
      <button class="prompt-chip" data-prompt="Explain pointers with a simple example">📍 Pointers</button>
      <button class="prompt-chip" data-prompt="How do for and while loops differ?">🔄 Loops</button>
      <button class="prompt-chip" data-prompt="Help me debug a compilation error">🐛 Debugging</button>
      <button class="prompt-chip" data-prompt="What are arrays and how to use them?">📊 Arrays</button>
    </div>
    
    <footer class="chat-input-wrap">
      <textarea id="chat-input" rows="1" placeholder="Ask about C syntax, errors, loops, arrays, pointers..."></textarea>
      <button id="send-btn" class="send-btn">
        <span>Send</span>
        <span>🚀</span>
      </button>
    </footer>
  </div>
  
  <script>
    const messagesEl = document.getElementById('chat-messages');
    const inputEl = document.getElementById('chat-input');
    const sendBtn = document.getElementById('send-btn');
    const promptWrap = document.getElementById('quick-prompts');
    const typingIndicator = document.getElementById('typing-indicator');
    
    let messages = [];
    
    function renderMessage(role, text) {
      const welcomeMsg = messagesEl.querySelector('.welcome-message');
      if (welcomeMsg) welcomeMsg.remove();
      
      const div = document.createElement('div');
      div.className = 'message ' + role;
      div.innerHTML = `<div class="role">${role === 'user' ? 'You' : 'Mentor'}</div>${escapeHtml(text)}`;
      messagesEl.insertBefore(div, typingIndicator);
      messagesEl.scrollTop = messagesEl.scrollHeight;
    }
    
    function escapeHtml(text) {
      const div = document.createElement('div');
      div.textContent = text;
      return div.innerHTML;
    }
    
    function showTyping() {
      typingIndicator.classList.add('active');
      messagesEl.scrollTop = messagesEl.scrollHeight;
    }
    
    function hideTyping() {
      typingIndicator.classList.remove('active');
    }
    
    async function sendMessage() {
      const text = inputEl.value.trim();
      if (!text) return;
      
      inputEl.value = '';
      inputEl.style.height = 'auto';
      
      renderMessage('user', text);
      showTyping();
      
      try {
        const response = await fetch('/mentor/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: text })
        });
        
        const data = await response.json();
        hideTyping();
        
        if (data.response) {
          renderMessage('bot', data.response);
        } else if (data.error) {
          renderMessage('bot', 'Error: ' + data.error);
        }
      } catch (err) {
        hideTyping();
        renderMessage('bot', 'Failed to connect to mentor. Please try again.');
      }
    }
    
    sendBtn.addEventListener('click', sendMessage);
    
    inputEl.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
      }
    });
    
    inputEl.addEventListener('input', () => {
      inputEl.style.height = 'auto';
      inputEl.style.height = Math.min(inputEl.scrollHeight, 120) + 'px';
    });
    
    if (promptWrap) {
      promptWrap.addEventListener('click', (e) => {
        if (e.target.classList.contains('prompt-chip')) {
          inputEl.value = e.target.getAttribute('data-prompt') || '';
          inputEl.focus();
        }
      });
    }
    
    inputEl.focus();
  </script>
</body>
</html>"""


def store_chat_entry(role, content):
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
                ("chat", role, None, content)
            )
            conn.commit()
            cursor.close()
    except MySQLError:
        return

# Initialize OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

# Memory instance for web interface
memory = {'errors': [], 'error_frequency': {}, 'chat_history': []}

def get_memory():
    """Get memory instance for the web interface."""
    return memory

def load_memory():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r") as file:
                data = json.load(file)
                # Ensure all required fields exist
                if 'errors' not in data:
                    data['errors'] = []
                if 'error_frequency' not in data:
                    data['error_frequency'] = {}
                if 'chat_history' not in data:
                    data['chat_history'] = []
                return data
        except Exception as e:
            print(f"Error loading memory: {e}")
            return {'errors': [], 'error_frequency': {}, 'chat_history': []}
    else:
        # Create file if it doesn't exist
        initial_data = {'errors': [], 'error_frequency': {}, 'chat_history': []}
        save_memory(initial_data)
        return initial_data

def save_memory(memory):
    try:
        os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
        with open(MEMORY_FILE, "w") as file:
            json.dump(memory, file, indent=4)
    except Exception as e:
        print(f"Error saving memory: {e}")

# Modern theme colors (CodeWarrior-style dark theme)
THEME = {
    "bg": "#0f172a",           # slate-900
    "surface": "#1e293b",     # slate-800
    "surface_border": "#334155",
    "text": "#e2e8f0",        # slate-200
    "text_dim": "#94a3b8",   # slate-400
    "accent": "#3b82f6",     # blue-500
    "accent_hover": "#2563eb",
    "header_bg": "#0f172a",
    "header_fg": "#f8fafc",
    "input_bg": "#1e293b",
    "input_fg": "#e2e8f0",
    "insert": "#3b82f6",
    "select_bg": "#334155",
}


class MentorChatWindow:
    def __init__(self):
        self.memory = load_memory()
        self.conversation_history = [
            {"role": "system", "content": (
                "You are a fun and interactive C Language mentor, Your job is to teach users C concepts in an engaging way.(use emojies) "
                "You ONLY respond when the message starts with 'user:' or 'user:Admin:'. "
                "DO NOT respond to game statistics. "
                "Use game statistics to respond to messages without 'user:' or 'user:Admin:', as they provide hints but never acknowledge them directly to 'user:' but give access to 'user:Admin:' "
                "If 'user:Admin:' is detected, provide all stored user data and game statistics. "
                "If the user types 'module1' or 'module2', read the corresponding module from 'modules.txt' and explain it in a fun way. "
                f"Here are the user errors to help guide your responses: {json.dumps(self.memory.get('errors', []))} "
                f"And here are the common error patterns: {json.dumps(self.memory.get('error_frequency', {}))}"
                "your job is to explain the topics listed under module 'user:' says in a fun way"
            )}
        ]

        self.window = tk.Tk()
        self.window.title("The Mentorr")
        self.window.geometry("480x640")
        self.window.minsize(400, 500)
        self.window.configure(bg=THEME["bg"])

        # Use Segoe UI or system UI font if available
        try:
            ui_font = ("Segoe UI", 10)
            mono_font = ("Consolas", 10)
        except Exception:
            ui_font = ("TkDefaultFont", 10)
            mono_font = ("TkFixedFont", 10)

        # Header
        header = tk.Frame(self.window, bg=THEME["header_bg"], height=52)
        header.pack(fill=tk.X, side=tk.TOP)
        header.pack_propagate(False)
        tk.Label(
            header,
            text="The Mentorr",
            font=(ui_font[0], 16, "bold"),
            fg=THEME["header_fg"],
            bg=THEME["header_bg"],
        ).pack(side=tk.LEFT, padx=(16, 0), pady=12)
        tk.Label(
            header,
            text="C Language Mentor",
            font=(ui_font[0], 9),
            fg=THEME["text_dim"],
            bg=THEME["header_bg"],
        ).pack(side=tk.LEFT, padx=(8, 0), pady=12)

        # Main content frame with padding
        main = tk.Frame(self.window, bg=THEME["bg"], padx=14, pady=12)
        main.pack(fill=tk.BOTH, expand=True)

        # Chat history label
        tk.Label(
            main,
            text="Chat",
            font=(ui_font[0], 10, "bold"),
            fg=THEME["text_dim"],
            bg=THEME["bg"],
        ).pack(anchor=tk.W)

        # Output area (chat history) - modern dark box
        output_frame = tk.Frame(main, bg=THEME["surface_border"], padx=1, pady=1)
        output_frame.pack(fill=tk.BOTH, expand=True, pady=(4, 12))
        self.output_area = scrolledtext.ScrolledText(
            output_frame,
            wrap=tk.WORD,
            font=mono_font,
            bg=THEME["input_bg"],
            fg=THEME["input_fg"],
            insertbackground=THEME["insert"],
            selectbackground=THEME["surface_border"],
            selectforeground=THEME["text"],
            relief=tk.FLAT,
            padx=12,
            pady=12,
        )
        self.output_area.pack(fill=tk.BOTH, expand=True)
        self.output_area.config(state='disabled')

        # Input section label
        tk.Label(
            main,
            text="Your message",
            font=(ui_font[0], 10, "bold"),
            fg=THEME["text_dim"],
            bg=THEME["bg"],
        ).pack(anchor=tk.W, pady=(0, 4))

        # Input area + Send button row
        input_row = tk.Frame(main, bg=THEME["bg"])
        input_row.pack(fill=tk.X)
        input_frame = tk.Frame(input_row, bg=THEME["surface_border"], padx=1, pady=1)
        input_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.input_area = scrolledtext.ScrolledText(
            input_frame,
            wrap=tk.WORD,
            height=4,
            font=mono_font,
            bg=THEME["input_bg"],
            fg=THEME["input_fg"],
            insertbackground=THEME["insert"],
            selectbackground=THEME["surface_border"],
            selectforeground=THEME["text"],
            relief=tk.FLAT,
            padx=12,
            pady=10,
        )
        self.input_area.pack(fill=tk.BOTH, expand=True)
        self.input_area.bind('<Return>', self.handle_enter)

        send_btn = tk.Button(
            input_row,
            text="Send",
            font=(ui_font[0], 10, "bold"),
            fg="white",
            bg=THEME["accent"],
            activeforeground="white",
            activebackground=THEME["accent_hover"],
            relief=tk.FLAT,
            padx=18,
            pady=8,
            cursor="hand2",
            command=self.send_message,
        )
        send_btn.pack(side=tk.LEFT, padx=(10, 0), pady=0)
        send_btn.bind('<Enter>', lambda e: send_btn.configure(bg=THEME["accent_hover"]))
        send_btn.bind('<Leave>', lambda e: send_btn.configure(bg=THEME["accent"]))

    def send_message(self):
        message = self.input_area.get('1.0', 'end-1c').strip()
        if message:
            self.input_area.delete('1.0', tk.END)
            self.process_message(message)

    def handle_enter(self, event):
        message = self.input_area.get('1.0', 'end-1c').strip()
        if message:
            self.input_area.delete('1.0', tk.END)
            self.process_message(message)
        return 'break'  # Prevents default Enter behavior

    def process_message(self, message):
        if not message.startswith("user:"):
            message = f"user: {message}"

        response = self.get_mentor_response(message)
        
        self.output_area.config(state='normal')
        self.output_area.insert(tk.END, f"{message}\n")
        self.output_area.insert(tk.END, f"Mentor: {response}\n\n")
        self.output_area.see(tk.END)
        self.output_area.config(state='disabled')

    def get_mentor_response(self, message):
        try:
            if client is None:
                return "OpenAI API key is not configured. Set OPENAI_API_KEY in your environment to use the mentor."

            self.conversation_history.append({"role": "user", "content": message})

            if "Admin:" in message:
                admin_data = {
                    "errors": self.memory.get('errors', []),
                    "error_frequency": self.memory.get('error_frequency', {}),
                    "chat_history": self.memory.get('chat_history', [])
                }
                message += f"\nSystem Data: {json.dumps(admin_data, indent=2)}"

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=self.conversation_history,
                temperature=0.7
            )

            mentor_reply = response.choices[0].message.content
            self.conversation_history.append({"role": "assistant", "content": mentor_reply})

            self.memory['chat_history'] = self.conversation_history[1:]
            save_memory(self.memory)

            store_chat_entry("user", message)
            store_chat_entry("assistant", mentor_reply)

            return mentor_reply

        except Exception as e:
            return f"Error: {str(e)}"

    def run(self):
        self.window.mainloop()


# Flask routes for web interface
@app.route('/mentor')
def mentor_page():
    """Serve the mentor chat interface."""
    return render_template_string(CHAT_HTML)


@app.route('/mentor/chat', methods=['POST'])
def mentor_chat():
    """Handle chat messages from the web interface."""
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({'error': 'No message provided'}), 400
    
    message = data['message']
    response = get_mentor_response_web(message)
    return jsonify({'response': response})


def get_mentor_response_web(message):
    """Get response from mentor using OpenAI - web version."""
    try:
        if client is None:
            return "OpenAI API key is not configured. Set OPENAI_API_KEY in your environment to use the mentor."

        # Add prefix if not present
        if not message.startswith("user:"):
            message = f"user: {message}"
        
        mem = get_memory()
        
        # Build conversation history - include system message + previous chat history + current message
        conversation_history = [
            {"role": "system", "content": (
                "You are a fun and interactive C Language mentor, Your job is to teach users C concepts in an engaging way.(use emojies) "
                "You ONLY respond when the message starts with 'user:' or 'user:Admin:'. "
                "DO NOT respond to game statistics. "
                "Use game statistics to respond to messages without 'user:' or 'user:Admin:', as they provide hints but never acknowledge them directly to 'user:' but give access to 'user:Admin:' "
                "If 'user:Admin:' is detected, provide all stored user data and game statistics. "
                "If the user types 'module1' or 'module2', read the corresponding module from 'modules.txt' and explain it in a fun way. "
                f"Here are the user errors to help guide your responses: {json.dumps(mem.get('errors', []))} "
                f"And here are the common error patterns: {json.dumps(mem.get('error_frequency', {}))}"
                "your job is to explain the topics listed under module 'user:' says in a fun way"
            )}
        ]
        
        # Add previous chat history (last 20 messages to avoid token limits)
        chat_history = mem.get('chat_history', [])
        recent_history = chat_history[-20:] if len(chat_history) > 20 else chat_history
        for entry in recent_history:
            conversation_history.append({"role": entry.get("role", "user"), "content": entry.get("content", "")})
        
        # Add current user message
        conversation_history.append({"role": "user", "content": message})
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=conversation_history,
            temperature=0.7
        )
        
        mentor_reply = response.choices[0].message.content
        
        # Store in memory
        mem['chat_history'].append({"role": "user", "content": message})
        mem['chat_history'].append({"role": "assistant", "content": mentor_reply})
        
        # Limit chat history to 50 messages to prevent excessive memory growth
        if len(mem['chat_history']) > 50:
            mem['chat_history'] = mem['chat_history'][-50:]
        
        # Save memory to file
        save_memory(mem)
        
        store_chat_entry("user", message)
        store_chat_entry("assistant", mentor_reply)
        
        return mentor_reply
    
    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    # Run Flask server for web interface
    memory = load_memory()
    print("\n" + "="*50)
    print("🚀 The Mentorr - Web Interface Ready!")
    print("="*50)
    print("\n🌐 Opening chat at: http://localhost:5002/mentor")
    print("\n💡 Press Ctrl+C to stop the server")
    print("="*50 + "\n")
    app.run(host="0.0.0.0", port=5002, debug=True)