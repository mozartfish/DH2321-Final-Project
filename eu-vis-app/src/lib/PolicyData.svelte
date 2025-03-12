<script>
  import * as d3 from 'd3';

  const {
    policyData = [],
    selectedCountries = [],
    euCountries = [],
    year,
    sector
  } = $props();

  const sectorColors = {
    Agriculture: '#FEFFE0',
    'Energy consumption': '#FEE292',
    'Energy supply': '#FFC559',
    'Industrial processes': '#FCAA39',
    LULUCF: '#F5841E',
    'Other sectors': '#EE7B19',
    Transport: '#E1650F',
    Waste: '#CF5309'
  };

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
</script>

<section>
  <h2>{year} Policies</h2>
  {#if policyData.length > 0}
    {#if selectedCountries && selectedCountries.filter((c) => c !== 'EU').length > 0}
      <div class="policy-container">
        {#each selectedCountries.filter((c) => c !== 'EU') as country}
          <div class="country-group">
            <h3 class="country-title">{country}</h3>
            <ul>
              {#each policyData.filter((policy) => 
                policy.country === country &&
                parseInt(policy.year) === year &&
                (!sector || policy.sector.split(';').map(s => s.trim()).includes(sector))
              ) as policy}
                <li style="background-color: {sectorColors[policy.sector.split(';')[0].trim()]};">
                  <p>{policy.policy}</p>
                  <p class="sector">{policy.sector.replace(/;/g, ', ')}</p>
                </li>
              {/each}
            </ul>
          </div>
        {/each}
      </div>
    {:else}
      <div class="policy-container">
        {#each Array.from(
          new Set(
            policyData
              .filter((policy) => 
                parseInt(policy.year) === year &&
                policy.country !== 'EU' &&
                (!sector || policy.sector.split(';').map(s => s.trim()).includes(sector))
              )
              .map((policy) => policy.country)
          )
        ) as country}
          <div class="country-group">
            <h3 class="country-title">{country}</h3>
            <ul>
              {#each policyData.filter((policy) => 
                parseInt(policy.year) === year &&
                policy.country === country &&
                policy.country !== 'EU' &&
                (!sector || policy.sector.split(';').map(s => s.trim()).includes(sector))
              ) as policy}
                <li style="background-color: {sectorColors[policy.sector.split(';')[0].trim()]};">
                  <p>{policy.policy}</p>
                  <p class="sector">{policy.sector.replace(/;/g, ', ')}</p>
                </li>
              {/each}
            </ul>
          </div>
        {/each}
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
    background-color: white;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
    position: relative;
    border: 3px solid rgba(0, 0, 0, 0.8);
  }

  h2 {
    color: #094c93;
    margin-top: 10px;
  }

  .policy-container {
    padding: 10px;
    width: 100%;
  }

  .country-group {
    margin-bottom: 12px;
  }

  .country-title {
    font-size: 1.4em;
    margin-bottom: 10px;
    text-align: center;
    color: #094c93;
  }

  ul {
    list-style-type: none;
    padding: 0;
  }

  li {
    margin-bottom: 6px;
    border-radius: 6px;
    padding: 12px 10px;
    border: 3px solid rgba(0, 0, 0, 0.8);
  }

  .sector {
    font-style: italic;
  }
</style>