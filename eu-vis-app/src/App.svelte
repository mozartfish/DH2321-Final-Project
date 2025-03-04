<script>
  // imports
  import { onMount } from 'svelte';
  import * as d3 from 'd3';
  import Slider from './lib/Slider.svelte';
  import PolicyChart from './lib/PolicyChart.svelte';

  // components
  import CountryData from './lib/CountryData.svelte';
  import EUMap from './lib/EUMap.svelte';
  // import PolicyData from './lib/PolicyData.svelte';
  import EUData from './lib/EUData.svelte';

  // import policies data as a raw csv file
  import policiesCSV from '/src/policies.csv?raw';

  // constants
  const EU_COUNTRY = 'EU';
  // list storing all the EU Countries and EU name
  let EU_COUNTRIES = $state([]);

  // State variables
  // all data - all the data for the visualization
  let allData = $state([]);
  // policy data - all the data related to policies
  let policyData = $state([]);
  // selected file - the csv file that is selected by the user
  let selectedFile = $state('');
  // selectedCountry - the country that is selected by the user
  let selectedCountry = $state(null);
  // selectEU - select all the data related to the EU
  let selectEU = $state(EU_COUNTRY);
  // selectedDataFile Data - all the data associated with the data file selected by the user
  let selectedDataFileData = $state([]);
  // boolean for checking whether all the data is loaded and when to start rendering the visualization
  let isDataLoaded = $state(false);

  let year = $state(2024);

  //Derived state
  // selected country data - filter out the data for the country that was selected by the user
  // let selectedCountryData = $derived(
  //   selectedCountry
  //     ? selectedDataFileData.filter((item) => item.country === selectedCountry)
  //     : []
  // );
  // // filter out the data for the EU
  // let selectedEUData = $derived(
  //   selectedDataFileData.filter((item) => item.country == selectEU)
  // );

  // import and load csv data
  const csvFiles = import.meta.glob('/src/data/*.csv', {
    as: 'raw',
    eager: true
  });

  // process and load the data immediately when the web page loads in the browser
  // load all the data into the data array
  async function loadAllData() {
    const tempData = [];
    const countrySet = new Set();
    for (const [path, csvContent] of Object.entries(csvFiles)) {
      const parsedData = d3.csvParse(csvContent);
      // get all the country names that are in the dataset
      for (const country_data of parsedData) {
        countrySet.add(country_data.country);
      }
      const fileName = path
        .replace('/src/data/', '')
        .replace('.csv', '')
        .replace(/_/g, ' ');
      tempData.push({ file: fileName, data: parsedData });
    }

    console.log('temp data: ', tempData);
    console.log('countrySet: ', countrySet);
    allData = tempData;
    // set of countries that belong to the EU + EU data name
    EU_COUNTRIES = [...countrySet];
  }

  // load all the policy data
  async function loadPolicyData() {
    policyData = d3.csvParse(await policiesCSV);
  }

  // data loaded on load
  function dataOnLoad() {
    if (allData.length > 0) {
      selectedFile = allData[0].file;
      selectData();
    }
  }

  // update data when file or country changes
  function selectData() {
    let dataFile = allData.find((item) => item.file === selectedFile);

    if (dataFile) {
      selectedDataFileData = dataFile.data;
    } else {
      selectedDataFileData = [];
      console.error('No data found for:', selectedFile);
    }
  }

  // callback for handling country selection from map
  function handleCountrySelect(data) {
    selectedCountry = data;
    selectData();
  }

  // load the csv data, policy data, and initialize visualization when the app loads
  onMount(async () => {
    await loadAllData();
    await loadPolicyData();
    dataOnLoad();
    isDataLoaded = true;
  });

  // for printing and debugging
  $effect(() => {
    console.log('EU COUNTRIES : ', EU_COUNTRIES);
  });
</script>

<main>
  <!-- render visualization components after all the data is loaded  -->
  <h1>EU Climate Insights</h1>
  {#if isDataLoaded}
    <section id="overview">
      <section id="presenter">
        <EUMap
          countries={EU_COUNTRIES}
          allCountriesData={selectedDataFileData}
          onCountrySelect={handleCountrySelect}
          {selectedFile}
          {year}
        />
        <section id="pol-sec">
          <select bind:value={selectedFile} onchange={selectData}>
            {#each allData as d}
              <option value={d.file}>{d.file}</option>
            {/each}
          </select>

          <PolicyChart {policyData} {year} />
        </section>

        <!-- <CountryData
      countryData={selectedCountryData}
      country={selectedCountry}
      euData={selectedEUData}
      eu={selectEU}
      {policyData}
    /> -->
      </section>
    </section>
    <Slider bind:year />
    <EUData
      allCountriesData={selectedDataFileData}
      euCountries={EU_COUNTRIES}
      {selectedCountry}
      euCountry={EU_COUNTRY}
    />
  {/if}
</main>

<style>
  #overview {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 20px;
    border-radius: 10px;
    border: 3px solid rgba(0, 0, 0, 0.8);
    box-shadow: 3px 3px 0px rgba(0, 0, 0, 0.8);
    padding: 20px;
    background-color: antiquewhite;
  }

  #presenter {
    display: flex;
    flex-direction: row;
    align-items: stretch;
    justify-content: center;
    gap: 40px;
  }

  #pol-sec {
    width: 50%;
    border-radius: 10px;
    border: 3px solid rgba(0, 0, 0, 0.8);
    box-shadow: 4px 4px 0px rgba(0, 0, 0, 0.8);
    padding-top: 20px;
    padding-bottom: 100px;
    padding-left: 50px;
    padding-right: 50px;
    align-items: stretch;
    background-color: white;
  }
</style>
