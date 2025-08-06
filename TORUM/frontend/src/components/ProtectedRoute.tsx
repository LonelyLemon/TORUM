import { Navigate } from 'react-router-dom';
import type { ReactNode } from 'react';

import { useAuth } from '../context/AuthContext';
import { useRoleCheck } from '../utils/auth';


interface ProtectedRouteProps {
    children: ReactNode;
    requireRoles?: string[];
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children, requireRoles }) => {
    const { user } = useAuth();
    const { hasRole } = useRoleCheck();

    if (!user) {
        return <Navigate to="/login" />;
    }

    if (requireRoles && !hasRole(requireRoles)) {
        return <Navigate to="/unauthorized" />
    }
    
    return children;
};

export default ProtectedRoute;