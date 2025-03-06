<script>
  // imports
  import { onMount } from 'svelte';
  import * as d3 from 'd3';
  import Slider from './lib/Slider.svelte';
  import PolicyChart from './lib/PolicyChart.svelte';

  // components
  import EUMap from './lib/EUMap.svelte';
  import PolicyData from './lib/PolicyData.svelte';
  import EUData from './lib/EUData.svelte';
  import BarChart from './lib/BarChart.svelte';


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

  let year = $state(2022);

  let isClimateView = $state(true);

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
    // let policySectorData = policyData.map((d, i) => {
    //   console.log('sector data:', d.sector);
    // });

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

  function handleDataSelect(file) {
    selectedFile = file;
    console.log('selectedFile :', selectedFile);
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
  <nav>
    <h2>EU Climate Insights</h2>
    <div class="links">
      <a>Home</a>
      <a>About</a>
      <a>Contact</a>
    </div>
  </nav>
  <!-- render visualization components after all the data is loaded  -->
  <h1>EU Climate Insights</h1>

  <div id="toggle">
    <button
      onclick={() => (isClimateView = true)}
      class={isClimateView ? 'climate-active' : ''}>Climate</button
    >
    <button
      onclick={() => (isClimateView = false)}
      class={!isClimateView ? 'policies-active' : ''}>Policies</button
    >
  </div>

  {#if isDataLoaded}
    <section id="overview">
      <section id="presenter">
        <section id="map">
          <EUMap
            countries={EU_COUNTRIES}
            allCountriesData={selectedDataFileData}
            onCountrySelect={handleCountrySelect}
            {selectedFile}
            {year}
          />
        </section>
        <section id="pol-sec">
          <select bind:value={selectedFile} onchange={selectData}>
            {#each allData as d}
              <option value={d.file}>{d.file}</option>
            {/each}
          </select>

          <BarChart
            {allData}
            {handleDataSelect}
            {selectedFile}
            {selectedCountry}
            {year}
          />
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
      <Slider bind:year />
    </section>
    <EUData
      allCountriesData={selectedDataFileData}
      euCountries={EU_COUNTRIES}
      {selectedCountry}
      euCountry={EU_COUNTRY}
      {year}
    />
    <!-- <PolicyData {policyData} {selectedCountry} {year} /> -->
  {/if}
</main>

<style>
  nav {
    width: 500px;
    position: fixed;
    z-index: 100;
    top: 10px;
    background-color: antiquewhite;
    border-radius: 10px;
    border: 2px solid rgba(0, 0, 0, 0.8);
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    padding: 4px;
    font-size: 0.9rem;
  }

  nav h2 {
    margin-left: 20px;
  }

  #toggle {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    gap: 10px;
    margin: 20px;
  }

  button {
    width: 200px;
    height: 50px;
    border: 2px solid black;
    box-shadow: 3px 3px 0px rgba(0, 0, 0, 1);
    border-radius: 10px;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 20px;
    cursor: pointer;
    transition-property: box-shadow, transform, background-color;
    transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
    transition-duration: 150ms;
  }

  button:hover {
    box-shadow: 0px 0px 0px 0px black;
    transform: translate(2px, 2px);
  }

  button:active {
    transform: translate(2px, 4px);
  }

  button.climate-active {
    background-color: #27af61;
    box-shadow: 0px 0px 0px 0px black;
    transform: translate(2px, 2px);
  }

  button.policies-active {
    background-color: #f49c12;
    box-shadow: 0px 0px 0px 0px black;
    transform: translate(2px, 2px);
  }

  .links {
    margin-right: 20px;
    display: flex;
    flex-direction: row;
    gap: 20px;
  }

  h1 {
    margin-top: 60px;
    text-align: center;
  }

  #overview {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    border-radius: 10px;
    border: 3px solid rgba(0, 0, 0, 0.8);
    /* box-shadow: 3px 3px 0px rgba(0, 0, 0, 0.8); */
    padding: 10px;
    background-color: antiquewhite;
  }

  #presenter {
    display: flex;
    flex-direction: row;
    align-items: stretch;
    justify-content: center;
    gap: 20px;
  }

  #map {
    border-radius: 10px;
    border: 3px solid rgba(0, 0, 0, 0.8);
    padding-top: 20px;
    padding-left: 50px;
    padding-right: 50px;
    background-color: white;
  }

  #pol-sec {
    width: 50%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 20px;
  }

  #pol-sec select {
    padding: 12px 12px;
    border: 3px solid rgba(0, 0, 0, 0.8);
    border-radius: 10px;
    background-color: white;
    font-size: 1rem;
    color: #333;
    outline: none;
    width: 100%;
  }
</style>
