<!-- This component is the main component (aka webpage where we import other components) -->

<script>
  import Country from "./lib/Country.svelte";
  import EuroStat from "./lib/EuroStat.svelte";
  import Map from "./lib/Map.svelte";
  import Policies from "./lib/Policies.svelte";
  import Sectors from "./lib/Sectors.svelte";
</script>

<main>
<Country />
<EuroStat />
<Map />
<Policies />
<Sectors />
</main>

<style>

</style>
