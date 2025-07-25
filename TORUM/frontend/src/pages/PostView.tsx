import React, { useEffect, useState } from "react";

import { getMyPosts, updatePost, deletePost } from "../services/api";
import { type Post } from "../types";

const PostView: React.FC = () => {
    const [posts, setPosts] = useState<Post[]>([]);
    const [error, setError] = useState("");
    const [isEditing, setIsEditing] = useState<string | null>(null);
    const [editTitle, setEditTitle] = useState("");
    const [editContent, setEditContent] = useState("");

    useEffect(() => {
        const fetchPosts = async () => {
            try {
                const fetchedPosts = await getMyPosts();
                setPosts(fetchedPosts);
            } catch (err: any) {
                setError(err.response?.data?.detail || "Failed to fetch posts");
            }
        };
        fetchPosts();
    }, []);

    const handleEditPost = async (postId: string) => {
        try {
            await updatePost(postId, { post_title: editTitle, post_content: editContent });
            setPosts((prevPosts) =>
                prevPosts.map((post) =>
                    post.post_id === postId ? { ...post, post_title: editTitle, post_content: editContent } : post
                )
            );
            setIsEditing(null);
            alert("Post updated!");
        } catch (err: any) {
            setError(err.response?.data?.detail || "Failed to update post");
        }
    };

    const handleDeletePost = async (postId: string) => {
        try {
            await deletePost(postId);
            setPosts((prevPosts) => prevPosts.filter((post) => post.post_id !== postId));
            alert("Post deleted!");
        } catch (err: any) {
            setError(err.response?.data?.detail || "Failed to delete post");
        }
    };

    if (error) {
        return <p className="text-red-500 text-center">{error}</p>;
    }

    return (
        <div className="max-w-2xl mx-auto mt-10 p-6 bg-white rounded-lg shadow">
            <h2 className="text-2xl font-bold text-center mb-4">Your Posts</h2>
            {posts.length === 0 ? (
                <p className="text-center">No posts found.</p>
            ) : (
                posts.map((post) => (
                    <div key={post.post_id} className="mb-6 p-4 border rounded">
                        {isEditing === post.post_id ? (
                            <div>
                                <input
                                    type="text"
                                    value={editTitle}
                                    onChange={(e) => setEditTitle(e.target.value)}
                                    placeholder="Edit title"
                                    className="w-full p-2 border rounded mb-2"
                                />
                                <textarea
                                    value={editContent}
                                    onChange={(e) => setEditContent(e.target.value)}
                                    placeholder="Edit content"
                                    className="w-full p-2 border rounded mb-2"
                                    rows={4}
                                />
                                <button
                                    onClick={() => handleEditPost(post.post_id)}
                                    className="bg-blue-600 text-white px-4 py-2 rounded mr-2"
                                >
                                    Save
                                </button>
                                <button
                                    onClick={() => setIsEditing(null)}
                                    className="bg-gray-500 text-white px-4 py-2 rounded"
                                >
                                    Cancel
                                </button>
                            </div>
                        ) : (
                            <div>
                                <h3 className="text-xl font-bold">{post.post_title}</h3>
                                <p className="mb-2">{post.post_content}</p>
                                <div className="flex space-x-2">
                                    <button
                                        onClick={() => {
                                            setIsEditing(post.post_id);
                                            setEditTitle(post.post_title);
                                            setEditContent(post.post_content);
                                        }}
                                        className="bg-yellow-500 text-white px-4 py-2 rounded"
                                    >
                                        Edit
                                    </button>
                                    <button
                                        onClick={() => handleDeletePost(post.post_id)}
                                        className="bg-red-500 text-white px-4 py-2 rounded"
                                    >
                                        Delete
                                    </button>
                                </div>
                            </div>
                        )}
                    </div>
                ))
            )}
        </div>
    );
};

export default PostView;