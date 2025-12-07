import React, { useState, useEffect, useRef } from 'react';
import { Loader2, MessageSquare, Sparkles } from 'lucide-react';
import Message from './Message';
import ChatInput from './ChatInput';
import PDFViewer from './PDFViewer';
import { getConversation, sendMessage } from '../services/api';

const ChatPanel = ({ conversationId, onConversationUpdate, onCreateConversation, onPdfViewChange }) => {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [pdfContent, setPdfContent] = useState(null);
  const [hasMore, setHasMore] = useState(true);
  const [loadingMore, setLoadingMore] = useState(false);
  const messagesEndRef = useRef(null);
  const chatContainerRef = useRef(null);
  const lastScrollTop = useRef(0);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const loadConversation = async (offset = 0, prepend = false) => {
    if (!conversationId) return;
    
    if (prepend) setLoadingMore(true);
    else setLoading(true);
    
    try {
      const data = await getConversation(conversationId, offset);
      
      if (data && data.content) {
        const newMessages = data.content.reverse();
        
        if (prepend) {
          setMessages(prev => [...newMessages, ...prev]);
          setHasMore(newMessages.length === 10);
        } else {
          setMessages(newMessages);
          setHasMore(newMessages.length === 10);
          setTimeout(scrollToBottom, 100);
        }
      }
    } catch (error) {
      console.error('Failed to load conversation:', error);
    } finally {
      setLoading(false);
      setLoadingMore(false);
    }
  };

  useEffect(() => {
    if (conversationId) {
      setMessages([]);
      setPdfContent(null);
      loadConversation();
    }
  }, [conversationId]);

  useEffect(() => {
    onPdfViewChange(!!pdfContent);
  }, [pdfContent, onPdfViewChange]);

  const handleScroll = () => {
    if (!chatContainerRef.current || loadingMore || !hasMore) return;
    
    const { scrollTop } = chatContainerRef.current;
    
    if (scrollTop < 100 && scrollTop < lastScrollTop.current) {
      const offset = messages.length;
      loadConversation(offset, true);
    }
    
    lastScrollTop.current = scrollTop;
  };

  const handleSend = async (text) => {
    if (!text.trim()) return;

    try {
      let currentConvId = conversationId;

      // Create new conversation if none is active
      if (!currentConvId) {
        const newConv = await onCreateConversation(text);
        if (!newConv || !newConv.id) return;
        
        currentConvId = newConv.id;
        
        // Add user message
        const userMsg = {
          id: Date.now(),
          text: text,
          sent_by_AI: 0,
          sent_at: new Date().toISOString(),
          file_ids: null
        };
        
        // Add AI response
        const aiMsg = {
          id: newConv.response.id,
          text: newConv.response.text,
          sent_by_AI: 1,
          sent_at: newConv.response.sent_at,
          file_ids: newConv.response.file_ids || null
        };
        
        setMessages([userMsg, aiMsg]);
        setTimeout(scrollToBottom, 100);
        return;
      }

      // Send message to existing conversation
      const data = await sendMessage(currentConvId, text);

      if (data) {
        const userMsg = {
          id: Date.now(),
          text: text,
          sent_by_AI: 0,
          sent_at: new Date().toISOString(),
          file_ids: null
        };
        
        setMessages(prev => [...prev, userMsg, data]);
        setTimeout(scrollToBottom, 100);
        
        if (onConversationUpdate) {
          onConversationUpdate();
        }
      }
    } catch (error) {
      console.error('Failed to send message:', error);
    }
  };

  const handleFileClick = (fileId) => {
    setPdfContent({ id: fileId });
  };

  if (!conversationId && !pdfContent) {
    return (
      <div className="flex-1 flex flex-col bg-black relative overflow-hidden">
        <div className="absolute inset-0">
          <div className="absolute w-96 h-96 bg-emerald-500/5 rounded-full blur-3xl top-1/4 left-1/4 animate-pulse"></div>
        </div>
        <div className="flex-1 flex items-center justify-center relative z-10">
          <div className="text-center animate-fade-in">
            <Sparkles className="w-20 h-20 text-emerald-500/50 mx-auto mb-6 animate-pulse" />
            <h3 className="text-2xl text-gray-300 mb-2 font-semibold">Welcome to RecruitAI</h3>
            <p className="text-gray-500">Start a conversation by typing a message below</p>
          </div>
        </div>
        <ChatInput onSend={handleSend} />
      </div>
    );
  }

  return (
    <div className="flex-1 flex">
      {/* Chat Panel */}
      <div className={`flex flex-col bg-black transition-all duration-300 ${
        pdfContent ? 'w-1/2' : 'w-full'
      }`}>
        <div className="p-4 bg-gray-900 border-b border-gray-800">
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></div>
            <h3 className="text-white font-semibold">Conversation #{conversationId}</h3>
          </div>
        </div>

        <div 
          ref={chatContainerRef}
          onScroll={handleScroll}
          className="flex-1 overflow-y-auto p-4 bg-black"
        >
          {loadingMore && (
            <div className="text-center mb-4 animate-fade-in">
              <Loader2 className="w-6 h-6 animate-spin text-emerald-500 mx-auto" />
            </div>
          )}
          
          {loading ? (
            <div className="flex items-center justify-center h-full">
              <Loader2 className="w-8 h-8 animate-spin text-emerald-500" />
            </div>
          ) : (
            <>
              {messages.map((msg, index) => (
                <Message key={msg.id} message={msg} onFileClick={handleFileClick} index={index} />
              ))}
              <div ref={messagesEndRef} />
            </>
          )}
        </div>

        <ChatInput onSend={handleSend} />
      </div>

      {/* PDF Viewer Panel */}
      {pdfContent && (
        <PDFViewer fileId={pdfContent.id} onClose={() => setPdfContent(null)} />
      )}
    </div>
  );
};

export default ChatPanel;