import { useAuth } from "../context/AuthContext";

export function useRoleCheck() {
    const { user } = useAuth();
    
    const hasRole = (requiredRoles: string[]): boolean => {
        return user?.user_role ? requiredRoles.includes(user.user_role) : false;
    };
    
    return { hasRole };
}