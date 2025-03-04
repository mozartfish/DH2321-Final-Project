<!-- EUMap.svelte -->
<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';

  // Props declaration with callback
<<<<<<< HEAD
  let { 
    countries,
    onCountrySelect  // New callback prop instead of event dispatcher
  } = $props();
  
  let width = 600;
  let height = 500;
  let selectedCountry = $state('');
=======
  let { countries, allCountriesData = [], onCountrySelect } = $props();

  let colorScale;
  let labelColor = $state('');

  // derive a new dataset for updating the UI based on the data passed in
  let formattedData = $derived(
    allCountriesData.length > 0
      ? allCountriesData.map((countryData) => {
          // import country data
          const country = countryData.country;
          // return new country object
          return {
            country
          };
        })
      : []
  );

  // Scales
  // country color scale - there are 28 unique countries (EU countries + EU)
  const countryColorScale = () => {
    const countries = formattedData.map((d) => d.country);
    const colorRange = countries.map((d, i) =>
      d3.interpolateRainbow(i / countries.length)
    );
    return d3.scaleOrdinal().domain(countries).range(colorRange);
  };

  let width = 600;
  let height = 500;
  let selectedCountry = $state(null);
>>>>>>> d25cbb8 (finish and finalize line chart without tooltips)
  let geoData;

  onMount(async () => {
    // Fetch Europe GeoJSON data
    const europeGeoJSON = await d3.json(
      'https://raw.githubusercontent.com/leakyMirror/map-of-europe/master/GeoJSON/europe.geojson'
    );
    // Include only EU countries
    geoData = {
      type: 'FeatureCollection',
      features: europeGeoJSON.features.filter((d) =>
        countries.includes(d.properties.NAME)
      )
    };
    console.log('the geo data: ', geoData);
    colorScale = countryColorScale();
    drawMap();
  });

  function drawMap() {
    const projection = d3.geoMercator().fitSize([width, height], geoData);
    const path = d3.geoPath().projection(projection);
    const svg = d3
      .select('#eu-map')
      .attr('width', width)
      .attr('height', height);

    svg
      .selectAll('path')
      .data(geoData.features)
      .enter()
      .append('path')
      .attr('d', path)
      .attr('fill', 'lightblue')
      .attr('stroke', 'white')
      .on('click', (event, d) => {
<<<<<<< HEAD
        svg.selectAll('path').attr('fill', 'lightblue');
        d3.select(event.target).attr('fill', 'peachpuff');
        selectedCountry = d.properties.NAME;
        
        // Use callback instead of dispatch
        if (onCountrySelect) {
          onCountrySelect({ country: selectedCountry });
        }
        
=======
        const countryName = d.properties.NAME;
        // initialize country colors as blue 
        svg.selectAll('path').attr('fill', 'lightblue');
        if (selectedCountry === countryName) {
          // deselect country if it has already been selected 
          selectedCountry = null;
          labelColor = '';
        } else {
          // select new country 
          selectedCountry = countryName;
          const countryColor = colorScale(selectedCountry);
          labelColor = countryColor;
          d3.select(event.target).attr('fill', countryColor);
        }
        // call callback function if one is passed
        if (onCountrySelect) {
          onCountrySelect(selectedCountry);
        }

>>>>>>> d25cbb8 (finish and finalize line chart without tooltips)
        console.log(selectedCountry);
      });
  }
</script>

<section>
  <h3>EU Map Component</h3>
  <div>
<<<<<<< HEAD
    <h2>
      {selectedCountry}
=======
    <h2 style="color: {labelColor}">
      {selectedCountry || ''}
>>>>>>> d25cbb8 (finish and finalize line chart without tooltips)
    </h2>
    <svg id="eu-map"></svg>
  </div>
</section>

<style>
  div {
    position: relative;
    height: 530px;
  }
  h2 {
    font-size: 40px;
    white-space: nowrap;
    position: absolute;
    top: 0;
    right: 0;
  }
  #eu-map {
    padding-top: 50px;
    overflow: visible;
  }
</style>