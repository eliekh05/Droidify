<script>
  import { navigate } from '../lib/router.js';
  export let device;

  function tag(label, cls) {
    return `<span class="tag tag-${cls}">${label}</span>`;
  }

  $: tags = [
    device.has_lineageos  && tag('LineageOS', 'green'),
    device.has_grapheneos && tag('GrapheneOS', 'blue'),
    device.has_twrp       && tag('TWRP', 'blue'),
    device.has_orangefox  && tag('OrangeFox', 'orange'),
  ].filter(Boolean);
</script>

<div class="card" role="button" tabindex="0"
  on:click={() => navigate(`/device/${device.codename}`)}
  on:keydown={e => e.key === 'Enter' && navigate(`/device/${device.codename}`)}>
  <div class="card-mfr">{device.manufacturer || 'Unknown'}</div>
  <div class="card-title">{device.model_name || device.codename}</div>
  <div class="card-codename">{device.codename}</div>
  {#if tags.length}
    <div class="tags">{@html tags.join('')}</div>
  {/if}
</div>
