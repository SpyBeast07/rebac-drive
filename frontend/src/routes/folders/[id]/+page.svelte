<script lang="ts">
    import { onMount } from 'svelte';
    import { page } from '$app/stores';
    import type { FileEntry, FolderEntry } from '$lib/types';
    import ShareModal from '$lib/components/ShareModal.svelte';
    import FilePreviewModal from '$lib/components/FilePreviewModal.svelte';

    let id = $derived($page.params.id);
    let data = $state<{ folders: FolderEntry[], files: FileEntry[] }>({ folders: [], files: [] });
    let loading = $state(true);
    let currentUserId = "user1";

    let showShareModal = $state(false);
    let showPreviewModal = $state(false);
    let selectedItem = $state<any>(null);

    async function fetchData() {
        if (!id) return;
        loading = true;
        try {
            const res = await fetch(`http://localhost:8000/folders/${id}?user_id=${currentUserId}`);
            data = await res.json();
        } catch (e) {
            console.error(e);
        } finally {
            loading = false;
        }
    }

    $effect(() => {
        fetchData();
    });

    function openShare(item: any) {
        selectedItem = item;
        showShareModal = true;
    }

    function openFile(file: FileEntry) {
        selectedItem = file;
        showPreviewModal = true;
    }

    function formatDate(dateStr: string) {
        if (!dateStr) return '--';
        const d = new Date(dateStr);
        return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
    }
</script>

<div class="max-w-screen-xl mx-auto space-y-10">
    <!-- Breadcrumbs / Header -->
    <div class="flex items-center gap-2 text-sm text-[#5F6368] mb-6">
        <a href="/" class="hover:underline">My Drive</a>
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
        <span class="font-medium text-[#3C4043]">Folder</span>
    </div>

    <!-- Folders -->
    {#if data.folders.length > 0}
    <section>
        <h2 class="text-[15px] font-medium text-[#3C4043] mb-4">Folders</h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {#each data.folders as folder}
                <a href="/folders/{folder.id}" class="flex items-center gap-3 p-3 border border-[#DADCE0] rounded-lg hover:bg-[#F1F3F4] transition-colors group decoration-transparent">
                    <svg class="w-6 h-6 text-[#5F6368]" fill="currentColor" viewBox="0 0 24 24"><path d="M10 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2h-8l-2-2z"/></svg>
                    <span class="text-[14px] font-medium text-[#3C4043] truncate">{folder.name}</span>
                </a>
            {/each}
        </div>
    </section>
    {/if}

    <!-- Files -->
    <section>
        <h2 class="text-[15px] font-medium text-[#3C4043] mb-4">Files</h2>
        <div class="space-y-0.5">
            {#if loading}
                {#each Array(3) as _}
                    <div class="h-12 bg-[#F1F3F4] rounded-lg animate-pulse mb-1"></div>
                {/each}
            {:else if data.files.length === 0 && data.folders.length === 0}
                <div class="py-20 text-center text-[#5F6368]">
                    <p class="text-lg opacity-40">This folder is empty</p>
                </div>
            {:else}
                {#each data.files as file}
                    <div 
                        onclick={() => openFile(file)}
                        class="flex items-center px-4 py-2.5 rounded hover:bg-[#F1F3F4] border-b border-[#F1F3F4] transition-colors cursor-pointer group"
                    >
                        <div class="flex-1 flex items-center gap-3 min-w-0">
                            <svg class="w-5 h-5 text-[#DADCE0]" fill="currentColor" viewBox="0 0 24 24"><path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/></svg>
                            <span class="text-sm font-medium text-[#3C4043] truncate">{file.name}</span>
                        </div>
                        <div class="w-32 hidden sm:flex items-center gap-2">
                             <div class="w-6 h-6 rounded-full bg-blue-100 flex items-center justify-center text-[10px] font-bold text-blue-600">M</div>
                             <span class="text-sm text-[#5F6368]">me</span>
                        </div>
                        <div class="w-32 hidden sm:block text-sm text-[#5F6368]">
                            {formatDate(file.created_at)}
                        </div>
                        <div class="opacity-0 group-hover:opacity-100 flex items-center gap-1 ml-4 transition-opacity">
                            <button onclick={() => openShare(file)} class="p-2 hover:bg-[#E8F0FE] hover:text-[#1A73E8] rounded-full text-[#5F6368]"><svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 100-2.684 3 3 0 000 2.684zm0 12.684a3 3 0 100-2.684 3 3 0 000 2.684z"/></svg></button>
                        </div>
                    </div>
                {/each}
            {/if}
        </div>
    </section>
</div>

{#if showShareModal && selectedItem}
<ShareModal bind:show={showShareModal} item={selectedItem} />
{/if}

{#if showPreviewModal && selectedItem}
<FilePreviewModal bind:show={showPreviewModal} file={selectedItem} />
{/if}
