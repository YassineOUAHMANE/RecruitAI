import React, { useState, useEffect } from 'react';
import { Loader2, X, FileText } from 'lucide-react';
import { getFile } from '../services/api';

const PDFViewer = ({ fileId, onClose }) => {
  const [fileUrl, setFileUrl] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    const loadFile = async () => {
      try {
        const url = await getFile(fileId);
        setFileUrl(url);
      } catch (err) {
        setError(true);
      } finally {
        setLoading(false);
      }
    };

    loadFile();

    return () => {
      if (fileUrl) {
        URL.revokeObjectURL(fileUrl);
      }
    };
  }, [fileId]);

  return (
    <div className="w-1/2 flex flex-col bg-gray-900 border-l border-gray-800 animate-slide-left">
      <div className="p-4 bg-black border-b border-gray-800 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-emerald-500/20 rounded-lg">
            <FileText className="w-5 h-5 text-emerald-500" />
          </div>
          <div>
            <h3 className="text-white font-semibold">CV Document</h3>
            <p className="text-gray-500 text-sm">File ID: {fileId}</p>
          </div>
        </div>
        <button
          onClick={onClose}
          className="p-2 hover:bg-gray-800 text-gray-400 hover:text-white rounded-lg transition-all duration-200 group"
        >
          <X className="w-5 h-5 group-hover:rotate-90 transition-transform duration-200" />
        </button>
      </div>
      
      {loading ? (
        <div className="flex-1 flex flex-col items-center justify-center bg-black">
          <Loader2 className="w-8 h-8 animate-spin text-emerald-500 mb-3" />
          <p className="text-gray-500">Loading document...</p>
        </div>
      ) : error ? (
        <div className="flex-1 flex flex-col items-center justify-center bg-black">
          <div className="p-4 bg-red-900/20 border border-red-500/50 rounded-lg">
            <p className="text-red-400">Failed to load document</p>
          </div>
        </div>
      ) : (
        <iframe
          src={fileUrl}
          className="flex-1 w-full bg-black"
          title={`CV Document ${fileId}`}
        />
      )}
    </div>
  );
};

export default PDFViewer;