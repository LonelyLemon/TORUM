import React, { type FormEvent, useState } from "react";

import { useAuth } from "../context/AuthContext";
import { createPost, getPost, updatePost, deletePost } from "../services/api";
import { type Post } from "../types";

const Post: React.FC = () => {
    const [title, setTitle] = useState('');
    const [content, setContent] = useState('');
    const [postID, setPostID] = useState('');
    const [post, setPost] = useState<Post | null>(null);
    const [isEditing, setIsEditing] = useState(false);
    const [editTitle, setEditTitle] = useState('');
    const [editContent, setEditContent] = useState('');
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

    // View Post
    const handleFetch = async () => {
        if (!postID) {
            setError('Post ID not found !');
            return;
        }
        setError('');
        try {
            const fetchedPost = await getPost(postID)
            setPost(fetchedPost);
            setIsEditing(false);
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Failed to view post !')
        }
    };

    // Edit Post
    const handleEditPost = async (e: FormEvent) => {
        e.preventDefault();
        if (!user || !post) return;
        setError('');
        try {
            await updatePost(post.post_id, { post_title: editTitle, post_content: editContent });
            setPost({ ...post, post_title: editTitle, post_content: editContent });
            setIsEditing(false);
            alert('Post updated!');
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Failed to update post');
        }
    };

    // Delete Post
    const handleDeletePost = async () => {
        if (!user || !post) return;
        setError('');
        try {
            await deletePost(post.post_id);
            setPost(null);
            setPostID('');
            alert('Post deleted!')
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Failed to delete post');
        }
    };

    return (
    <div className="container mx-auto p-4">
        <h2 className="text-2xl font-bold text-center mb-4">My Post</h2>
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

        {/* View Post */}
        <div className="max-w-md mx-auto mb-8">
            <label className="block mb-1">View Post</label>
            <div className="flex space-x-2">
                <input 
                    type="text"
                    value={postID}
                    onChange={(e) => setPostID(e.target.value)}
                    placeholder="Enter Post ID"
                    className="w-full p-2 border rounded"
                />
                <button onClick={handleFetch} className="bg-green-600 text-while p-2 rounded hover:bg-green-700">
                    View
                </button>
            </div>
        </div>

        {/* Edit Post Form */}
        {post && !isEditing && (
            <div className="max-w-md mx-auto p-6 bg-gray-100 rounded-lg shadow">
                <h3 className="text-xl font-bold mb-2">{post.post_title}</h3>
                <p className="mb-4">{post.post_content}</p>
                <div className="flex space-x-2">
                    <button 
                        onClick={() => {
                            setIsEditing(true);
                            setEditTitle(post.post_title);
                            setEditContent(post.post_content);
                        }}
                        className="bg-yellow-500 text-white p-2 rounded hover:bg-yellow-600"
                    >
                        Edit
                    </button>
                    <button onClick={handleDeletePost} className="bg-red-500 text-white p-2 rounded hover:bg-red-600">
                        Delete
                    </button>
                </div>
            </div>
        )}

        {post && isEditing && (
            <form onSubmit={handleEditPost} className="max-w-md mx-auto p-6 bg-white rounded-lg shadow">
                <div className="mb-4">
                    <label className="block mb-1">Post Title</label>
                    <input 
                        type="text"
                        value={editTitle}
                        onChange={(e) => setEditTitle(e.target.value)}
                        className="w-full p-2 border rounded"
                    />
                </div>
                <div className="mb-4">
                    <label className="block mb-1">Post Content</label>
                    <textarea 
                        value={editContent}
                        onChange={(e) => setEditContent(e.target.value)}
                        className="w-full p-2 border rounded"
                        rows={4}
                    />
                </div>
                <div className="flex space-x-2">
                    <button type="submit" className="bg-blue-600 text-white p-2 rounded hover:bg-blue-700">
                        Save
                    </button>
                    <button type="button" onClick={() => setIsEditing(false)} className="bg-gray-500 text-white p-2 rounded hover:bg-gray-600">
                        Cancel
                    </button>
                </div>
            </form>
        )}
    </div>
  );
};

export default Post;