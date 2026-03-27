<script lang="ts">
    import type { FolderEntry } from '$lib/types';
    let { folder } = $props<{ folder: FolderEntry }>();
</script>

<div class="bg-gray-50/50 border border-gray-100 rounded-2xl p-4 hover:bg-blue-50/50 hover:border-blue-100 transition-all duration-300 cursor-pointer group flex items-center gap-4 active:scale-95 shadow-sm hover:shadow-md">
    <div class="w-10 h-10 bg-white rounded-xl shadow-sm flex items-center justify-center text-blue-500 group-hover:scale-110 transition-transform">
        <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24"><path d="M10 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2h-8l-2-2z"/></svg>
    </div>
    <div class="flex flex-col min-w-0">
        <span class="text-sm font-semibold text-gray-700 truncate group-hover:text-blue-700 transition-colors">{folder.name}</span>
        <span class="text-[10px] text-gray-400 font-medium uppercase tracking-wider">Folder</span>
    </div>
    <div class="ml-auto opacity-0 group-hover:opacity-100 transition-opacity">
        <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
    </div>
</div>
