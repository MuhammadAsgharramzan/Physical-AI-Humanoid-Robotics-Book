import React, { useState, useRef, useEffect, useCallback, useMemo } from 'react';
import './RAGChatbot.css';

const RAGChatbot = () => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedText, setSelectedText] = useState('');
  const messagesEndRef = useRef(null);

  // Function to scroll to bottom of messages
  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, scrollToBottom]);

  // Function to get selected text from the page
  const getSelectedText = useCallback(() => {
    const selectedText = window.getSelection().toString().trim();
    if (selectedText) {
      setSelectedText(selectedText);
      // Optionally pre-fill the input with a question about the selected text
      setInputValue(`Can you explain more about: "${selectedText.substring(0, 50)}..."?`);
    }
  }, []);

  // Handle sending a message
  const handleSendMessage = useCallback(async () => {
    if (!inputValue.trim() || isLoading) return;

    // Add user message to chat
    const userMessage = { type: 'user', content: inputValue, timestamp: new Date() };
    setMessages(prev => [...prev, userMessage]);
    const currentInput = inputValue;
    const currentSelectedText = selectedText;
    setInputValue('');
    setIsLoading(true);

    try {
      // Try the real API first, fall back to mock if it fails
      let data;
      const endpoint = currentSelectedText ? '/api/selected-text-ask' : '/api/ask';

      try {
        const response = await fetch('http://localhost:8000' + endpoint, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            question: currentInput,
            selected_text: currentSelectedText || null,
          }),
        });

        if (!response.ok) {
          throw new Error(`API request failed with status ${response.status}`);
        }

        data = await response.json();
      } catch (apiError) {
        console.warn('Real API failed, using mock service:', apiError.message);

        // Import and use mock service
        const { mockAskQuestion, mockSelectedTextAsk } = await import('../../utils/mockRAGService');

        if (currentSelectedText) {
          data = await mockSelectedTextAsk(currentInput, currentSelectedText);
        } else {
          data = await mockAskQuestion(currentInput);
        }
      }

      // Add bot response to chat
      const botMessage = {
        type: 'bot',
        content: data.answer,
        sources: data.sources,
        confidence: data.confidence,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, botMessage]);
      // Clear selected text after use
      setSelectedText('');
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        type: 'bot',
        content: 'Sorry, I encountered an error processing your question. Please try again.',
        sources: [],
        confidence: 0,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  }, [inputValue, isLoading, selectedText]);

  // Handle key press (Enter to send)
  const handleKeyPress = useCallback((e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  }, [handleSendMessage]);

  // Function to copy message to clipboard
  const copyToClipboard = useCallback((text) => {
    navigator.clipboard.writeText(text);
  }, []);

  // Memoize message components to prevent unnecessary re-renders
  const MessageComponent = useMemo(() => {
    return messages.map((message, index) => (
      <div
        key={`${index}-${message.timestamp?.getTime() || index}`}
        className={`message ${message.type === 'user' ? 'user-message' : 'bot-message'}`}
      >
        <div className="message-content">
          <div className="message-text">
            {message.content}
          </div>

          {message.sources && message.sources.length > 0 && (
            <div className="message-sources">
              <strong>Sources:</strong>
              <ul>
                {message.sources.map((source, idx) => (
                  <li key={idx}>{source}</li>
                ))}
              </ul>
            </div>
          )}

          {message.confidence !== undefined && (
            <div className="message-confidence">
              Confidence: {(message.confidence * 100).toFixed(0)}%
            </div>
          )}

          <button
            className="copy-button"
            onClick={() => copyToClipboard(message.content)}
            title="Copy to clipboard"
          >
            📋
          </button>
        </div>
      </div>
    ));
  }, [messages, copyToClipboard]);

  return (
    <div className="rag-chatbot-container">
      <div className="rag-chatbot-header">
        <h3>Physical AI & Humanoid Robotics Assistant</h3>
        <p>Ask questions about the book content</p>
      </div>

      <div className="rag-chatbot-messages" onClick={getSelectedText}>
        {messages.length === 0 ? (
          <div className="welcome-message">
            <p>Hello! I'm your Physical AI & Humanoid Robotics book assistant.</p>
            <p>You can ask me questions about any topic covered in the book.</p>
            <p>Select text on the page and click here to ask specific questions about it!</p>
          </div>
        ) : (
          MessageComponent
        )}
        {isLoading && (
          <div className="message bot-message">
            <div className="message-content">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="rag-chatbot-input-area">
        {selectedText && (
          <div className="selected-text-preview">
            <strong>Selected text:</strong> "{selectedText.substring(0, 100)}{selectedText.length > 100 ? '...' : ''}"
            <button
              className="clear-selection"
              onClick={() => setSelectedText('')}
              title="Clear selection"
            >
              ×
            </button>
          </div>
        )}

        <div className="input-container">
          <textarea
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder={selectedText
              ? "Ask a question about the selected text..."
              : "Ask a question about the book content..."}
            rows="3"
            disabled={isLoading}
          />
          <button
            onClick={handleSendMessage}
            disabled={!inputValue.trim() || isLoading}
            className="send-button"
          >
            {isLoading ? 'Sending...' : 'Send'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default RAGChatbot;