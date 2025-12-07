import React from 'react';
import { FileText, Bot, User } from 'lucide-react';
import { formatDate } from '../utils/helpers';

const Message = ({ message, onFileClick, index }) => {
  const isAI = message.sent_by_AI === 1;
  
  return (
    <div 
      className={`flex gap-3 mb-6 animate-slide-up`}
      style={{ animationDelay: `${index * 0.05}s` }}
    >
      {/* Avatar */}
      <div className={`w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0 ${
        isAI ? 'bg-emerald-500/20' : 'bg-gray-800'
      }`}>
        {isAI ? (
          <Bot className="w-5 h-5 text-emerald-500" />
        ) : (
          <User className="w-5 h-5 text-gray-400" />
        )}
      </div>

      {/* Message Content */}
      <div className="flex-1 max-w-3xl">
        <div className={`rounded-lg p-4 ${
          isAI ? 'bg-gray-900 border border-gray-800' : 'bg-gray-800/50'
        }`}>
          <p className="text-gray-200 whitespace-pre-wrap leading-relaxed">{message.text}</p>
          
          {message.file_ids && message.file_ids.length > 0 && (
            <div className="mt-3 space-y-2">
              {message.file_ids.map((fileId) => (
                <button
                  key={fileId}
                  onClick={() => onFileClick(fileId)}
                  className="w-full flex items-center gap-3 bg-black/50 hover:bg-emerald-500/10 border border-gray-700 hover:border-emerald-500/50 text-gray-300 hover:text-emerald-500 py-3 px-4 rounded-lg transition-all duration-200 group"
                >
                  <FileText className="w-5 h-5 group-hover:scale-110 transition-transform" />
                  <span className="font-medium">CV Document #{fileId}</span>
                  <svg className="w-4 h-4 ml-auto transform group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </button>
              ))}
            </div>
          )}
        </div>
        <p className="text-gray-600 text-xs mt-2 ml-1">{formatDate(message.sent_at)}</p>
      </div>
    </div>
  );
};

export default Message;