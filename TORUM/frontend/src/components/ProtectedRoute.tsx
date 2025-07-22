import { Navigate } from 'react-router-dom';
import type { ReactNode } from 'react';

import { useAuth } from '../context/AuthContext';



interface ProtectedRouteProps {
    children: ReactNode;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
    const { user } = useAuth();
    return user ? children : <Navigate to="/login" />;
};

export default ProtectedRoute;