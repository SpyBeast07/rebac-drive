<script lang="ts">
    let { show = $bindable(), onUpdate } = $props<{ show: boolean, onUpdate: (path: string) => void }>();
    
    let path = $state('');
    let loading = $state(false);
    let error = $state<string | null>(null);

    async function handleSubmit() {
        if (!path) return;
        loading = true;
        error = null;
        try {
            const formData = new FormData();
            formData.append('path', path);
            const res = await fetch('http://localhost:8000/settings/storage-path', {
                method: 'POST',
                body: formData
            });
            if (!res.ok) {
                const data = await res.json();
                throw new Error(data.detail || 'Failed to update path');
            }
            onUpdate(path);
            show = false;
        } catch (e: any) {
            error = e.message;
        } finally {
            loading = false;
        }
    }
</script>

{#if show}
<div class="fixed inset-0 z-[110] flex items-center justify-center p-4">
    <div onclick={() => show = false} class="absolute inset-0 bg-black/40 backdrop-blur-sm"></div>
    <div class="relative w-full max-w-md bg-white rounded-2xl shadow-2xl p-6 animate-in fade-in zoom-in duration-200">
        <h2 class="text-xl font-semibold mb-2">Set Storage Path</h2>
        <p class="text-sm text-[#5F6368] mb-6">Enter the absolute path to the local folder you want to manage.</p>
        
        <div class="space-y-4">
            <div>
                <label for="path" class="block text-xs font-medium text-[#5F6368] mb-1 ml-1">Absolute Local Path</label>
                <input 
                    id="path"
                    type="text" 
                    bind:value={path}
                    placeholder="/Users/username/Documents/MyFiles"
                    class="w-full px-4 py-2.5 bg-[#F1F3F4] border border-transparent rounded-lg outline-none focus:bg-white focus:border-[#1A73E8] focus:ring-4 focus:ring-blue-50 transition-all text-sm"
                />
            </div>
            
            {#if error}
            <p class="text-xs text-red-600 bg-red-50 p-2 rounded-lg border border-red-100">{error}</p>
            {/if}

            <div class="flex items-center justify-end gap-3 pt-2">
                <button 
                    onclick={() => show = false}
                    class="px-5 py-2 text-sm font-medium text-[#5F6368] hover:bg-[#F1F3F4] rounded-full transition-colors"
                >
                    Cancel
                </button>
                <button 
                    onclick={handleSubmit}
                    disabled={loading || !path}
                    class="px-6 py-2 bg-[#1A73E8] text-white text-sm font-medium rounded-full hover:bg-[#185ABC] disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-sm flex items-center gap-2"
                >
                    {#if loading}
                    <div class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                    {/if}
                    Save & Restart
                </button>
            </div>
        </div>
    </div>
</div>
{/if}
