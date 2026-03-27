<script lang="ts">
	import '../app.css';
	import { page } from '$app/stores';
    import { onMount } from 'svelte';
    import PathSettingsModal from '$lib/components/PathSettingsModal.svelte';

	let { children } = $props();

    let storageInfo = $state({ total: 1, used: 0, free: 1, path: '' });
    let showPathModal = $state(false);

	const menuItems = [
		{ name: 'Home', href: '/', icon: 'M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6' },
		{ name: 'My Drive', href: '/drive', icon: 'M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z' },
		{ name: 'Starred', href: '/starred', icon: 'M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z' },
	];

    async function fetchStorage() {
        try {
            const res = await fetch('http://localhost:8000/system/storage-info');
            storageInfo = await res.json();
        } catch (e) { console.error(e); }
    }

    onMount(fetchStorage);

    function formatBytes(bytes: number) {
        if (bytes === 0) return '0 B';
        const k = 1024;
        const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
    }
</script>

<div class="flex h-screen bg-[#F8F9FA] text-[#3C4043] antialiased select-none overflow-hidden">
	<!-- Sidebar -->
	<aside class="w-64 flex flex-col pt-4 pb-6 transition-all duration-300 border-r border-transparent">
		<!-- Brand / Logo -->
		<a href="/" class="flex items-center gap-3 px-6 mb-4 group decoration-transparent">
			<div class="w-10 h-10 bg-white rounded-lg flex items-center justify-center p-1.5 shadow-sm group-hover:shadow-md transition-all">
				<svg viewBox="0 0 87.3 78" class="w-full h-full"><path d="m6.6 66.85 3.85 6.65c.8 1.4 1.95 2.5 3.3 3.3l13.75-23.8h-27.5c0 1.55.4 3.1 1.2 4.5z" fill="#0066da"/><path d="m43.65 23.95-13.75-23.8c-1.35.8-2.5 1.9-3.3 3.3l-25.4 44c-.8 1.4-1.2 2.95-1.2 4.5h27.5z" fill="#00ac47"/><path d="m73.55 76.8c1.35-.8 2.5-1.9 3.3-3.3l1.6-2.75 7.65-13.25c.8-1.4 1.2-2.95 1.2-4.5h-27.5l.2 3.5.05 3.5 6.1 10.55s3.55 6.25 3.7 6.5c.8 1.4 1.95 2.5 3.3 3.3z" fill="#ea4335"/><path d="m43.65 23.95 13.75 23.8h27.5c0-1.55-.4-3.1-1.2-4.5l-25.4-44c-.8-1.4-1.95-2.5-3.3-3.3z" fill="#ffbc00"/><path d="m43.65 78c1.55 0 3.1-.4 4.5-1.2l13.75-23.8h-36.5l-13.75 23.8c1.4.8 2.95 1.2 4.5 1.2z" fill="#2684fc"/><path d="m57.4 47.75-13.75-23.8-13.75 23.8h27.5z" fill="#00832d"/></svg>
			</div>
			<span class="text-[22px] font-medium text-[#5F6368]">Drive</span>
		</a>

		<!-- New Button -->
		<div class="px-3 mb-4 flex flex-col gap-2">
            <button 
                onclick={() => showPathModal = true}
                class="flex items-center gap-3 px-5 py-3.5 bg-[#E8F0FE] text-[#1967D2] rounded-2xl hover:bg-[#D2E3FC] transition-all group border border-transparent hover:border-[#4285F4]"
                title="Change local directory"
            >
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path></svg>
                <span class="text-sm font-medium">Set Storage</span>
            </button>
			<button 
                onclick={() => alert('Feature coming soon!')}
                class="flex items-center gap-3 px-5 py-3.5 bg-white border border-[#DADCE0] rounded-2xl shadow-sm hover:shadow-md transition-all active:scale-[0.98] group"
            >
				<svg class="w-6 h-6 text-[#1A73E8]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 4v16m8-8H4"/></svg>
				<span class="text-sm font-medium text-[#3C4043]">New</span>
			</button>
		</div>

		<!-- Main Nav -->
		<nav class="flex-1 px-3">
			<ul class="space-y-0.5">
				{#each menuItems as item}
					<li>
						<a 
							href={item.href} 
							class="flex items-center gap-4 px-4 py-2.5 rounded-r-full text-[14px] font-medium transition-colors { $page.url.pathname === item.href ? 'bg-[#E8F0FE] text-[#1967D2]' : 'hover:bg-[#F1F3F4] text-[#3C4043]' }"
						>
							<svg class="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d={item.icon}></path></svg>
							{item.name}
						</a>
					</li>
				{/each}
			</ul>
		</nav>

		<!-- Storage info -->
		<div class="px-6 py-4 mt-auto">
			<div class="flex items-center gap-3 mb-3 text-[#5F6368]">
				<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z"/></svg>
				<span class="text-[13px] font-medium">Device Storage</span>
			</div>
			<div class="w-full h-1 bg-[#DADCE0] rounded-full overflow-hidden mb-2">
				<div class="h-full bg-[#1A73E8]" style="width: {(storageInfo.used / storageInfo.total) * 100}%"></div>
			</div>
			<p class="text-[12px] text-[#5F6368]">{formatBytes(storageInfo.used)} used of {formatBytes(storageInfo.total)}</p>
            <div class="mt-2 text-[10px] text-[#5F6368] opacity-60 truncate" title={storageInfo.path}>
                {storageInfo.path}
            </div>
		</div>
	</aside>

    <PathSettingsModal bind:show={showPathModal} onUpdate={() => { fetchStorage(); window.location.href = '/'; }} />

	<!-- Main Container -->
	<main class="flex-1 flex flex-col bg-white overflow-hidden m-2 rounded-2xl shadow-sm border border-[#DADCE0]">
		<!-- Header -->
		<header class="h-16 flex items-center justify-between px-6 border-b border-[#F1F3F4]">
			<!-- Search Bar -->
			<div class="flex-1 max-w-2xl group">
				<div class="relative flex items-center bg-[#F1F3F4] rounded-full px-4 py-2.5 focus-within:bg-white focus-within:shadow-md transition-all border border-transparent focus-within:border-[#DADCE0]">
					<button class="p-1 hover:bg-gray-200 rounded-full transition-colors mr-2 text-[#5F6368]">
						<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
					</button>
					<input 
						type="text" 
						placeholder="Search in Drive" 
						class="w-full bg-transparent outline-none text-[15px] placeholder-[#5F6368] text-[#3C4043]"
					/>
					<button class="p-1 hover:bg-gray-200 rounded-full transition-colors ml-2 text-[#5F6368]">
						<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4"/></svg>
					</button>
				</div>
			</div>

			<!-- Right Actions -->
			<div class="flex items-center gap-2 ml-6">
				<button class="p-2 hover:bg-[#F1F3F4] rounded-full text-[#5F6368] transition-colors">
					<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
				</button>
				<button class="p-2 hover:bg-[#F1F3F4] rounded-full text-[#5F6368] transition-colors">
					<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
				</button>
				<div class="ml-2 w-8 h-8 rounded-full bg-[#1A73E8] flex items-center justify-center text-white font-semibold text-sm cursor-pointer border-2 border-white shadow-sm">K</div>
			</div>
		</header>

		<!-- Content -->
		<div class="flex-1 overflow-y-auto px-6 py-4">
			{@render children()}
		</div>
	</main>
</div>
