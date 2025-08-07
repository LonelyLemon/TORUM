import { useState, type FormEvent } from "react";
import { useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext";
import { login, getUser } from "../services/api";

const Login: React.FC = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const { login: authLogin } = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (e: FormEvent) => {
        e.preventDefault();
        setError('');
        try {
            const data = await login({ email, password });
            authLogin(data.access_token, data.refresh_token, { 
                user_id: '', 
                email, 
                username: '',
                user_role: 'user', 
            });
            const userData = await getUser();
            authLogin(data.access_token, data.refresh_token, { 
                user_id: userData.user_id, 
                email: userData.email, 
                username: userData.username,
                user_role: userData.user_role, 
            });
            navigate('/');
        } catch (err) {
            setError('Invalid email or password !');
        }
    }

    return (
        <div className="max-w-md mx-auto mt-10 p-6 bg-white rounded-lg shadow">
            <h2 className="text-2xl font-bold text-center mb-4">Login</h2>
            {error && <p className="text-red-500 mb-4">{error}</p>}
            <form onSubmit={handleSubmit}>
                <div className="mb-4">
                <label className="block mb-1">Email</label>
                <input
                    type="email"
                    value={email}    
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="Enter email"
                    className="w-full p-2 border rounded"
                />
                </div>
                <div className="mb-4">
                    <label className="block mb-1">Password</label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="Enter your password"
                        className="w-full p-2 border rounded"
                    />
                </div>
                <div>
                    <button type="submit" className="w-full bg-blue-600 text-white p-2 rounded hover:bg-blue-700">
                        Login
                    </button>
                </div>
            </form>
        </div>
    );
};

export default Login