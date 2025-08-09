import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { getPostById, updatePost, deletePost } from "../services/api";
import type { Post } from "../types";
import { useAuth } from "../context/AuthContext";

const PostDetail: React.FC = () => {
    const { id } = useParams<{ id: string }>();
    const { user } = useAuth();
    const [post, setPost] = useState<Post | null>(null);
    const [error, setError] = useState("");
    const [isEditing, setIsEditing] = useState(false);
    const [editTitle, setEditTitle] = useState("");
    const [editContent, setEditContent] = useState("");
    const navigate = useNavigate()

    useEffect(() => {
        const fetchPost = async () => {
            if (!id) return;
            try {
                const fetched = await getPostById(id);
                setPost(fetched);
            } catch (error: unknown) {
                const err = error as { response?: { data?: { detail?: string } } };
                setError(err.response?.data?.detail || "Failed to load post.");
            }
        };
        fetchPost();
    }, [id]);

    const handleSave = async () => {
        if (!post) return;
        try {
            await updatePost(post.post_id, { post_title: editTitle, post_content: editContent });
            const updated = await getPostById(post.post_id);
            setPost(updated);
            setIsEditing(false);
        } catch (error: unknown) {
            const err = error as { response?: { data?: { detail?: string } } };
            setError(err.response?.data?.detail || "Failed to update post.");
        }
    };

    const handleDelete = async () => {
        if (!post) return;
        try {
            await deletePost(post.post_id);
            navigate("/view-post");
        } catch (error: unknown) {
            const err = error as { response?: { data?: { detail?: string } } };
            setError(err.response?.data?.detail || "Failed to delete post.");
        }
    };

    if (error) {
        return <p className="text-red-500 text-center">{error}</p>;
    }

    if (!post) {
        return <p className="text-center">Post not found.</p>;
    }

    return (
        <div className="max-w-2xl mx-auto mt-10 p-6 bg-white rounded-lg shadow">
            {isEditing ? (
                <div>
                    <input
                        type="text"
                        value={editTitle}
                        onChange={(e) => setEditTitle(e.target.value)}
                        className="w-full p-2 border rounded mb-2"
                        placeholder="Edit title"
                    />
                    <textarea
                        value={editContent}
                        onChange={(e) => setEditContent(e.target.value)}
                        className="w-full p-2 border rounded mb-2"
                        rows={6}
                        placeholder="Edit content"
                    />
                    <button
                        onClick={handleSave}
                        className="bg-blue-600 text-white px-4 py-2 rounded mr-2"
                    >
                        Save
                    </button>
                    <button
                        onClick={() => setIsEditing(false)}
                        className="bg-gray-500 text-white px-4 py-2 rounded"
                    >
                        Cancel
                    </button>
                </div>
            ) : (
                <div>
                    <h2 className="text-2xl font-bold mb-4">{post.post_title}</h2>
                    <p className="mb-4 whitespace-pre-line">{post.post_content}</p>
                    <p className="text-sm text-gray-600 mb-1">
                        Created: {new Date(post.created_at).toLocaleString()}
                    </p>
                    <p className="text-sm text-gray-600 mb-4">
                        Updated: {post.updated_at ? new Date(post.updated_at).toLocaleString() : "Have not been edited"}
                    </p>
                    {user && (user.user_role === "admin" ||
                        post.post_owner === user.user_id ||
                        (user.user_role === "moderator" && post.owner_role === "user")) && (
                        <div className="flex space-x-2">
                            <button
                                onClick={() => {
                                    setIsEditing(true);
                                    setEditTitle(post.post_title);
                                    setEditContent(post.post_content);
                                }}
                                className="bg-yellow-500 text-white px-4 py-2 rounded"
                            >
                                Edit
                            </button>
                            <button
                                onClick={handleDelete}
                                className="bg-red-500 text-white px-4 py-2 rounded"
                            >
                                Delete
                            </button>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default PostDetail;