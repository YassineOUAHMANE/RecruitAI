// src/components/Message.jsx
import React from 'react';
import { FileText, Bot, User } from 'lucide-react';
import { formatDate } from '../utils/helpers';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';

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
          {isAI ? (
            <div className="markdown-content text-gray-200">
              <ReactMarkdown
                remarkPlugins={[remarkGfm]}
                components={{
                  // Headings
                  h1: ({node, ...props}) => <h1 className="text-2xl font-bold text-emerald-500 mb-3 mt-4" {...props} />,
                  h2: ({node, ...props}) => <h2 className="text-xl font-bold text-emerald-400 mb-2 mt-3" {...props} />,
                  h3: ({node, ...props}) => <h3 className="text-lg font-semibold text-emerald-400 mb-2 mt-2" {...props} />,
                  
                  // Paragraphs
                  p: ({node, ...props}) => <p className="mb-3 leading-relaxed" {...props} />,
                  
                  // Lists
                  ul: ({node, ...props}) => <ul className="list-disc list-inside mb-3 space-y-1 ml-2" {...props} />,
                  ol: ({node, ...props}) => <ol className="list-decimal list-inside mb-3 space-y-1 ml-2" {...props} />,
                  li: ({node, ...props}) => <li className="text-gray-200" {...props} />,
                  
                  // Links
                  a: ({node, ...props}) => (
                    <a 
                      className="text-emerald-500 hover:text-emerald-400 underline transition-colors" 
                      target="_blank" 
                      rel="noopener noreferrer" 
                      {...props} 
                    />
                  ),
                  
                  // Code blocks
                  code: ({node, inline, className, children, ...props}) => {
                    const match = /language-(\w+)/.exec(className || '');
                    return !inline && match ? (
                      <SyntaxHighlighter
                        style={vscDarkPlus}
                        language={match[1]}
                        PreTag="div"
                        className="rounded-lg my-3 text-sm"
                        {...props}
                      >
                        {String(children).replace(/\n$/, '')}
                      </SyntaxHighlighter>
                    ) : (
                      <code className="bg-black/50 text-emerald-400 px-1.5 py-0.5 rounded text-sm" {...props}>
                        {children}
                      </code>
                    );
                  },
                  
                  // Blockquotes
                  blockquote: ({node, ...props}) => (
                    <blockquote 
                      className="border-l-4 border-emerald-500 pl-4 italic text-gray-400 my-3" 
                      {...props} 
                    />
                  ),
                  
                  // Tables
                  table: ({node, ...props}) => (
                    <div className="overflow-x-auto my-3">
                      <table className="min-w-full border border-gray-700 rounded-lg" {...props} />
                    </div>
                  ),
                  thead: ({node, ...props}) => <thead className="bg-gray-800" {...props} />,
                  tbody: ({node, ...props}) => <tbody className="divide-y divide-gray-700" {...props} />,
                  tr: ({node, ...props}) => <tr className="hover:bg-gray-800/50 transition-colors" {...props} />,
                  th: ({node, ...props}) => <th className="px-4 py-2 text-left text-emerald-500 font-semibold" {...props} />,
                  td: ({node, ...props}) => <td className="px-4 py-2 text-gray-300" {...props} />,
                  
                  // Horizontal rule
                  hr: ({node, ...props}) => <hr className="border-gray-700 my-4" {...props} />,
                  
                  // Strong/Bold
                  strong: ({node, ...props}) => <strong className="font-bold text-white" {...props} />,
                  
                  // Emphasis/Italic
                  em: ({node, ...props}) => <em className="italic text-gray-300" {...props} />,
                }}
              >
                {message.text}
              </ReactMarkdown>
            </div>
          ) : (
            <p className="text-gray-200 whitespace-pre-wrap leading-relaxed">{message.text}</p>
          )}
          
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