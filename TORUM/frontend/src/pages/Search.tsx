import React, { useState } from "react";
import { Link } from "react-router-dom";

import { search, downloadDocument } from "../services/api";
import type { Search, Post, ReadingDocumentResponse } from "../types";

const Search: React.FC = () => {
    const [query, setQuery] = useState("");
    const [results, setResults] = useState<Search | null>(null);
    const [error, setError] = useState("");
    const [isLoading, setIsLoading] = useState(false);

    const openDocument = async (id: string) => {
        try {
            const { url } = await downloadDocument(id);
            window.open(url, "_blank", "noopener,noreferrer");
        } catch (err) {
            console.error("Failed to open document", err);
        }
    };

    const handleSearch = async () => {
        if (!query.trim()) {
            setError("Please enter a search query.");
            return;
        }
        setIsLoading(true);
        try {
            const data = await search(query);
            setResults(data);
            setError("");
        } catch (error: any) {
            setError(error.response?.data?.detail || "Failed to perform search.");
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="max-w-2xl mx-auto mt-10 p-6 bg-white rounded-lg shadow">
            <h2 className="text-2xl font-bold text-center mb-4">Search</h2>
            {error && <p className="text-red-500 text-center mb-4">{error}</p>}
            <div className="flex gap-2 mb-4">
                <input
                    type="text"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    onKeyDown={(e) => e.key === "Enter" && handleSearch()}
                    className="w-full p-2 border rounded"
                    placeholder="Search posts and documents..."
                />
                <button
                    onClick={handleSearch}
                    disabled={!query.trim() || isLoading}
                    className="bg-blue-600 text-white px-4 py-2 rounded disabled:bg-gray-400"
                >
                    {isLoading ? "Searching..." : "Search"}
                </button>
            </div>
            {results && (
                <>
                    <h3 className="text-lg font-semibold mb-2">Posts</h3>
                    {results.post_result.length === 0 ? (
                        <p className="text-gray-500">No posts found.</p>
                    ) : (
                        results.post_result.map((post: Post) => (
                            <div
                                key={post.post_id}
                                className="mb-2 p-2 border rounded hover:bg-gray-50"
                            >
                                <Link
                                    to={`/view-post/${post.post_id}`}
                                    className="text-blue-600 hover:underline"
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
                    <h3 className="text-lg font-semibold mb-2 mt-4">Documents</h3>
                    {results.document_result.length === 0 ? (
                        <p className="text-gray-500">No documents found.</p>
                    ) : (
                        results.document_result.map((doc: ReadingDocumentResponse) => (
                            <div
                                key={doc.docs_id}
                                onClick={() => openDocument(doc.docs_id)}
                                className="mb-2 p-2 border rounded cursor-pointer text-blue-600 hover:underline"
                            >
                                {doc.docs_title}
                            </div>
                        ))
                    )}
                </>
            )}
        </div>
    );
};

export default Search;