<script lang="ts">
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    onMount(() => {
        goto('/'); // For MVP, 'My Drive' is the same as home
    });
</script>
