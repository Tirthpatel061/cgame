(function () {
  'use strict';
  // Resolve chatbot URL from current host so it works on other devices too.
  function getChatbotUrl() {
    if (window.MENTOR_CHATBOT_URL) return window.MENTOR_CHATBOT_URL;

    var path = '/Home%20Page/chatbot.html';
    var origin = window.location && window.location.origin;
    if (origin && origin !== 'null') {
      return origin + path;
    }
    return './Home Page/chatbot.html';
  }
  var chatOverlay = null;
  var iframe = null;

  function openChatbot() {
    // If overlay already exists, just show it
    if (chatOverlay) {
      chatOverlay.classList.add('active');
      return;
    }

    // Create overlay container
    chatOverlay = document.createElement('div');
    chatOverlay.id = 'mentor-chat-overlay';
    chatOverlay.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0, 0, 0, 0.7);
      z-index: 99999;
      display: flex;
      justify-content: center;
      align-items: center;
      animation: mentorOverlayFadeIn 0.3s ease;
    `;

    // Create iframe container
    var iframeContainer = document.createElement('div');
    iframeContainer.style.cssText = `
      width: 420px;
      height: 600px;
      max-width: 95vw;
      max-height: 90vh;
      border-radius: 16px;
      overflow: hidden;
      box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5);
      animation: mentorSlideUp 0.3s ease;
      background: #0b1220;
    `;

    // Create iframe
    iframe = document.createElement('iframe');
    iframe.src = getChatbotUrl();
    iframe.style.cssText = `
      width: 100%;
      height: 100%;
      border: none;
      background: #0b1220;
    `;

    // Create close button
    var closeBtn = document.createElement('button');
    closeBtn.innerHTML = '✕';
    closeBtn.style.cssText = `
      position: absolute;
      top: 20px;
      right: 20px;
      width: 36px;
      height: 36px;
      border: none;
      background: rgba(255, 255, 255, 0.1);
      color: white;
      border-radius: 50%;
      font-size: 18px;
      cursor: pointer;
      z-index: 100000;
      transition: all 0.2s ease;
    `;
    closeBtn.addEventListener('mouseenter', function() {
      closeBtn.style.background = '#ef4444';
    });
    closeBtn.addEventListener('mouseleave', function() {
      closeBtn.style.background = 'rgba(255, 255, 255, 0.1)';
    });
    closeBtn.addEventListener('click', closeChatbot);

    // Add animations
    var style = document.createElement('style');
    style.textContent = `
      @keyframes mentorOverlayFadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
      }
      @keyframes mentorSlideUp {
        from { transform: translateY(30px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
      }
    `;
    document.head.appendChild(style);

    // Assemble
    iframeContainer.appendChild(iframe);
    chatOverlay.appendChild(closeBtn);
    chatOverlay.appendChild(iframeContainer);
    document.body.appendChild(chatOverlay);

    // Close on overlay click
    chatOverlay.addEventListener('click', function(e) {
      if (e.target === chatOverlay) {
        closeChatbot();
      }
    });

    // Close on escape
    document.addEventListener('keydown', handleEscape);
  }

  function closeChatbot() {
    if (chatOverlay) {
      chatOverlay.classList.remove('active');
      chatOverlay.style.display = 'none';
    }
  }

  function handleEscape(e) {
    if (e.key === 'Escape' && chatOverlay) {
      closeChatbot();
    }
  }

  function styleInjectedButton(btn) {
    btn.style.position = 'fixed';
    btn.style.right = '20px';
    btn.style.bottom = '20px';
    btn.style.zIndex = '99998';
    btn.style.border = 'none';
    btn.style.borderRadius = '999px';
    btn.style.padding = '12px 18px';
    btn.style.fontWeight = '700';
    btn.style.cursor = 'pointer';
    btn.style.background = 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)';
    btn.style.color = '#ffffff';
    btn.style.boxShadow = '0 10px 24px rgba(59, 130, 246, 0.4)';
    btn.style.fontFamily = 'Segoe UI, Inter, system-ui, sans-serif';
    btn.style.fontSize = '14px';
    btn.style.display = 'flex';
    btn.style.alignItems = 'center';
    btn.style.gap = '8px';
    btn.style.transition = 'all 0.2s ease';
  }

  function wireMentorButton() {
    var btn = document.getElementById('mentorButton');

    if (!btn) {
      btn = document.createElement('button');
      btn.id = 'mentorButton';
      btn.type = 'button';
      btn.innerHTML = '<span style="font-size: 18px;">🤖</span><span>Mentor</span>';
      styleInjectedButton(btn);
      document.body.appendChild(btn);
    }

    // Add hover effects
    btn.addEventListener('mouseenter', function() {
      btn.style.transform = 'translateY(-3px)';
      btn.style.boxShadow = '0 14px 28px rgba(59, 130, 246, 0.5)';
    });

    btn.addEventListener('mouseleave', function() {
      btn.style.transform = 'translateY(0)';
      btn.style.boxShadow = '0 10px 24px rgba(59, 130, 246, 0.4)';
    });

    btn.onclick = function (e) {
      if (e) e.preventDefault();
      openChatbot();
      return false;
    };
  }

  window.openSharedMentorChatbot = openChatbot;

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', wireMentorButton);
  } else {
    wireMentorButton();
  }
})();


