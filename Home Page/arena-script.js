const chatBtn = document.getElementById('chat-btn');
const chatPanel = document.getElementById('chat-panel');
const closeBtn = document.getElementById('close-chat');
const messageInput = document.getElementById('message-input');
const sendBtn = document.getElementById('send-btn');
const messagesContainer = document.getElementById('messages');

const initialMessage = {
  text: "Hi! I'm your CodeWarrior Arena assistant. Ask me anything about C programming or our platform!",
  isUser: false
};

let messages = [initialMessage];

const responsePatterns = {
  about: {
    patterns: ['codewarrior', 'about', 'platform', 'website'],
    response: "CodeWarrior Arena is an interactive C programming learning platform that gamifies coding education! We transform learning into an exciting space adventure where you complete challenges, level up your skills, and compete with other coders."
  },
  progression: {
    patterns: ['level', 'progression', 'how does it work'],
    response: "Our platform has multiple levels from Beginner to Expert! Start with basic syntax, progress through data structures, and master advanced algorithms. Each level unlocks new challenges and earns you badges. Complete missions to advance through the ranks!"
  },
  cprogramming: {
    patterns: ['c programming', 'basics', 'learn c'],
    response: "C is a powerful programming language! We cover everything from variables, loops, and functions to pointers, memory management, and data structures. Each concept is taught through interactive coding challenges in our game environment."
  },
  gettingstarted: {
    patterns: ['start', 'begin', 'getting started'],
    response: "Getting started is easy! Click the 'Launch Mission' button to create your account. You'll start in the Rookie Bay with simple challenges. Complete the tutorial missions to learn the basics, then progress through increasingly difficult levels!"
  },
  game: {
    patterns: ['game', 'play', 'challenge'],
    response: "Each challenge is a mission! Write C code to solve problems, debug errors, and optimize solutions. Earn stars based on code efficiency and correctness. Unlock achievements and climb the leaderboard as you complete more missions!"
  },
  greeting: {
    patterns: ['hello', 'hi', 'hey'],
    response: "Hello, Space Cadet! Ready to embark on your coding journey? Ask me anything about CodeWarrior Arena or C programming!"
  }
};

function getResponse(question) {
  const lowerQuestion = question.toLowerCase();

  for (const category in responsePatterns) {
    const { patterns, response } = responsePatterns[category];
    if (patterns.some(pattern => lowerQuestion.includes(pattern))) {
      return response;
    }
  }

  return "Great question! CodeWarrior Arena offers comprehensive C programming courses through an engaging game format. Try asking about our levels, C programming basics, or how to get started!";
}

function renderMessages() {
  messagesContainer.innerHTML = '';

  messages.forEach(message => {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${message.isUser ? 'user' : 'assistant'}`;

    const bubble = document.createElement('div');
    bubble.className = 'message-bubble';
    bubble.textContent = message.text;

    messageDiv.appendChild(bubble);
    messagesContainer.appendChild(messageDiv);
  });

  messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function sendMessage() {
  const text = messageInput.value.trim();

  if (!text) return;

  const userMessage = { text, isUser: true };
  messages.push(userMessage);
  messageInput.value = '';
  renderMessages();

  setTimeout(() => {
    const response = getResponse(text);
    const botMessage = { text: response, isUser: false };
    messages.push(botMessage);
    renderMessages();
  }, 500);
}

function toggleChat() {
  const isOpen = !chatPanel.classList.contains('hidden');

  if (isOpen) {
    chatPanel.classList.add('hidden');
    chatBtn.classList.remove('open');
  } else {
    chatPanel.classList.remove('hidden');
    chatBtn.classList.add('open');
    messageInput.focus();
  }
}

chatBtn.addEventListener('click', toggleChat);

closeBtn.addEventListener('click', () => {
  chatPanel.classList.add('hidden');
  chatBtn.classList.remove('open');
});

sendBtn.addEventListener('click', sendMessage);

messageInput.addEventListener('keypress', (event) => {
  if (event.key === 'Enter') {
    sendMessage();
  }
});

renderMessages();
