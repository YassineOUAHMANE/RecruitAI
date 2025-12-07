import React, { useState } from 'react';
import { Send, Loader2 } from 'lucide-react';

const ChatInput = ({ onSend }) => {
  const [input, setInput] = useState('');
  const [sending, setSending] = useState(false);

  const handleSend = async () => {
    if (!input.trim() || sending) return;

    const message = input.trim();
    setInput('');
    setSending(true);

    try {
      await onSend(message);
    } finally {
      setSending(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="p-4 bg-gray-900 border-t border-gray-800">
      <div className="flex gap-3 items-end">
        <div className="flex-1 relative">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message... (Shift + Enter for new line)"
            className="w-full bg-black text-gray-200 px-4 py-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500/50 border border-gray-800 resize-none transition-all duration-200"
            rows="1"
            style={{
              minHeight: '48px',
              maxHeight: '120px',
              height: 'auto'
            }}
            onInput={(e) => {
              e.target.style.height = 'auto';
              e.target.style.height = e.target.scrollHeight + 'px';
            }}
            disabled={sending}
          />
        </div>
        <button
          onClick={handleSend}
          disabled={sending || !input.trim()}
          className="bg-emerald-500 hover:bg-emerald-600 disabled:bg-gray-800 disabled:text-gray-600 text-black p-3 rounded-lg transition-all duration-200 shadow-lg shadow-emerald-500/20 hover:shadow-emerald-500/40 hover:scale-105 disabled:shadow-none disabled:scale-100"
        >
          {sending ? (
            <Loader2 className="w-6 h-6 animate-spin" />
          ) : (
            <Send className="w-6 h-6" />
          )}
        </button>
      </div>
      <p className="text-gray-600 text-xs mt-2 ml-1">Press Enter to send, Shift + Enter for new line</p>
    </div>
  );
};

export default ChatInput;