import React, { type FormEvent, useState } from "react";
import { Link } from "react-router-dom";

import { useAuth } from "../context/AuthContext";
import { createPost } from "../services/api";
import { type Post } from "../types";

const Posts: React.FC = () => {
    const [title, setTitle] = useState('');
    const [content, setContent] = useState('');
    const [postID, setPostID] = useState('');
    const [post, setPost] = useState<Post | null>(null);
    const [error, setError] = useState(''); 
    const { user } = useAuth();

    // Create Post
    const handleCreateSubmit = async (e: FormEvent) => {
        e.preventDefault();
        if (!user) return;
        setError('');
        try {
            const newPost = await createPost({ post_title: title, post_content: content });
            setPost(newPost);
            setPostID(newPost.post_id);
            setTitle('');
            setContent('');
            alert('Post created!'); 
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Failed to create post');
        }
    };

    return (
    <div className="container mx-auto p-4">
        <h2 className="text-2xl font-bold text-center mb-4">Post Manager</h2>
        {error && <p className="text-red-500 mb-4">{error}</p>}

        {/* Create Post Form */}
        <form onSubmit={handleCreateSubmit} className="max-w-md mx-auto p-6 bg-white rounded-lg shadow">
            <div className="mb-4">
                <label className="block mb-1">Post Title</label>
                <input
                    type="text"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    placeholder="Enter post title"
                    className="w-full p-2 border rounded"
                />
            </div>
            <div className="mb-4">
                <label className="block mb-1">Post Content</label>
                <textarea
                    value={content}
                    onChange={(e) => setContent(e.target.value)}
                    placeholder="Enter post content"
                    className="w-full p-2 border rounded"
                    rows={4}
                />
            </div>
            <button type="submit" className="w-full bg-blue-600 text-white p-2 rounded hover:bg-blue-700">
                Create Post
            </button>
        </form>

        {/* View Post*/}
        <div className="max-w-md mx-auto mt-4">
            <Link to={`/view-post`} className="text-blue-600 hover:underline">
                View Post
            </Link>
        </div>
    </div>
  );
};

export default Posts