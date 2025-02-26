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

  // please declare variables here
  // data structures to process the data

  // store the parsed data into this array
  let allData = $state([]);
  // the data file selected by the user
  let selectedFile = $state('');
  // the country selected by the user
  let selectedCountry = $state('');
  // data array for a particular dataset
  let selectedDataFileData = $state([]);
  // data array for a particular country
  let selectedCountryData = $state([]);
  let isDataLoaded = $state(false);
  // a list of country names in the european union - need this to be fact checked or parsed somehow
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

  // import directly and load all the csv files when the app loads
  const csvFiles = import.meta.glob('/src/data/*.csv', {
    as: 'raw',
    eager: true
  });
  // console.log("csv files data: ", csvFiles);

  // process and load data when web page is opened
  onMount(async () => {
    const tempData = [];
    for (const [path, csvContent] of Object.entries(csvFiles)) {
      const parsedData = d3.csvParse(csvContent);
      const fileName = path.replace('/src/data/', '').replace('.csv', '');
      tempData.push({ file: fileName, data: parsedData });
    }
    allData = tempData;
    if (allData.length > 0) {
      // set the first data file to the selected file
      selectedFile = allData[0].file;
      selectedCountry = countryNames[0];
    }
    selectData();
    isDataLoaded = true;
    // print the data after loading
    // console.log('The original loaded data', data);
  });

  function selectData() {
    const dataFile = allData.find((item) => item.file === selectedFile);
    if (dataFile) {
      console.log('hello world I am the app data component');
      // console.log('Selected country: ', selectedCountry);
      // console.log('Selected Dataset: ', selectedFile);
      selectedDataFileData = dataFile.data;
      selectedCountryData = selectedDataFileData.filter(
        (item) => item.country === selectedCountry
      );
    } else {
      selectedDataFileData = [];
      console.log('No data found for:', selectedDataFileData);
    }
  }
</script>

<main>
  This is the main content
  <select bind:value={selectedFile}>
    {#each allData as d}
      <option value={d.file}>{d.file}</option>
    {/each}
  </select>

  <select bind:value={selectedCountry}>
    {#each countryNames as c}
      <option value={c}>{c}</option>
    {/each}
  </select>
  <button onclick={selectData}>Select Data</button>
  {#if isDataLoaded}
    <CountryData countryData={selectedCountryData} country={selectedCountry} />
  {/if}
  <!-- <Country/> -->
  <!-- <EuMap /> -->
  <!-- <EUData data={selectedDataFileData} country={selectedCountry} /> -->
</main>

<style>
</style>
