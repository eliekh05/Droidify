<script>
  export let total = 0;
  export let offset = 0;
  export let limit = 24;
  export let onPage = () => {};

  $: pages = Math.ceil(total / limit);
  $: current = Math.floor(offset / limit);

  function go(page) { onPage(page * limit); }
</script>

{#if pages > 1}
  <div class="pagination">
    {#if current > 0}
      <button class="page-btn" on:click={() => go(current - 1)}>←</button>
    {/if}
    {#each Array(Math.min(pages, 7)) as _, i}
      {@const page = pages <= 7 ? i : current <= 3 ? i : current >= pages - 4 ? pages - 7 + i : current - 3 + i}
      <button class="page-btn {page === current ? 'active' : ''}" on:click={() => go(page)}>
        {page + 1}
      </button>
    {/each}
    {#if current < pages - 1}
      <button class="page-btn" on:click={() => go(current + 1)}>→</button>
    {/if}
  </div>
{/if}
