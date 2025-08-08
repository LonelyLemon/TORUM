import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { api } from "../services/api";
import type { Post } from "../types";

const PostDetail: React.FC = () => {
    const { id } = useParams<{ id: string }>();
    const [post, setPost] = useState<Post | null>(null);
    const [error, setError] = useState("");
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const fetchPost = async () => {
            if (!id) return;
            try {
                const response = await api.get<Post>(`/view-post/${id}`);
                setPost(response.data);
            } catch (error) {
                const err = error as { response?: { data?: { detail?: string } } };
                setError(err.response?.data?.detail || "Failed to load post.");
            } finally {
                setIsLoading(false);
            }
        };
        fetchPost();
    }, [id]);

    if (isLoading) {
        return <p className="text-center">Loading...</p>;
    }

    if (error) {
        return <p className="text-red-500 text-center">{error}</p>;
    }

    if (!post) {
        return <p className="text-center">Post not found.</p>;
    }

    return (
        <div className="max-w-2xl mx-auto mt-10 p-6 bg-white rounded-lg shadow">
            <h2 className="text-2xl font-bold mb-4">{post.post_title}</h2>
            <p>{post.post_content}</p>
        </div>
    );
};

export default PostDetail;