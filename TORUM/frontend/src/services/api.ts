import axios from "axios";

import type { User, UserUpdate, 
              AuthResponse, LoginCredentials, SignupCredentials, 
              Post, PostCreate, PostUpdate, 
              ReadingDocumentResponse, 
              Search
            } from "../types/index";

const api = axios.create ({
    baseURL: "http://127.0.0.1:8000",
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
              const response = await axios.post('http://127.0.0.1:8000/refresh', { refresh_token: refreshToken }, { headers: { 'Content-Type': 'application/json' } });
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

export const signup = async (credentials: SignupCredentials) => {
    const response = await api.post<User>('/register', credentials);
    return response.data;
};

export const createPost = async (post: PostCreate) => {
  const response = await api.post<Post>('/create-post', post);
  return response.data;
};

export const getMyPosts = async() => {
  const response = await api.get<Post[]>('/my-posts');
  return response.data;
}

export const updatePost = async (id: string, post: PostUpdate) => {
  const response = await api.put<{ message: string | undefined}>(`/update-post/${id}`, post);
  return response.data;
};

export const deletePost = async (id: string) => {
  const response = await api.delete<{ message: string }>(`/delete-post/${id}`);
  return response.data;
};

export const getUser = async () => {
  const response = await api.get<User>('/me');
  return response.data;
};

export const updateUser = async (update_data: UserUpdate): Promise<{ message: string | undefined}> => {
  const response = await api.put('/update-user', update_data);
  return response.data;
};

export const uploadReadingDocument = async (docs_title: string, docs_description: string, docs_tags: string, file: File): Promise<ReadingDocumentResponse> => {
  const formData = new FormData();
  formData.append("docs_title", docs_title);
  formData.append("docs_description", docs_description);
  formData.append("docs_tags", docs_tags || "Documents");
  formData.append("file", file);

  const response = await api.post<ReadingDocumentResponse>('/upload-reading-documents', formData, {headers: {"Content-Type": "multipart/form-data"}});
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

export const search = async (query: string): Promise<Search> => {
  const response = await api.get('/search', {params: {query}});
  return response.data;
}