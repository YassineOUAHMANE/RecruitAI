import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Loader2 } from 'lucide-react';
import ConversationList from '../components/ConversationList';
import ChatPanel from '../components/ChatPanel';
import { getAllConversations, createConversation } from '../services/api';

const HRPanel = () => {
  const [conversations, setConversations] = useState([]);
  const [activeConversation, setActiveConversation] = useState(null);
  const [loading, setLoading] = useState(true);
  const [pdfViewOpen, setPdfViewOpen] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    loadConversations();
    
    const hash = location.hash;
    if (hash.startsWith('#')) {
      const id = parseInt(hash.substring(1));
      if (!isNaN(id)) {
        setActiveConversation(id);
      }
    }
  }, [location.hash]);

  const loadConversations = async () => {
    try {
      const data = await getAllConversations();
      setConversations(data);
    } catch (error) {
      console.error('Failed to load conversations:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectConversation = (id) => {
    setActiveConversation(id);
    navigate(`#${id}`);
  };

  const handleNewConversation = () => {
    setActiveConversation(null);
    navigate('#');
  };

  const handleCreateConversation = async (firstMessage) => {
    try {
      const data = await createConversation(firstMessage);
      if (data && data.id) {
        await loadConversations();
        setActiveConversation(data.id);
        navigate(`#${data.id}`);
        return data;
      }
    } catch (error) {
      console.error('Failed to create conversation:', error);
      throw error;
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <Loader2 className="w-8 h-8 animate-spin text-emerald-500" />
      </div>
    );
  }

  return (
    <div className="flex h-screen bg-black overflow-hidden">
      <ConversationList
        conversations={conversations}
        activeId={activeConversation}
        onSelect={handleSelectConversation}
        onNewConversation={handleNewConversation}
        isCollapsed={pdfViewOpen}
      />
      <ChatPanel 
        conversationId={activeConversation}
        onConversationUpdate={loadConversations}
        onCreateConversation={handleCreateConversation}
        onPdfViewChange={setPdfViewOpen}
      />
    </div>
  );
};

export default HRPanel;