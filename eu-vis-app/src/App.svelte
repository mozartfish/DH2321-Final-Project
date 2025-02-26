<!-- App.svelte -->
<script>
  import CountryData from './lib/CountryData.svelte';
  import EUData from './lib/EUData.svelte';
  import EUMap from './lib/EUMap.svelte';
  import Country from './lib/Country.svelte';
  import { onMount } from 'svelte';
  import * as d3 from 'd3';

  // data structures to process the data
  let allData = $state([]);
  let selectedFile = $state('');
  let selectedCountry = $state('');
  let selectedDataFileData = $state([]);
  let selectedCountryData = $state([]);
  let isDataLoaded = $state(false);
  
  // a list of country names in the european union
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
  });

  function selectData() {
    const dataFile = allData.find((item) => item.file === selectedFile);
    if (dataFile) {
      console.log('hello world I am the app data component');
      selectedDataFileData = dataFile.data;
      selectedCountryData = selectedDataFileData.filter(
        (item) => item.country === selectedCountry
      );
    } else {
      selectedDataFileData = [];
      console.log('No data found for:', selectedDataFileData);
    }
  }
  
  // Updated country selection handler for callback approach
  function handleCountrySelect(data) {
    selectedCountry = data.country;
    selectData(); // Update the data based on the new country selection
  }
  
  $effect(() => {
    console.log('allData : ', allData);
  });
</script>

<main>
  <h3>Main App Component</h3>

  <!-- Updated to use callback instead of event -->
  <EUMap countries={countryNames} onCountrySelect={handleCountrySelect} />

  <br/>

  <select bind:value={selectedFile}>
    {#each allData as d}
      <option value={d.file}>{d.file}</option>
    {/each}
  </select>

  <select bind:value={selectedCountry} onchange={selectData}>
    {#each countryNames as c}
      <option value={c}>{c}</option>
    {/each}
  </select>

  <button onclick={selectData}>Select Data</button>

  {#if isDataLoaded}
    <CountryData countryData={selectedCountryData} country={selectedCountry} />
  {/if}
  <!-- <Country/> -->
  <!-- <EUData data={selectedDataFileData} country={selectedCountry} /> -->
</main>








