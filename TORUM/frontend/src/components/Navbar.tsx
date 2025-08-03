import { Link, useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext";


const Navbar: React.FC = () => {
    const { user, logout } = useAuth();
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate("/login");
    }

    return (
        <nav className="bg-blue-600 text-white p-4">
            <div className="container mx-auto flex justify-between items-center">
                <Link to="/" className="text-xl font-bold">
                    Welcome to TORUM
                </Link>
                <div className="space-x-4">
                    { user ? (
                        <>
                            <Link to="/upload-document" className="bg-lime-500 text-white px-4 py-2 rounded hover:text-gray-200">
                                Upload Documents
                            </Link>
                            <Link to="/view-document" className="bg-lime-500 text-white px-4 py-2 rounded hover:text-gray-200">
                                Documents
                            </Link>
                            <Link to="/post" className="bg-lime-500 text-white px-4 py-2 rounded hover:text-gray-200">
                                Your Post
                            </Link>
                            <Link to="/account" className="bg-lime-500 text-white px-4 py-2 rounded hover:text-gray-200">
                                Your Account
                            </Link>
                            <button onClick={handleLogout} className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600">
                                Logout
                            </button>
                        </>
                    ) : (
                        <>
                            <Link to="/login" className="hover:text-gray-200">
                                Login
                            </Link>
                            <Link to="/signup" className="hover:text-gray-200">
                                Sign Up
                            </Link>
                        </>
                    )}
                </div>
            </div>
        </nav>
    );
};

export default Navbar;