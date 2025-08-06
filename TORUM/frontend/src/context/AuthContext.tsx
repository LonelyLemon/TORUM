import { createContext, useContext, useState, type ReactNode } from 'react';
import { type User } from '../types';

interface AuthContextType {
    user: User | null;
    accessToken: string | null;
    refreshToken: string | null;
    login: (accessToken: string, refreshToken: string, user: User) => void;
    logout: () => Promise<void>;
    refreshAccessToken: () => Promise<void>;
    error: string | null;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
    const [user, setUser] = useState<User | null>(() => {
        const storedUser = localStorage.getItem('user');
        return storedUser ? JSON.parse(storedUser) : null;
    });
    
    const [accessToken, setAccessToken] = useState<string | null>(() => {
        return localStorage.getItem('access_token');
    });

    const [refreshToken, setRefreshToken] = useState<string | null>(() => {
        return localStorage.getItem('refresh_token')
    });

    const [error, setError] = useState<string | null>(null);

    const login = (accessToken: string, refreshToken: string, user: User) => {
        setAccessToken(accessToken);
        setRefreshToken(refreshToken);
        setUser(user);
        setError(null);
        localStorage.setItem('access_token', accessToken);
        localStorage.setItem('refresh_token', refreshToken);
        localStorage.setItem('user', JSON.stringify(user));
    };

    const logout = async () => {
        try {
            if (refreshToken) {
                await fetch('/logout', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        Authorization: `Bearer ${accessToken}`,
                    },
                    body: JSON.stringify({ refresh_token: refreshToken }),
                });
            }
        } catch (err) {
            console.error('Logout failed:', err);
        } finally {
            setAccessToken(null);
            setRefreshToken(null);
            setUser(null);
            setError(null);
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            localStorage.removeItem('user');
        }
    };

    const refreshAccessToken = async () => {
        if (!refreshToken) {
            setError('No refresh token available !');
            await logout();
            return;
        }
        try {
            const response = await fetch('/refresh', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ refresh_token: refreshToken }),
            });
            if (!response.ok) {
                throw new Error('Failed to refresh token');
            }
            const data: { access_token: string; token_type: string } = await response.json();
            setAccessToken(data.access_token);
            setError(null);
            localStorage.setItem('access_token', data.access_token);
        } catch (err) {
            setError('Session expired. Please log in again.');
            await logout();
        }
    };

    return (
        <AuthContext.Provider value={{ user, accessToken, refreshToken, login, logout, refreshAccessToken, error }}>
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
}