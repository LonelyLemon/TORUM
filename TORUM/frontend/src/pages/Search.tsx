import React, { useState } from "react";
import { search } from "../services/api";

const Search: React.FC = () => {
    const [query, setQuery] = useState("");
    const [results, setResults] = useState<any>(null);

    const handleSearch = async () => {
        const data = await search(query);
        setResults(data);
    };

    return (
        <div>
            <input type="text" value={query} onChange={(e) => setQuery(e.target.value)} />
            <button onClick={handleSearch}>Search</button>
            <div>
                {results && (
                    <>
                        <h3>Posts</h3>
                        {results.posts.map((post: any) => (
                            <div key={post.post_id}>{post.post_title}</div>
                        ))}
                        <h3>Documents</h3>
                        {results.documents.map((doc: any) => (
                            <div key={doc.docs_id}>{doc.docs_title}</div>
                        ))}
                    </>
                )}
            </div>
        </div>
    );
};

export default Search;