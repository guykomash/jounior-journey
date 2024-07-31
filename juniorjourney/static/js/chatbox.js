document.addEventListener('DOMContentLoaded', (event) => {
  const chatHeader = document.getElementById('chat-header');
  const chatContent = document.getElementById('chat-content');
  const chatToggleButton = document.getElementById('chat-toggle-button');

  chatHeader.addEventListener('click', () => {
    if (
      chatContent.style.display === 'none' ||
      chatContent.style.display === ''
    ) {
      chatContent.style.display = 'block';
      chatHeader.title = 'Close Chat';
      // chatToggleButton.textContent = 'Collapse';
    } else {
      chatContent.style.display = 'none';
      //   chatToggleButton.textContent = 'Open';
      chatHeader.title = 'Open Chat';
    }
  });

  const sendButton = document.getElementById('send-button');
  const chatInput = document.getElementById('chat-input');
  const chatMessages = document.getElementById('chat-messages');

  sendButton.addEventListener('click', () => {
    const message = chatInput.value;
    if (message.trim() !== '') {
      const messageElement = document.createElement('div');
      messageElement.textContent = message;
      chatMessages.appendChild(messageElement);
      chatInput.value = '';
      chatMessages.scrollTop = chatMessages.scrollHeight;
    }
  });
});
