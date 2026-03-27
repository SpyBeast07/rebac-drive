const API_BASE = "http://localhost:8000";

export async function fetchFiles(userId: string) {
    const res = await fetch(`${API_BASE}/me/files?user_id=${userId}`);
    if (!res.ok) throw new Error("Failed to fetch files");
    return res.json();
}

export async function fetchFolder(folderId: string, userId: string) {
    const res = await fetch(`${API_BASE}/folders/${folderId}?user_id=${userId}`);
    if (!res.ok) throw new Error("Failed to fetch folder");
    return res.json();
}

export async function shareItem(objectId: string, targetUserId: string, relation: string, type: 'file' | 'folder') {
    const res = await fetch(`${API_BASE}/share`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            object_id: objectId,
            user_id: targetUserId,
            relation: relation,
            type: type
        })
    });
    if (!res.ok) throw new Error("Failed to share item");
    return res.json();
}
