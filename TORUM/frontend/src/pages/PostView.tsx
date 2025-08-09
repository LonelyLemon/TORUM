import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { getMyPosts } from "../services/api";
import { type Post } from "../types";

const PostView: React.FC = () => {
    const [posts, setPosts] = useState<Post[]>([]);
    const [error, setError] = useState("");

    useEffect(() => {
        const fetchPosts = async () => {
            try {
                const fetchedPosts = await getMyPosts();
                setPosts(fetchedPosts);
            } catch (error: unknown) {
                const err = error as { response?: { data?: { detail?: string } } };
                setError(err.response?.data?.detail || "Failed to delete post.");
            }
        };
        fetchPosts();
    }, []);

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
                    <div
                        key={post.post_id}
                        className="mb-4 p-4 border rounded hover:bg-gray-50"
                    >
                        <Link
                            to={`/view-post/${post.post_id}`}
                            className="text-xl font-semibold text-blue-600 hover:underline"
                        >
                            {post.post_title}
                        </Link>
                        <p className="text-sm text-gray-600">
                            Created: {new Date(post.created_at).toLocaleString()}
                        </p>
                        <p className="text-sm text-gray-600">
                            Updated: {post.updated_at ? new Date(post.updated_at).toLocaleString() : "Have not been edited"}
                        </p>
                    </div>
                ))
            )}
        </div>
    );
};

export default PostView;