import React, { useEffect, useState } from "react";
import { getMyDocuments } from "../services/api";
import type { ReadingDocumentResponse } from "../types";

const DocumentList: React.FC = () => {
    const [documents, setDocuments] = useState<ReadingDocumentResponse[]>([]);
    const [error, setError] = useState("");

    useEffect(() => {
        const fetchDocs = async () => {
        try {
            const result = await getMyDocuments();
            setDocuments(result);
        } catch (err: any) {
            setError(err.response?.data?.detail || "Failed to load documents.");
        }
        };
        fetchDocs();
    }, []);

    return (
        <div className="max-w-3xl mx-auto mt-10 p-6 bg-white rounded-lg shadow">
            <h2 className="text-2xl font-bold text-center mb-4">My Documents</h2>
            {error && <p className="text-red-500 text-center">{error}</p>}
            {documents.length === 0 ? (
                <p className="text-center">No documents uploaded yet.</p>
            ) : (
                documents.map((doc) => (
                <div key={doc.docs_id} className="mb-4 p-4 border rounded">
                    <h3 className="text-lg font-semibold">{doc.docs_title}</h3>
                    <p className="text-sm text-gray-600 mb-1">{doc.docs_description}</p>
                    <p className="text-xs text-gray-500 mb-2">Tags: {doc.docs_tags}</p>
                    <a
                        href={`https://your-s3-bucket-url/${doc.docs_file_path}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-blue-600 hover:underline"
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
