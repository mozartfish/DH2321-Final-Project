<!-- EUMap.svelte -->
<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';

  // props 
  let { countries, allCountriesData = [], onCountrySelect } = $props();

  // state variables
  let euGeoData;
  let colorScale;
  let width = 600;
  let height = 500;
  let selectedCountry = $state(null);
  let labelColor = $state('');

  // derived state for modifying data 
  let formattedData = $derived(
    allCountriesData.length > 0
      ? allCountriesData.map((countryData) => {
          return { country: countryData.country };
        })
      : []
  );

  // color scale generator - create color palette for all countries 
  const createCountryColorScale = () => {
    const countryNames = formattedData.map((d) => d.country);
    const colorRange = countryNames.map((d, i) =>
      d3.interpolateRainbow(i / countryNames.length)
    );
    return d3.scaleOrdinal().domain(countryNames).range(colorRange);
  };

// load and visualize all the map data when the map loads 
  onMount(async () => {
    const europeGeoJSON = await d3.json(
      'https://raw.githubusercontent.com/leakyMirror/map-of-europe/master/GeoJSON/europe.geojson'
    );

    // eu geographic data features
    euGeoData = {
      type: 'FeatureCollection',
      features: europeGeoJSON.features.filter((d) =>
        countries.includes(d.properties.NAME)
      )
    };

    colorScale = createCountryColorScale();
    drawMap();
  });

  // draw map 
  function drawMap() {
    const projection = d3.geoMercator().fitSize([width, height], euGeoData);
    const path = d3.geoPath().projection(projection);

    const svg = d3
      .select('#eu-map')
      .attr('width', width)
      .attr('height', height);

    // draw countries 
    svg
      .selectAll('path')
      .data(euGeoData.features)
      .enter()
      .append('path')
      .attr('d', path)
      .attr('fill', 'lightblue')
      .attr('stroke', 'white')
      .on('click', handleCountryClick);
  }

  // handle country click event
  function handleCountryClick(event, d) {
    const countryName = d.properties.NAME;
    const svg = d3.select('#eu-map');

    // reset all countries to a default color 
    svg.selectAll('path').attr('fill', 'lightblue');

    if (selectedCountry === countryName) {
      // deselect country if it is selected 
      selectedCountry = null;
      labelColor = '';
    } else {
      // select new country 
      selectedCountry = countryName;
      labelColor = colorScale(selectedCountry);
      d3.select(event.target).attr('fill', labelColor);
    }

    // apply callback if one is provided 
    if (onCountrySelect) {
      onCountrySelect(selectedCountry);
    }
  }
</script>

<section>
  <h3>EU Map Component</h3>
  <div>
    <h2 style="color: {labelColor}">
      {selectedCountry || ''}
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
