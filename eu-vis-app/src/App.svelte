<!-- App.svelte -->
<script>
  import CountryData from './lib/CountryData.svelte';
  import PolicyData from './lib/PolicyData.svelte';
  import EUData from './lib/EUData.svelte';
  import EUMap from './lib/EUMap.svelte';
  import Country from './lib/Country.svelte';
  import { onMount } from 'svelte';
  import policiesCSV from '/src/policies.csv?raw';

  import * as d3 from 'd3';
  import EuData from './lib/EUData.svelte';

  // data structures to process the data
  let allData = $state([]);
  let selectedFile = $state('');
  let selectedCountry = $state('');
  let selectEU = $state('EU');
  let selectedDataFileData = $state([]);
  let selectedCountryData = $derived(
    selectedDataFileData.filter((item) => item.country === selectedCountry)
  );
  let selectedEUData = $derived(
    selectedDataFileData.filter((item) => item.country == selectEU)
  );
  let isDataLoaded = $state(false);
  let policyData = $state([]);

  // EU Countries
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

  // import and load all the csv data at once
  const csvFiles = import.meta.glob('/src/data/*.csv', {
    as: 'raw',
    eager: true
  });

  // process and load the data immediately when the web page loads in the browser
  onMount(async () => {
    const tempData = [];
    for (const [path, csvContent] of Object.entries(csvFiles)) {
      const parsedData = d3.csvParse(csvContent);
      const fileName = path
        .replace('/src/data/', '')
        .replace('.csv', '')
        .replace(/_/g, ' ');
      tempData.push({ file: fileName, data: parsedData });
    }
    allData = tempData;
    if (allData.length > 0) {
      // set the first data file to the selected file
      selectedFile = allData[0].file;
      selectedCountry = countryNames[0];
    }
    policyData = d3.csvParse(await policiesCSV);
    selectData();
    isDataLoaded = true;
  });

  function selectData() {
    const dataFile = allData.find((item) => item.file === selectedFile);
    if (dataFile) {
      console.log('hello world I am the app data component');
      selectedDataFileData = dataFile.data;
    } else {
      selectedDataFileData = [];
      console.log('No data found for:', selectedDataFileData);
    }
  }

  // callback function to call the select data based on the country the
  // user clicks on the map
  function handleCountrySelect(data) {
    selectedCountry = data.country;
    // trigger a refresh of the UI
    selectData();
  }

  // this effect is for making sure we printing the correct data
  $effect(() => {
    console.log('allData : ', allData);
    console.log('policyData : ', policyData);
  });
</script>

<main>
  <h3>Main App Component</h3>
  <EUMap countries={countryNames} onCountrySelect={handleCountrySelect} />
  <br />

  <select bind:value={selectedFile} onchange={selectData}>
    {#each allData as d}
      <option value={d.file}>{d.file}</option>
    {/each}
  </select>

  <select bind:value={selectedCountry} onchange={selectData}>
    {#each countryNames as c}
      <option value={c}>{c}</option>
    {/each}
  </select>

  <!-- <button onclick={selectData}>Select Data</button> -->

  {#if isDataLoaded}
    <CountryData
      countryData={selectedCountryData}
      country={selectedCountry}
      euData={selectedEUData}
      eu={selectEU}
      {policyData}
    />
    <!-- <PolicyData {policyData} country={selectedCountry} /> -->
  {/if}
  <!-- <Country/> -->
  <!-- <EUData data={selectedDataFileData} country={selectedCountry} /> -->
</main>
