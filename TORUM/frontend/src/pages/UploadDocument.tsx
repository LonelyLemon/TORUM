import React, {useState} from "react";

import { uploadReadingDocument } from "../services/api";

const UploadDocument: React.FC = () => {
    const [title, setTitle] = useState("");
    const [description, setDescription] = useState("");
    const [tags, setTags] = useState("");
    const [file, setFile] = useState<File | null>(null);
    const [message, setMessage] = useState("");

    const handleUpload = async () => {
        if (!file) {
        setMessage("Please select a file.");
        return;
        }

        try {
            await uploadReadingDocument({ docs_title: title, docs_description: description, docs_tags: tags }, file);
            setMessage("File uploaded successfully!");
            setTitle("");
            setDescription("");
            setTags("");
            setFile(null);
            } catch (error: any) {
            setMessage(error.response?.data?.detail || "Upload failed.");
            }
    };

    return (
        <div className="max-w-2xl mx-auto mt-10 p-6 bg-white rounded-lg shadow">
            <h2 className="text-2xl font-bold text-center mb-4">Upload Document</h2>
            {message && <p className="text-center text-sm text-red-500">{message}</p>}
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
            />
            <button
                onClick={handleUpload}
                className="w-full bg-blue-600 text-white py-2 rounded"
            >
                Upload
            </button>
        </div>
    );
};

export default UploadDocument;