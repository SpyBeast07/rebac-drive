<script lang="ts">
    import { shareItem } from '$lib/api';
    
    let { show = $bindable(false), item } = $props();
    let targetUser = $state("");
    let loading = $state(false);
    let success = $state(false);

    async function handleShare() {
        if (!targetUser) return;
        loading = true;
        try {
            await shareItem(item.id, targetUser, "viewer", item.type ? "file" : "folder");
            success = true;
            setTimeout(() => {
                show = false;
                success = false;
                targetUser = "";
            }, 1500);
        } catch (e) {
            console.error(e);
        } finally {
            loading = false;
        }
    }
</script>

{#if show}
<div class="fixed inset-0 bg-gray-900/60 backdrop-blur-md flex items-center justify-center z-[100] p-4 transition-all duration-500">
    <div class="bg-white rounded-[32px] shadow-2xl w-full max-w-md p-8 transform transition-all border border-white/20 ring-1 ring-black/5">
        <div class="flex items-center justify-between mb-8">
            <div class="flex flex-col">
                <h3 class="text-2xl font-bold text-gray-900 tracking-tight leading-tight">Share Item</h3>
                <p class="text-sm text-gray-400 font-medium mt-1 truncate max-w-[240px]">{item.name}</p>
            </div>
            <button onclick={() => show = false} class="p-2 hover:bg-gray-100 rounded-2xl text-gray-400 hover:text-gray-600 transition-all active:scale-90">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12"></path></svg>
            </button>
        </div>

        {#if success}
            <div class="flex flex-col items-center py-8 animate-in fade-in zoom-in duration-300">
                <div class="w-20 h-20 bg-green-50 text-green-500 rounded-full flex items-center justify-center mb-6 shadow-sm shadow-green-100">
                    <svg class="w-10 h-10" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"></path></svg>
                </div>
                <h4 class="text-xl font-bold text-gray-800">Successfully shared!</h4>
                <p class="text-sm text-gray-400 mt-2">Access granted to {targetUser}</p>
            </div>
        {:else}
            <div class="space-y-6">
                <div class="space-y-2">
                    <label class="block text-xs font-bold text-gray-400 uppercase tracking-widest ml-1">Add People</label>
                    <div class="relative group">
                        <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                            <svg class="h-5 w-5 text-gray-400 group-focus-within:text-blue-500 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.206" /></svg>
                        </div>
                        <input 
                            type="text" 
                            bind:value={targetUser}
                            placeholder="username or email" 
                            class="w-full pl-11 pr-4 py-4 bg-gray-50 border border-gray-100 rounded-[20px] focus:ring-4 focus:ring-blue-100 focus:bg-white focus:border-blue-400 outline-none transition-all font-medium text-gray-700 placeholder:text-gray-300"
                        />
                    </div>
                </div>
                
                <div class="flex items-start gap-4 p-4 bg-blue-50/50 rounded-2xl border border-blue-100/30">
                    <div class="mt-0.5 text-blue-500 bg-white p-1.5 rounded-lg shadow-sm">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path></svg>
                    </div>
                    <p class="text-[13px] text-blue-700 font-medium leading-snug">
                        Sharing adds a <span class="font-bold underline">viewer</span> relation in OpenFGA for fine-grained access control.
                    </p>
                </div>

                <div class="flex gap-4 pt-4">
                    <button onclick={() => show = false} class="flex-1 py-4 text-gray-500 hover:bg-gray-100 rounded-[20px] font-bold text-sm transition-all active:scale-95">Cancel</button>
                    <button 
                        onclick={handleShare}
                        disabled={loading || !targetUser}
                        class="flex-[2] py-4 bg-blue-600 text-white rounded-[20px] font-bold text-sm hover:bg-blue-700 hover:shadow-xl hover:shadow-blue-200 disabled:opacity-30 disabled:hover:shadow-none transition-all flex items-center justify-center gap-3 active:scale-[0.98]"
                    >
                        {#if loading}
                            <svg class="animate-spin h-5 w-5 text-white" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                        {/if}
                        Send invite
                    </button>
                </div>
            </div>
        {/if}
    </div>
</div>
{/if}
