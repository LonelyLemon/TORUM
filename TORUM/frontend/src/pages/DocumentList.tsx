import React, { useEffect, useState } from "react";
import { getMyDocuments, downloadDocument } from "../services/api";
import type { ReadingDocumentResponse } from "../types";

const DocumentList: React.FC = () => {
    const [documents, setDocuments] = useState<ReadingDocumentResponse[]>([]);
    const [presignedUrls, setPresignedUrls] = useState<{ [key: string]: string }>({});
    const [error, setError] = useState("");
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const fetchDocs = async () => {
            setIsLoading(true);
            try {
                const result = await getMyDocuments();
                setDocuments(result);
                const urls: { [key: string]: string } = {};
                await Promise.all(
                    result.map(async (doc) => {
                        try {
                            const response = await downloadDocument(doc.docs_id);
                            urls[doc.docs_id] = response.url;
                        } catch (error) {
                            urls[doc.docs_id] = "#";
                        }
                    })
                );
                setPresignedUrls(urls);
                setError("");
            } catch (err: any) {
                setError(err.response?.data?.detail || "Failed to load documents.");
            } finally {
                setIsLoading(false);
            }
        };
        fetchDocs();
    }, []);

    return (
        <div className="max-w-3xl mx-auto mt-10 p-6 bg-white rounded-lg shadow">
            <h2 className="text-2xl font-bold text-center mb-4">My Documents</h2>
            {error && <p className="text-red-500 text-center">{error}</p>}
            {isLoading ? (
                <p className="text-center">Loading documents...</p>
            ) : documents.length === 0 ? (
                <p className="text-center">No documents uploaded yet.</p>
            ) : (
                documents.map((doc) => (
                    <div key={doc.docs_id} className="mb-4 p-4 border rounded">
                        <h3 className="text-lg font-semibold">{doc.docs_title}</h3>
                        <p className="text-sm text-gray-600 mb-1">{doc.docs_description || "No description provided"}</p>
                        <p className="text-xs text-gray-500 mb-2">Tags: {doc.docs_tags || "None"}</p>
                        <a
                            href={presignedUrls[doc.docs_id] || "#"}
                            target="_blank"
                            rel="noopener noreferrer"
                            className={`text-blue-600 hover:underline ${!presignedUrls[doc.docs_id] ? "opacity-50 cursor-not-allowed" : ""}`}
                        >
                            View Document
                        </a>
                    </div>
                ))
            )}
        </div>
    );
};

export default DocumentList;