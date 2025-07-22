import axios from "axios";

import type { User, AuthResponse, LoginCredentials, SignupCredentials, Post, PostCreate, PostUpdate } from "../types/index";

const api = axios.create ({
    baseURL: "http://127.0.0.1:8000",
});

api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = 'Bearer ${token}';
    }
    return config;
});

export const login = async (credentials: LoginCredentials) => {
    const formData = new URLSearchParams();
    formData.append('email', credentials.email);
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

export const getPost = async (id: string) => {
  const response = await api.get<Post>(`/view-post/${id}`);
  return response.data;
};

export const updatePost = async (id: string, post: PostUpdate) => {
  const response = await api.put<{ message: string }>(`/update-post/${id}`, post);
  return response.data;
};

export const deletePost = async (id: string) => {
  const response = await api.delete<{ message: string }>(`/delete-post/${id}`);
  return response.data;
};