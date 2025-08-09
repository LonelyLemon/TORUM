import axios from "axios";

import type { User, UserUpdate, 
              AuthResponse, LoginCredentials, SignupCredentials, 
              Post, PostCreate, PostUpdate, 
              ReadingDocumentResponse, 
              Search
            } from "../types/index";

export const api = axios.create ({
    baseURL: import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000",
});

api.interceptors.request.use(async (config) => {
    let token = localStorage.getItem('access_token');
    if (token) {
        console.log('Token:', token);
        console.log('Authorization Header:', `Bearer ${token}`);
        config.headers["Authorization"] = `Bearer ${token}`;
        try {
          const payload = JSON.parse(atob(token.split('.')[1]));
          const expiry = payload.exp * 1000;
          if (Date.now() >= expiry) {
            const refreshToken = localStorage.getItem('refresh_token');
            if (refreshToken) {
              const response = await axios.post(`${import.meta.env.VITE_API_BASE_URL}/refresh`, { refresh_token: refreshToken }, { headers: { 'Content-Type': 'application/json' } });
              token = response.data.access_token;
              localStorage.setItem('access_token', response.data.access_token);
            } else {
              throw new Error('No refresh token available');
            }
          }
        } catch (error) {
          console.error('Token refresh error:', error);
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          localStorage.removeItem('user');
          window.location.href = '/login';
        }
    }
    return config;
});

export const login = async (credentials: LoginCredentials) => {
    const formData = new URLSearchParams();
    formData.append('username', credentials.email);
    formData.append('password', credentials.password);
    const response = await api.post<AuthResponse>('/login', formData, {
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
    })
    return response.data;
};

export const signup = async (credentials: SignupCredentials): Promise<User> => {
    const response = await api.post('/register', credentials);
    return response.data;
};

export const createPost = async (post: PostCreate): Promise<Post> => {
  const response = await api.post('/create-post', post);
  return response.data;
};

export const getMyPosts = async(): Promise<Post[]> => {
  const response = await api.get('/my-posts');
  return response.data;
}

export const getPostById = async(id: string): Promise<Post> => {
  const response = await api.get(`/view-post/${id}`);
  return response.data;
}

export const updatePost = async (id: string, post: PostUpdate): Promise<{ message: string | undefined}> => {
  const response = await api.put(`/update-post/${id}`, post);
  return response.data;
};

export const deletePost = async (id: string): Promise<{ message: string }> => {
  const response = await api.delete(`/delete-post/${id}`);
  return response.data;
};

export const getUser = async (): Promise<User> => {
  const response = await api.get('/me');
  return response.data;
};

export const getAllUsers = async (): Promise<User[]> => {
    const response = await api.get('/users');
    return response.data;
};

export const updateUser = async (update_data: UserUpdate): Promise<{ message: string | undefined}> => {
  const response = await api.put('/update-user', update_data);
  return response.data;
};

export const updateUserRole = async (user_id: string, new_role: string): Promise<{ message: string | undefined }> => {
  const response = await api.put(`/update-user-role/${user_id}?new_role=${new_role}`);
  return response.data;
}

export const uploadReadingDocument = async (title: string, description: string, tags: string, file: File): Promise<ReadingDocumentResponse> => {
  const formData = new FormData();
  formData.append("docs_title", title);
  formData.append("docs_description", description);
  formData.append("docs_tags", tags);
  formData.append("file", file);

  const response = await api.post('/upload-reading-documents', formData);
  return response.data;
}

export const getMyDocuments = async (): Promise<ReadingDocumentResponse[]> => {
  const response = await api.get('/my-reading-documents');
  return response.data;
}

export const downloadDocument = async (docId: string): Promise<{ url: string }> => {
  const response = await api.get(`/download-document/${docId}`);
  return response.data;
};

export const deleteDocument = async (docId: string): Promise<{ message: string }> => {
  const response = await api.delete(`/delete-reading-document/${docId}`);
  return response.data; 
}

export const search = async (query: string): Promise<Search> => {
  const response = await api.get('/search', {params: {query: query.trim()}});
  return response.data;
}