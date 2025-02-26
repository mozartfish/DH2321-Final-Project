<!-- This component is the main component (aka webpage where we import other)-->
<!-- 
A svelte component is structured like this in format 
<script></script> - this is where all your javascript code goes 
content - this is where all the svelte and html code goes 
<style></style> - this is where all the styling and design goes 
-->
<script>
  import CountryData from './lib/CountryData.svelte';
  import EUData from './lib/EUData.svelte';
  import EUMap from './lib/EUMap.svelte';
  import Country from './lib/Country.svelte';
  import { onMount } from 'svelte';
  import * as d3 from 'd3';

  // import directly and load all the csv files when the app loads
  const csvFiles = import.meta.glob('/src/data/*.csv', {
    as: 'raw',
    eager: true
  });
  // console.log("csv files data: ", csvFiles);

  // data structures to process the data
  let data = $state([]);
  let selectedFile = $state('');
  let selectedCountry = $state('');
  let selectedDataFileData = $state([]);
  let countryNames = [
    'Austria',
    'Belgium',
    'Croatia',
    'Cyprus',
    'Czech Republic',
    'Denmark',
    'Estonia',
    'Finland',
    'France',
    'Germany',
    'Greece',
    'Hungary',
    'Ireland',
    'Italy',
    'Latvia',
    'Lithuania',
    'Luxembourg',
    'Malta',
    'Netherlands',
    'Poland',
    'Portugal',
    'Romania',
    'Slovakia',
    'Slovenia',
    'Spain',
    'Sweden'
  ];

  // load the data when the map is mounted
  onMount(async () => {
    const tempData = [];
    for (const [path, csvContent] of Object.entries(csvFiles)) {
      const parsed = d3.csvParse(csvContent);
      const fileName = path.replace('/src/data/', '').replace('.csv', '');
      tempData.push({ file: fileName, data: parsed });
    }
    data = tempData;
    if (data.length > 0) {
      // set the first data file to the selected file
      selectedFile = data[0].file;
      selectedCountry = countryNames[0];
    }
    // print the data after loading
    // console.log('The original loaded data', data);
  });

  function selectData() {
    const dataFile = data.find((item) => item.file === selectedFile);
    if (dataFile) {
      console.log('hello world I am the app data component');
      console.log('Selected country: ', selectedCountry);
      console.log('Selected Dataset: ', selectedFile);
      selectedDataFileData = dataFile.data;
      console.log('selected data: ', selectedDataFileData);

      // const selectedDataFile = data.find((item) => item.file == selectedFile);
      // selectedDataFileData = selectedDataFile['data'];
      // const EUData = selectedDataFileData.find((item) => item.country === "EU");
      // const selectedCountryData = selectedDataFileData.find(
      //   (item) => item.country === selectedCountry
      // );
      // console.log('selected data file: ', selectedDataFile);
      // console.log('data: ', selectedDataFileData);
      // console.log('selected country data: ', selectedCountryData);
      // console.log("EU Data: ", EUData);

      // selectedData = file.data;
      // console.log('Selected Country: ', selectedCountry);
      // console.log(selectedData);
    } else {
      selectedDataFileData = [];
      console.log('No data found for:', selectedDataFileData);
    }
  }
</script>

<main>
  <select bind:value={selectedFile}>
    {#each data as d}
      <option value={d.file}>{d.file}</option>
    {/each}
  </select>
  <select bind:value={selectedCountry}>
    {#each countryNames as c}
      <option value={c}>{c}</option>
    {/each}
  </select>
  <button onclick={selectData}>Select Data</button>
  <!-- <select bind:value={selectedFile}>
    {#each data as d}
      <option value={d.file}>{d.file}</option>
    {/each}
  </select> -->

  This is the main content

  <!-- <Country/> -->
  <!-- <EuMap /> -->
  <!-- <CountryData data={selectedData} /> -->
  <EUData data={selectedDataFileData} country={selectedCountry} />
</main>

<style>
</style>
