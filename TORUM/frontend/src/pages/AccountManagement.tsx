import React, { useEffect, useState } from "react";

import { getUser, updateUser } from "../services/api";
import { type User } from "../types";

const AccountManagement: React.FC = () => {
    const [users, setUser] = useState<User | null>(null);

    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");

    const [editingUsername, setEditingUsername] = useState(false);
    const [editingPassword, setEditingPassword] = useState(false);

    const [editUsername, setEditUsername] = useState("");
    const [newPassword, setNewPassword] = useState("");
    const [confirmNewPassword, setConfirmNewPassword] = useState("");

    useEffect(() => {
        const fetchUser = async () => {
            try {
                const userData = await getUser();
                setUser(userData);
                setEditUsername(userData.username);
            } catch (err: any) {
                setError(err.response?.data?.detail || "Failed to fetch user data.");
            }
        };
        fetchUser();
    }, []);

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
            if (editingUsername && editUsername !== users?.username) {
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
            setUser((prev) => prev ? { ...prev, ...payload} : prev);
            
            setEditingUsername(false);
            setEditingPassword(false);
            setNewPassword("");
            setConfirmNewPassword("");
        } catch (err: any) {
            setError(err.response?.data?.detail || "Failed to update account !")
        }
    };

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
                        value={users?.user_id || ""}
                        disabled
                        className="w-full p-2 border rounded bg-gray-100"
                    />
                </div>
                <div className="mb-4">
                    <label className="block mb-1">Email</label>
                    <input
                        type="email"
                        value={users?.email || ""}
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
        </div>
    );
};

export default AccountManagement;