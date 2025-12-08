const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export const uploadCV = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await fetch(`${API_BASE}/upload`, {
    method: 'POST',
    body: formData,
  });
  
  const data = await response.json();
  return data.message === 'success';
};

export const getAllConversations = async () => {
  const response = await fetch(`${API_BASE}/conversation/`);
  const data = await response.json();
  return data.message && Array.isArray(data.message) ? data.message : [];
};

export const getConversation = async (id, offset = null) => {
  const url = offset !== null 
    ? `${API_BASE}/conversation/${id}?offset=${offset}`
    : `${API_BASE}/conversation/${id}`;
  
  const response = await fetch(url);
  const data = await response.json();
  return data.message;
};

export const sendMessage = async (conversationId, text) => {
  const response = await fetch(`${API_BASE}/conversation/${conversationId}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text }),
  });
  
  const data = await response.json();
  return data.message;
};

export const createConversation = async (text) => {
  const response = await fetch(`${API_BASE}/conversation/`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text }),
  });
  
  const data = await response.json();
  return data.message;
};

export const getFile = async (fileId) => {
  const response = await fetch(`${API_BASE}/files/${fileId}`);
  const blob = await response.blob();
  return URL.createObjectURL(blob);
};