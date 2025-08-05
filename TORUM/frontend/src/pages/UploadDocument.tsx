import React, { useState, useRef } from "react";
import { uploadReadingDocument } from "../services/api";

const UploadDocument: React.FC = () => {
    const [title, setTitle] = useState("");
    const [description, setDescription] = useState("");
    const [tags, setTags] = useState("");
    const [file, setFile] = useState<File | null>(null);
    const [message, setMessage] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const fileInputRef = useRef<HTMLInputElement>(null);

    const handleUpload = async () => {
        if (!file) {
            setMessage("Please select a file.");
            return;
        }
        const allowedExtensions = ['.pdf', '.docx'];
        const ext = file.name.toLowerCase().slice(-4);
        if (!allowedExtensions.includes(ext)) {
            setMessage("Only .pdf and .docx files are allowed.");
            return;
        }
        if (!title.trim()) {
            setMessage("Title is required.");
            return;
        }
        if (title.length > 100) {
            setMessage("Title must be 100 characters or less.");
            return;
        }
        if (description.length > 500) {
            setMessage("Description must be 500 characters or less.");
            return;
        }
        if (tags.length > 100) {
            setMessage("Tags must be 100 characters or less.");
            return;
        }
        setIsLoading(true);
        try {
            await uploadReadingDocument(title, description, tags, file);
            setMessage("File uploaded successfully!");
            setTitle("");
            setDescription("");
            setTags("");
            setFile(null);
            if (fileInputRef.current) {
                fileInputRef.current.value = "";
            }
        } catch (error: any) {
            setMessage(error.response?.data?.detail || "Upload failed.");
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="max-w-2xl mx-auto mt-10 p-6 bg-white rounded-lg shadow">
            <h2 className="text-2xl font-bold text-center mb-4">Upload Document</h2>
            {message && (
                <p className={`text-center text-sm ${message.includes("successfully") ? "text-green-500" : "text-red-500"}`}>
                    {message}
                </p>
            )}
            <input 
                type="text"
                placeholder="Title"
                className="w-full p-2 border rounded mb-2"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
            />
            <textarea 
                placeholder="Description"
                className="w-full p-2 border rounded mb-2"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
            />
            <input 
                type="text"
                placeholder="Tags"
                className="w-full p-2 border rounded mb-2"
                value={tags}
                onChange={(e) => setTags(e.target.value)}
            />
            <input 
                type="file"
                className="mb-4"
                onChange={(e) => setFile(e.target.files?.[0] || null)}
                ref={fileInputRef}
            />
            <button
                onClick={handleUpload}
                disabled={isLoading}
                className="w-full bg-blue-600 text-white py-2 rounded disabled:bg-gray-400"
            >
                {isLoading ? "Uploading..." : "Upload"}
            </button>
        </div>
    );
};

export default UploadDocument;