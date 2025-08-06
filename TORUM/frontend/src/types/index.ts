export interface User {
    user_id: string;
    username: string;
    email: string;
    password?: string;
    user_role: string;
};

export interface UserUpdate {
    username?: string;
    password?: string;
    new_password?: string;
};

/*---------------------------------------------------------------*/

export interface AuthResponse {
    access_token: string;
    refresh_token: string;
    token_type: string;
};

export interface LoginCredentials {
    email: string;
    password: string;
};

export interface SignupCredentials {
    username: string;
    email: string;
    password: string;
};

/*---------------------------------------------------------------*/

export interface Post {
    post_id: string;
    post_owner: string;
    post_title: string;
    post_content: string;
    created_at: string;
    updated_at: string;
};

export interface PostCreate {
    post_title: string;
    post_content: string;
};

export interface PostUpdate {
    post_title: string;
    post_content: string;
};

/*---------------------------------------------------------------*/

// export interface ReadingDocumentUpload {
//     docs_title: string;
//     docs_description: string;
//     docs_tags: string;
// }

export interface ReadingDocumentResponse {
    docs_id: string;
    docs_owner: string;
    docs_title: string;
    docs_description: string;
    docs_tags: string;
    docs_file_path: string;
    uploaded_at: string;
}

/*---------------------------------------------------------------*/

export interface Search {
    post_result: Post[];
    document_result: ReadingDocumentResponse[];
}