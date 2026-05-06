(function () {
  'use strict';

  // Resolve API endpoints dynamically so chat works on other devices too.
  function buildApiCandidates() {
    var candidates = [];
    if (window.MENTOR_API_URL) {
      candidates.push(window.MENTOR_API_URL);
    }

    var protocol = window.location && window.location.protocol;
    var origin = window.location && window.location.origin;
    var hostname = window.location && window.location.hostname;

    if (origin && origin !== 'null') {
      candidates.push(origin + '/auth/mentor/chat');
    }
    if ((protocol === 'http:' || protocol === 'https:') && hostname) {
      candidates.push(protocol + '//' + hostname + ':5002/auth/mentor/chat');
    }

    return candidates;
  }

  var API_CANDIDATES = buildApiCandidates();

  var messagesEl = document.getElementById('chat-messages');
  var inputEl = document.getElementById('chat-input');
  var sendBtn = document.getElementById('send-btn');
  var closeBtn = document.getElementById('close-btn');
  var promptWrap = document.getElementById('quick-prompts');

  if (!messagesEl || !inputEl || !sendBtn || !closeBtn) return;

  // Always start fresh - no previous messages
  var messages = [
    {
      role: 'bot',
      text: 'Welcome to CodeWarrior Mentor! 🎓\n\nI\'m your personal C Language mentor. Ask me anything about C programming - syntax, pointers, loops, arrays, debugging, or anything else!'
    }
  ];

  function render(messages) {
    messagesEl.innerHTML = '';
    messages.forEach(function (m) {
      var div = document.createElement('div');
      div.className = 'message ' + (m.role === 'user' ? 'user' : 'bot');
      div.textContent = m.text;
      messagesEl.appendChild(div);
    });
    messagesEl.scrollTop = messagesEl.scrollHeight;
  }

  // Show typing indicator
  function showTyping() {
    var typing = document.createElement('div');
    typing.className = 'message bot typing';
    typing.id = 'typing-indicator';
    typing.innerHTML = '<span class="typing-dot"></span><span class="typing-dot"></span><span class="typing-dot"></span>';
    messagesEl.appendChild(typing);
    messagesEl.scrollTop = messagesEl.scrollHeight;
  }

  // Hide typing indicator
  function hideTyping() {
    var typing = document.getElementById('typing-indicator');
    if (typing) typing.remove();
  }

  // Initial render - fresh start
  render(messages);

  // Send message to API
  async function sendMessage() {
    var text = inputEl.value.trim();
    if (!text) return;

    messages.push({ role: 'user', text: text });
    inputEl.value = '';
    inputEl.style.height = 'auto';
    render(messages);

    showTyping();

    try {
      var data = null;
      var lastError = null;

      for (var i = 0; i < API_CANDIDATES.length; i++) {
        try {
          var response = await fetch(API_CANDIDATES[i], {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text })
          });

          data = await response.json();
          if (response.ok) {
            break;
          }

          lastError = new Error((data && data.error) ? data.error : 'Request failed');
        } catch (candidateErr) {
          lastError = candidateErr;
        }
      }

      hideTyping();

      if (data && data.response) {
        messages.push({ role: 'bot', text: data.response });
      } else if (data && data.error) {
        messages.push({ role: 'bot', text: 'Error: ' + data.error });
      } else {
        messages.push({
          role: 'bot',
          text: 'Failed to connect to mentor API. Ensure server is running on this host (port 5002).'
        });
        if (lastError && window.console) {
          console.error('Mentor API error:', lastError);
        }
      }
    } catch (err) {
      hideTyping();
      messages.push({ role: 'bot', text: 'Failed to connect to mentor. Please check if the server is running.' });
    }

    render(messages);
  }

  sendBtn.addEventListener('click', sendMessage);
  inputEl.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

  inputEl.addEventListener('input', function () {
    inputEl.style.height = 'auto';
    inputEl.style.height = Math.min(inputEl.scrollHeight, 140) + 'px';
  });

  if (promptWrap) {
    promptWrap.addEventListener('click', function (e) {
      var t = e.target;
      if (t && t.classList.contains('prompt-chip')) {
        inputEl.value = t.getAttribute('data-prompt') || '';
        inputEl.focus();
      }
    });
  }

  closeBtn.addEventListener('click', function () {
    var app = document.getElementById('app');
    if (app) {
      app.style.display = 'none';
    }
  });

  inputEl.focus();
})();
