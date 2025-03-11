<script>
  import * as d3 from 'd3';
  import CountryData from './CountryData.svelte';

  const {
    policyData = [],
    selectedCountries = [],
    euCountries = [],
    year
  } = $props();

  const countryList =
    euCountries && euCountries.length > 0
      ? euCountries.filter((c) => c !== 'EU')
      : Array.from(new Set(policyData.map((p) => p.country))).filter(
          (c) => c !== 'EU'
        );

  function countryColorScale() {
    const colorRange = countryList.map((d, i) =>
      d3.interpolatePlasma(i / countryList.length)
    );
    return d3.scaleOrdinal().domain(countryList).range(colorRange);
  }
  let colorScale = countryColorScale();

  // Function to determine text color based on background brightness
  function getContrastYIQ(hexcolor) {
    hexcolor = hexcolor.replace('#', '');
    const r = parseInt(hexcolor.substr(0, 2), 16);
    const g = parseInt(hexcolor.substr(2, 2), 16);
    const b = parseInt(hexcolor.substr(4, 2), 16);
    const yiq = (r * 299 + g * 587 + b * 114) / 1000;
    return yiq >= 110 ? 'black' : 'white';
  }
</script>

<section>
  <h2>{year} Policies</h2>
  {#if policyData.length > 0}
    {#if selectedCountries && selectedCountries.filter((c) => c !== 'EU').length > 0}
      <div class="policy-container">
        {#each selectedCountries.filter((c) => c !== 'EU') as country}
          <ul>
            {#each policyData.filter((policy) => policy.country === country && parseInt(policy.year) === year) as policy}
              <li
                style="background-color: {colorScale(
                  country
                )}; color: {getContrastYIQ(colorScale(country))}"
              >
                <p class="country">{policy.country}</p>
                <p>{policy.policy}</p>
                <p class="sector">
                  {policy.sector.replace(/;/g, ', ')}
                </p>
              </li>
            {/each}
          </ul>
        {/each}
      </div>
    {:else}
      <div class="policy-container">
        <ul>
          {#each policyData.filter((policy) => parseInt(policy.year) === year && policy.country !== 'EU') as policy}
            <li
              style="background-color: {colorScale(
                policy.country
              )}; color: {getContrastYIQ(colorScale(policy.country))}"
            >
              <p class="country">{policy.country}</p>
              <p>{policy.policy}</p>
              <p>
                <i>
                  {policy.sector.replace(/;/g, ', ')}
                </i>
              </p>
            </li>
          {/each}
        </ul>
      </div>
    {/if}
  {/if}
</section>

<style>
  section {
    width: 100%;
    height: 100%;
    overflow-y: scroll;
    border-radius: 10px;
    border: 3px solid rgba(0, 0, 0, 0.8);
    background-color: white;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
    position: relative;
  }

  h2 {
    color: #094c93;
    margin-top: 10px;
  }

  .policy-container {
    padding: 10px;
  }

  ul {
    list-style-type: none;
    padding: 0;
  }

  li {
    margin-bottom: 6px;
    border-radius: 6px;
    border: 2px solid rgba(0, 0, 0, 0.8);
    padding-top: 4px;
    padding-bottom: 4px;
    padding-left: 10px;
    padding-right: 10px;
  }

  .country {
    font-size: 1.5em;
    font-weight: bold;
  }

  .sector {
    font-style: italic;
  }
</style>
