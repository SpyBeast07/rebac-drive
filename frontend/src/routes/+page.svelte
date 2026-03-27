<script lang="ts">
	import { onMount } from 'svelte';
	import type { FileEntry, FolderEntry } from '$lib/types';
    import ShareModal from '$lib/components/ShareModal.svelte';
    import FilePreviewModal from '$lib/components/FilePreviewModal.svelte';
	
	let data = $state<{ folders: FolderEntry[], files: FileEntry[] }>({ folders: [], files: [] });
	let loading = $state(true);
	let currentUserId = "user1";

    let showShareModal = $state(false);
    let showPreviewModal = $state(false);
    let selectedItem = $state<any | null>(null);

	onMount(async () => {
		try {
            const res = await fetch(`http://localhost:8000/folders/root?user_id=${currentUserId}`);
			data = await res.json();
		} catch (e) {
			console.error("Dashboard fetch error:", e);
		} finally {
			loading = false;
		}
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
        const d = new Date(dateStr);
        return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
    }
</script>

<div class="max-w-screen-xl mx-auto space-y-10">
    <!-- Suggested Section (Big Cards) -->
    <section>
        <div class="flex items-center justify-between mb-4">
            <h2 class="text-[15px] font-medium text-[#3C4043]">Suggested</h2>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {#if loading}
                {#each Array(4) as _}
                    <div class="h-40 bg-[#F1F3F4] rounded-xl animate-pulse"></div>
                {/each}
            {:else if data.files.length > 0}
                {#each data.files.slice(0, 4) as file}
                    <div 
                        onclick={() => openFile(file)}
                        role="button"
                        tabindex="0"
                        onkeydown={(e) => e.key === 'Enter' && openFile(file)}
                        class="bg-white border border-[#DADCE0] rounded-xl overflow-hidden hover:shadow-md transition-shadow group cursor-pointer outline-none focus:ring-2 focus:ring-blue-100"
                    >
                        <div class="h-28 bg-[#F1F3F4] flex items-center justify-center border-b border-[#DADCE0]">
                            <!-- File Icon / Preview Placeholder -->
                             <svg class="w-12 h-12 text-[#DADCE0]" fill="currentColor" viewBox="0 0 24 24"><path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/></svg>
                        </div>
                        <div class="p-3 flex items-center justify-between">
                            <div class="flex items-center gap-2 min-w-0">
                                <svg class="w-4 h-4 text-[#4285F4] flex-shrink-0" fill="currentColor" viewBox="0 0 24 24"><path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/></svg>
                                <span class="text-[13px] font-medium truncate">{file.name}</span>
                            </div>
                            <button 
                                onclick={(e) => { e.stopPropagation(); openShare(file); }}
                                class="opacity-0 group-hover:opacity-100 p-1 hover:bg-[#F1F3F4] rounded-full text-[#5F6368] transition-all"
                            >
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 100-2.684 3 3 0 000 2.684zm0 12.684a3 3 0 100-2.684 3 3 0 000 2.684z"></path></svg>
                            </button>
                        </div>
                    </div>
                {/each}
            {/if}
        </div>
    </section>

    <!-- Folders Section -->
    <section>
        <div class="flex items-center justify-between mb-4">
            <h2 class="text-[15px] font-medium text-[#3C4043]">Folders</h2>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {#if loading}
                {#each Array(4) as _}
                    <div class="h-12 bg-[#F1F3F4] rounded-lg animate-pulse"></div>
                {/each}
            {:else}
                {#each data.folders as folder}
                    <a 
                        href="/folders/{folder.id}"
                        class="flex items-center gap-3 p-3 border border-[#DADCE0] rounded-lg hover:bg-[#F1F3F4] transition-colors cursor-pointer group decoration-transparent"
                    >
                        <svg class="w-6 h-6 text-[#5F6368]" fill="currentColor" viewBox="0 0 24 24"><path d="M10 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2h-8l-2-2z"/></svg>
                        <span class="text-[14px] font-medium text-[#3C4043] truncate">{folder.name}</span>
                        <div class="ml-auto opacity-0 group-hover:opacity-100 flex items-center">
                            <button 
                                onclick={(e) => { e.preventDefault(); e.stopPropagation(); openShare(folder); }}
                                class="p-1 hover:bg-[#E8F0FE] hover:text-[#1A73E8] rounded-full text-[#5F6368] transition-all"
                            >
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 100-2.684 3 3 0 000 2.684zm0 12.684a3 3 0 100-2.684 3 3 0 000 2.684z"></path></svg>
                            </button>
                        </div>
                    </a>
                {/each}
            {/if}
        </div>
    </section>

    <!-- Files Table-like Grid -->
    <section>
        <div class="flex items-center justify-between mb-4 border-b border-[#F1F3F4] pb-2">
            <h2 class="text-[15px] font-medium text-[#3C4043]">Files</h2>
        </div>
        
        <div class="space-y-0.5">
            {#if loading}
                {#each Array(5) as _}
                    <div class="h-12 bg-[#F1F3F4] rounded-lg animate-pulse mb-1"></div>
                {/each}
            {:else if data.files.length === 0}
                <div class="py-20 text-center text-[#5F6368]">
                    <svg class="w-16 h-16 mx-auto mb-4 opacity-10" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M9 13h6m-3-3v6m5 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
                    <p class="text-lg">No files here yet</p>
                    <p class="text-sm mt-1 opacity-60">Add some files to your storage folder to see them appear here.</p>
                </div>
            {:else}
                <!-- Header Column Labels -->
                <div class="flex items-center px-4 py-2 text-[12px] font-bold text-[#5F6368] uppercase tracking-wider">
                    <div class="flex-1">Name</div>
                    <div class="w-32 hidden sm:block">Owner</div>
                    <div class="w-32 hidden sm:block">Date</div>
                    <div class="w-12 text-right">Size</div>
                </div>
                
                {#each data.files as file}
                    <div 
                        onclick={() => openFile(file)}
                        role="button"
                        tabindex="0"
                        onkeydown={(e) => e.key === 'Enter' && openFile(file)}
                        class="flex items-center px-4 py-2.5 rounded hover:bg-[#F1F3F4] border-b border-[#F1F3F4] transition-colors cursor-pointer group outline-none focus:bg-blue-50/50"
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
                        <div class="w-12 text-right text-sm text-[#5F6368]">--</div>
                        <div class="opacity-0 group-hover:opacity-100 flex items-center gap-1 ml-4 transition-opacity">
                            <button onclick={(e) => { e.stopPropagation(); openShare(file); }} class="p-2 hover:bg-[#E8F0FE] hover:text-[#1A73E8] rounded-full text-[#5F6368]"><svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 100-2.684 3 3 0 000 2.684zm0 12.684a3 3 0 100-2.684 3 3 0 000 2.684z"/></svg></button>
                            <button class="p-2 hover:bg-[#F1F3F4] rounded-full text-[#5F6368]"><svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z"/></svg></button>
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
