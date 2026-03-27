<script lang="ts">
    import type { FileEntry } from '$lib/types';
    
    let { show = $bindable(), file } = $props<{ show: boolean, file: FileEntry }>();
    
    let content = $state<string | null>(null);
    let loading = $state(false);
    let error = $state<string | null>(null);
    
    const fileUrl = $derived(`http://localhost:8000/files/${file.id}/content?user_id=user1`);
    const isImage = $derived(file.name.match(/\.(jpg|jpeg|png|gif|webp)$/i));
    const isPdf = $derived(file.name.match(/\.(pdf)$/i));
    const isText = $derived(file.name.match(/\.(txt|md|log|json|js|ts|py|css|html)$/i));

    $effect(() => {
        if (show && isText) {
            fetchText();
        }
    });

    async function fetchText() {
        loading = true;
        error = null;
        try {
            const res = await fetch(fileUrl);
            if (!res.ok) throw new Error('Failed to load content');
            content = await res.text();
        } catch (e: any) {
            error = e.message;
        } finally {
            loading = false;
        }
    }

    function close() {
        show = false;
        content = null;
    }
</script>

{#if show}
<div class="fixed inset-0 z-[100] flex items-center justify-center p-4 sm:p-10">
    <!-- Backdrop -->
    <div 
        onclick={close}
        class="absolute inset-0 bg-black/40 backdrop-blur-sm transition-opacity"
    ></div>

    <!-- Modal Container -->
    <div class="relative w-full max-w-5xl h-full bg-white rounded-2xl shadow-2xl flex flex-col overflow-hidden animate-in fade-in zoom-in duration-200">
        <!-- Header -->
        <div class="h-16 flex items-center justify-between px-6 border-b border-[#F1F3F4] flex-shrink-0">
            <div class="flex items-center gap-3 min-w-0">
                <svg class="w-6 h-6 text-[#1A73E8]" fill="currentColor" viewBox="0 0 24 24"><path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/></svg>
                <div class="min-w-0">
                    <h2 class="text-[16px] font-medium text-[#3C4043] truncate">{file.name}</h2>
                    <p class="text-[12px] text-[#5F6368]">Previewing file</p>
                </div>
            </div>
            <div class="flex items-center gap-2">
                <a href={fileUrl} download={file.name} class="p-2 hover:bg-[#F1F3F4] rounded-full text-[#5F6368] transition-colors" title="Download">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a2 2 0 002 2h12a2 2 0 002-2v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/></svg>
                </a>
                <button onclick={close} class="p-2 hover:bg-[#F1F3F4] rounded-full text-[#5F6368] transition-colors">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
                </button>
            </div>
        </div>

        <!-- Content Area -->
        <div class="flex-1 overflow-auto bg-[#F8F9FA] p-8 flex items-center justify-center">
            {#if loading}
                <div class="flex flex-col items-center gap-4 text-[#5F6368]">
                    <div class="w-8 h-8 border-4 border-blue-100 border-t-blue-600 rounded-full animate-spin"></div>
                    <p class="text-sm font-medium">Loading content...</p>
                </div>
            {:else if error}
                <div class="text-center text-[#D93025]">
                    <p class="font-medium">Error loading preview</p>
                    <p class="text-sm opacity-70">{error}</p>
                </div>
            {:else if isImage}
                <img src={fileUrl} alt={file.name} class="max-w-full max-h-full object-contain rounded-lg shadow-lg border border-white" />
            {:else if isPdf}
                <iframe src={fileUrl} class="w-full h-full rounded-lg border border-[#DADCE0] bg-white shadow-sm" title={file.name}></iframe>
            {:else if isText}
                <div class="w-full max-w-4xl bg-white p-8 rounded-lg border border-[#DADCE0] shadow-sm font-mono text-[13px] leading-relaxed text-[#3C4043] whitespace-pre-wrap selection:bg-blue-100 italic-text-correction">
                    {content}
                </div>
            {:else}
                <div class="text-center text-[#5F6368]">
                    <svg class="w-20 h-20 mx-auto mb-4 opacity-10" fill="currentColor" viewBox="0 0 24 24"><path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/></svg>
                    <p class="font-medium text-lg">Preview not available</p>
                    <p class="text-sm opacity-60 mt-1">Downloading might be required for this file type.</p>
                    <a href={fileUrl} download={file.name} class="mt-6 inline-flex items-center gap-2 px-6 py-2.5 bg-[#1A73E8] text-white rounded-full text-sm font-medium hover:bg-[#185ABC] transition-colors shadow-sm">
                        Download File
                    </a>
                </div>
            {/if}
        </div>
    </div>
</div>
{/if}

<style>
    .italic-text-correction {
        font-style: normal;
    }
</style>
