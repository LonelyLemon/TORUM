import React, { useEffect, useState } from "react";

import { getUser, getAllUsers, updateUser, updateUserRole } from "../services/api";
import { type User } from "../types";
import { useAuth } from "../context/AuthContext";

const AccountManagement: React.FC = () => {
    const { user } = useAuth();
    const [currentUser, setCurrentUser] = useState<User | null>(null);
    const [allUsers, setAllUsers] = useState<User[]>([]);

    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");

    const [editingUsername, setEditingUsername] = useState(false);
    const [editingPassword, setEditingPassword] = useState(false);
    const [editUsername, setEditUsername] = useState("");
    const [newPassword, setNewPassword] = useState("");
    const [confirmNewPassword, setConfirmNewPassword] = useState("");
    const [selectedUserID, setSelectedUserID] = useState("");
    const [newRole, setNewRole] = useState("")

    useEffect(() => {
        const fetchUserData = async () => {
            try {
                const userData = await getUser();
                setCurrentUser(userData);
                setEditUsername(userData.username);
                
                if (user?.user_role === "admin") {
                    const users = await getAllUsers();
                    setAllUsers(users);
                }
            } catch (err: any) {
                setError(err.response?.data?.detail || "Failed to fetch user data!");
            }
        };
        fetchUserData();
    }, [user]);

    const handleUpdate = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");
        setSuccess("");

        if (editingPassword && newPassword !== confirmNewPassword) {
            setError("New password does not match !");
            return;
        }

        try {
            const payload: {username?: string, password?: string} = {};
            if (editingUsername && editUsername !== currentUser?.username) {
                payload.username = editUsername;
            }
            if (editingPassword && newPassword) {
                payload.password = newPassword;
            }

            if (Object.keys(payload).length === 0) {
                setError("No changes to update !")
                return;
            }

            await updateUser(payload);
            setSuccess("Account Updated Successfully !");
            setCurrentUser((prev) => prev ? { ...prev, ...payload} : prev);
            setEditingUsername(false);
            setEditingPassword(false);
            setNewPassword("");
            setConfirmNewPassword("");
        } catch (err: any) {
            setError(err.response?.data?.detail || "Failed to update account !")
        }
    };

    const handleRoleUpdate = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");
        setSuccess("");
        if (!selectedUserID || !newRole) {
            setError("Please select a user and a role!");
            return;
        }

        try {
            await updateUserRole(selectedUserID, newRole);
            setSuccess("User role updated successfully!");
            setAllUsers((prev) => 
                prev.map((u) => 
                    u.user_id === selectedUserID ? { ...u, user_role: newRole } : u
                ));
            setSelectedUserID("");
            setNewRole("");
        } catch (err: any) {
            setError(err.response?.data?.detail || "Failed to update user role!");
        }
    }

    return (
        <div className="max-w-md mx-auto mt-10 p-6 bg-white rounded-lg shadow">
            <h2 className="text-2xl font-bold text-center mb-4">Account Management</h2>
            {error && <p className="text-red-500 mb-4">{error}</p>}
            {success && <p className="text-green-500 mb-4">{success}</p>}
            <form onSubmit={handleUpdate}>
                <div className="mb-4">
                    <label className="block mb-1">User ID</label>
                    <input
                        type="text"
                        value={currentUser?.user_id || ""}
                        disabled
                        className="w-full p-2 border rounded bg-gray-100"
                    />
                </div>
                <div className="mb-4">
                    <label className="block mb-1">Email</label>
                    <input
                        type="email"
                        value={currentUser?.email || ""}
                        disabled
                        className="w-full p-2 border rounded bg-gray-100"
                    />
                </div>
                <div className="mb-4">
                    <label className="block mb-1">Username</label>
                    <div className="flex item-center gap-2">
                        <input
                            type="text"
                            value={editUsername}
                            disabled={!editingUsername}
                            onChange={(e) => setEditUsername(e.target.value)}
                            className={`w-full p-2 border rounded ${!editingUsername ? "bg-gray-100" : ""}`}
                        />
                        <button
                            type="button"
                            onClick={() => setEditingUsername(!editingUsername)}
                            className="text-blue-600 hover:underline"
                        >
                            {editingUsername ? "Cancel" : "Edit"}
                        </button>
                    </div>
                </div>
                <div className="mb-4">
                    <label className="block mb-1">Role</label>
                    <input 
                        type="text"
                        value={currentUser?.user_role || ""}
                        disabled
                        className="w-full p-2 border rounded"
                    />
                </div>
                <div className="mb-4">
                    <label className="block mb-1">Password</label>
                    {!editingPassword ? (
                        <div className="flex items-center justify-between">
                            <input 
                                type="password"
                                value={"********"}
                                disabled
                                className="w-full p-2 border rounded bg-gray-100"
                            />
                            <button
                                type="button"
                                onClick={() => setEditingPassword(true)}
                                className="text-blue-600 hover:underline ml-2"
                            >
                                Edit
                            </button>
                        </div>
                    ) : (
                        <>
                            <input 
                                type="password"
                                placeholder="New Password"
                                value={newPassword}
                                onChange={(e) => setNewPassword(e.target.value)}
                                className="w-full p-2 border rounded mb-2"
                            />
                            <input
                                type="password"
                                placeholder="Confirm New Password"
                                value={confirmNewPassword}
                                onChange={(e) => setConfirmNewPassword(e.target.value)}
                                className="w-full p-2 border rounded mb-2"
                            />
                            <button
                                type="button"
                                onClick={() => {
                                    setEditingPassword(false);
                                    setNewPassword("");
                                    setConfirmNewPassword("");
                                }}
                                className="text-red-500 hover:underline text-sm"
                            >
                                Cancel Password Change
                            </button>
                        </>
                    )}
                </div>
                <button 
                    type="submit" 
                    className="w-full bg-blue-600 text-white p-2 rounded hover:bg-blue-700"
                >
                    Save Changes
                </button>
            </form>

            {user?.user_role === "admin" && (
                <div className="mt-8">
                    <h3 className="text-xl font-semibold mb-4">Admin: Update User Role</h3>
                    <form onSubmit={handleRoleUpdate}>
                        <div className="mb-4">
                            <label className="block mb-1">Select User</label>
                            <select
                                value={selectedUserID}
                                onChange={(e) => setSelectedUserID(e.target.value)}
                                className="w-full p-2 border rounded"
                            >
                                <option value=""></option>
                                {allUsers.filter((u) => u.user_id !== currentUser?.user_id).map((u) => (
                                    <option key={u.user_id} value={u.user_id}>{u.username} ({u.email})</option>
                                ))}
                            </select>
                        </div>
                        <div className="mb-4">
                            <label className="block mb-1">New Role</label>
                            <select
                                value={newRole}
                                onChange={(e) => setNewRole(e.target.value)}
                                className="w-full p-2 border rounded"
                            >
                                <option value=""></option>
                                <option value="user">User</option>
                                <option value="moderator">Moderator</option>
                                <option value="admin">Admin</option>
                            </select>
                        </div>
                        <button
                            type="submit"
                            className="w-full bg-green-600 text-white p-2 rounded hover:bg-green-700"
                        >
                            Update Role
                        </button>
                    </form>
                </div>
            )}
        </div>
    );
};

export default AccountManagement;