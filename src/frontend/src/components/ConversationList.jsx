import React from 'react';
import { MessageSquare, Sparkles, Plus } from 'lucide-react';
import { formatDate } from '../utils/helpers';

const ConversationList = ({ conversations, activeId, onSelect, isCollapsed, onNewConversation }) => {
  return (
    <div className={`bg-gray-900 border-r border-gray-800 flex flex-col h-screen transition-all duration-300 ${
      isCollapsed ? 'w-0 opacity-0 overflow-hidden' : 'w-80 opacity-100'
    }`}>
      <div className="p-4 border-b border-gray-800">
        <div className="flex items-center gap-2 mb-4">
          <Sparkles className="w-6 h-6 text-emerald-500" />
          <h2 className="text-xl font-bold text-white">RecruitAI</h2>
        </div>
        <div className="text-sm text-gray-400 mb-3">HR Panel</div>
        
        {activeId && (
          <button
            onClick={onNewConversation}
            className="w-full flex items-center justify-center gap-2 bg-emerald-500/20 hover:bg-emerald-500/30 border border-emerald-500/50 text-emerald-500 py-2 px-4 rounded-lg transition-all duration-200 hover:scale-105"
          >
            <Plus className="w-4 h-4" />
            <span className="font-medium">New Conversation</span>
          </button>
        )}
      </div>
      
      <div className="flex-1 overflow-y-auto">
        {conversations.length === 0 ? (
          <div className="p-6 text-center">
            <MessageSquare className="w-12 h-12 text-gray-700 mx-auto mb-3" />
            <p className="text-gray-500 text-sm">No conversations yet</p>
            <p className="text-gray-600 text-xs mt-1">Start typing to begin</p>
          </div>
        ) : (
          conversations.map((conv) => (
            <button
              key={conv.id}
              onClick={() => onSelect(conv.id)}
              className={`w-full text-left p-4 border-b border-gray-800 transition-all duration-200 ${
                activeId === conv.id 
                  ? 'bg-emerald-500/10 border-l-2 border-l-emerald-500' 
                  : 'hover:bg-gray-800/50'
              }`}
            >
              <div className="flex items-center gap-3">
                <div className={`p-2 rounded-lg ${activeId === conv.id ? 'bg-emerald-500/20' : 'bg-gray-800'}`}>
                  <MessageSquare className={`w-4 h-4 ${activeId === conv.id ? 'text-emerald-500' : 'text-gray-400'}`} />
                </div>
                <div className="flex-1 min-w-0">
                  <p className={`font-medium ${activeId === conv.id ? 'text-emerald-500' : 'text-gray-300'}`}>
                    Conversation #{conv.id}
                  </p>
                  <p className="text-gray-500 text-xs truncate">
                    {formatDate(conv.updated_at)}
                  </p>
                </div>
              </div>
            </button>
          ))
        )}
      </div>
    </div>
  );
};

export default ConversationList;