export interface FileEntry {
    id: str;
    name: str;
    path: str;
    type: str;
    parent_id: str | null;
    created_at: string;
}

export interface FolderEntry {
    id: str;
    name: str;
    path: str;
    parent_id: str | null;
    created_at: string;
}
