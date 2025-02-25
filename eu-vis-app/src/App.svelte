<!-- This component is the main component (aka webpage where we import other)-->
<!-- 
A svelte component is structured like this in format 
<script></script> - this is where all your javascript code goes 
content - this is where all the svelte and html code goes 
<style></style> - this is where all the styling and design goes 
-->
<script>
  import CountryData from "./lib/CountryData.svelte";
  import EuData from "./lib/EUData.svelte";
  import EuMap from "./lib/EUMap.svelte";
  import Country from "./lib/Country.svelte";
  import { onMount } from "svelte";
  import * as d3 from "d3";

  const csvFiles = import.meta.glob("/src/data/*.csv", { as: "raw", eager: true });
  let data = [];
  let selectedFile = "";
  let selectedData = [];

  onMount(async () => {
    const tempData = [];
    for (const [path, csvContent] of Object.entries(csvFiles)) {
      const parsed = d3.csvParse(csvContent);
      const fileName = path.replace("/src/data/", "").replace(".csv", "");
      tempData.push({ file: fileName, data: parsed });
    }
    data = tempData;
    if (data.length > 0) {
      selectedFile = data[0].file;
    }
    console.log(data);
  });

  function selectData() {
    const file = data.find(item => item.file === selectedFile);
    if (file) {
      selectedData = file.data;
      console.log(file.data);
    } else {
      selectedData = [];
      console.log("No data found for:", selectedFile);
    }
  }
</script>

<main>
  <select bind:value={selectedFile}>
    {#each data as d}
      <option value={d.file}>{d.file}</option>
    {/each}
  </select>
  <button on:click={selectData}>Select Data</button>

  This is the main content 

  <Country/>
  <EuMap />
  <CountryData data={selectedData} />
  <EuData />
</main>

<style>

</style>
