import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, Loader2, Sparkles } from 'lucide-react';
import { uploadCV } from '../services/api';

const CandidateUpload = () => {
  const [uploadStatus, setUploadStatus] = useState(null);
  const [uploading, setUploading] = useState(false);

  const onDrop = async (acceptedFiles) => {
    if (acceptedFiles.length === 0) return;
    
    setUploading(true);
    const file = acceptedFiles[0];

    try {
      const success = await uploadCV(file);
      setUploadStatus(success ? 'success' : 'error');
    } catch (error) {
      setUploadStatus('error');
    } finally {
      setUploading(false);
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/msword': ['.doc'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx']
    },
    maxFiles: 1,
    disabled: uploading
  });

  return (
    <div className="min-h-screen bg-black flex items-center justify-center p-4 relative overflow-hidden">
      {/* Animated background */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute w-96 h-96 bg-emerald-500/10 rounded-full blur-3xl -top-48 -left-48 animate-pulse"></div>
        <div className="absolute w-96 h-96 bg-emerald-500/10 rounded-full blur-3xl -bottom-48 -right-48 animate-pulse" style={{ animationDelay: '1s' }}></div>
      </div>

      <div className="max-w-2xl w-full relative z-10">
        <div className="text-center mb-8 animate-fade-in">
          <div className="flex items-center justify-center gap-2 mb-4">
            <Sparkles className="w-10 h-10 text-emerald-500 animate-pulse" />
            <h1 className="text-5xl font-bold text-white">RecruitAI</h1>
          </div>
          <p className="text-gray-400 text-lg">Upload your CV to join our talent pool</p>
        </div>

        {uploadStatus === 'success' ? (
          <div className="bg-gray-900/50 backdrop-blur-sm rounded-2xl p-8 text-center border border-emerald-500/50 shadow-lg shadow-emerald-500/20 animate-slide-up">
            <div className="w-20 h-20 bg-emerald-500/20 rounded-full flex items-center justify-center mx-auto mb-4 animate-scale-in">
              <svg className="w-10 h-10 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <h2 className="text-3xl font-semibold text-white mb-2">CV Uploaded Successfully!</h2>
            <p className="text-gray-400 mb-6">Your CV has been saved and will be processed by our AI as soon as possible.</p>
            <button 
              onClick={() => setUploadStatus(null)}
              className="px-8 py-3 bg-emerald-500 hover:bg-emerald-600 text-black font-semibold rounded-lg transition-all duration-300 shadow-lg shadow-emerald-500/50 hover:shadow-emerald-500/70 hover:scale-105"
            >
              Upload Another CV
            </button>
          </div>
        ) : (
          <div
            {...getRootProps()}
            className={`bg-gray-900/30 backdrop-blur-sm border-2 border-dashed rounded-2xl p-12 text-center cursor-pointer transition-all duration-300 animate-slide-up ${
              isDragActive 
                ? 'border-emerald-500 bg-emerald-500/10 shadow-lg shadow-emerald-500/30 scale-105' 
                : 'border-gray-700 hover:border-emerald-500/50 hover:bg-gray-900/50'
            } ${uploading ? 'opacity-50 cursor-not-allowed' : ''}`}
          >
            <input {...getInputProps()} />
            <Upload className={`w-16 h-16 mx-auto mb-4 transition-all duration-300 ${isDragActive ? 'text-emerald-500 scale-110' : 'text-gray-500'}`} />
            {uploading ? (
              <>
                <Loader2 className="w-10 h-10 animate-spin text-emerald-500 mx-auto mb-2" />
                <p className="text-gray-300 text-lg">Uploading your CV...</p>
              </>
            ) : (
              <>
                <p className="text-gray-300 text-xl mb-2 font-medium">
                  {isDragActive ? 'Drop your CV here' : 'Drag & drop your CV here'}
                </p>
                <p className="text-gray-500 mb-4">or click to browse</p>
                <div className="inline-block px-4 py-2 bg-gray-800/50 rounded-lg border border-gray-700">
                  <p className="text-gray-400 text-sm">Supported formats: PDF, DOC, DOCX</p>
                </div>
              </>
            )}
          </div>
        )}

        {uploadStatus === 'error' && (
          <div className="mt-4 bg-red-900/20 border border-red-500/50 rounded-lg p-4 text-center backdrop-blur-sm animate-slide-up">
            <p className="text-red-400">Upload failed. Please try again.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default CandidateUpload;