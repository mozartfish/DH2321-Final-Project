<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';

  let {
    countries,
    allCountriesData = [],
    onCountrySelect,
    selectedFile,
    year
  } = $props();

  let euGeoData;
  let width = 300;
  let height = 410;
  let selectedCountries = $state(['EU']);
  let lastSelectedCountry = $state('EU');
  let labelColor = $state('black');
  let selectedYear = $state('');

  // Global variables to hold projection and path for use in label placement.
  let projection;
  let path;

  // Update lastSelectedCountry and its color whenever the selection changes.
  $effect(() => {
    if (selectedCountries && selectedCountries.length > 0) {
      lastSelectedCountry = selectedCountries[selectedCountries.length - 1];
    } else {
      lastSelectedCountry = 'EU';
    }
    if (lastSelectedCountry !== 'EU') {
      const countryColorScale = createCountryColorScale();
      if (countryColorScale) {
        labelColor = countryColorScale(lastSelectedCountry);
      } else {
        labelColor = 'black';
      }
    } else {
      labelColor = '#094C93';
    }
  });

  $effect(() => {
    if (allCountriesData.length > 0) {
      const firstDataPoint = allCountriesData[0];
      const fields = Object.keys(firstDataPoint).filter(
        (key) => key !== 'country'
      );
      if (fields.length > 0) {
        if (year) {
          const exactYearMatch = fields.find((field) =>
            field.includes(year.toString())
          );
          selectedYear = exactYearMatch ? exactYearMatch : fields[0];
        } else {
          selectedYear = fields[0];
        }
      }
    }
  });

  function createHeatmapColorScale() {
    if (!allCountriesData || allCountriesData.length === 0 || !selectedYear)
      return null;
    const values = allCountriesData
      .map((d) => parseFloat(d[selectedYear]))
      .filter((val) => !isNaN(val));
    if (values.length === 0) return null;
    const dataMin = d3.min(values);
    const dataMax = d3.max(values);
    return d3
      .scaleSequential()
      .domain([dataMin, dataMax])
      .interpolator(d3.interpolateBlues);
  }

  function createCountryColorScale() {
    const countryNames = allCountriesData
      .map((d) => d.country)
      .filter((country) => country !== undefined);
    if (countryNames.length === 0) return null;
    const colorRange = countryNames.map((d, i) =>
      d3.interpolateRdPu(i / countryNames.length)
    );
    return d3.scaleOrdinal().domain(countryNames).range(colorRange);
  }

  function updateMapColors() {
    if (!euGeoData || !allCountriesData || allCountriesData.length === 0)
      return;
    const heatmapColorScale = createHeatmapColorScale();
    const countryColorScale = createCountryColorScale();
    if (!heatmapColorScale || !countryColorScale) return;
    const svg = d3.select('#eu-map');
    svg.selectAll('path').attr('fill', (d) => {
      const countryName = d.properties.NAME;
      if (selectedCountries.includes(countryName)) {
        return countryColorScale(countryName);
      }
      const countryData = allCountriesData.find(
        (item) => item.country === countryName
      );
      if (countryData) {
        const value = parseFloat(countryData[selectedYear]);
        return !isNaN(value) ? heatmapColorScale(value) : '#ccc';
      }
      return '#DFDFDF';
    });

    // Remove any previous labels.
    svg.selectAll('.country-label').remove();

    // Add a text label on each selected country.
    selectedCountries.forEach((countryName) => {
      const feature = euGeoData.features.find(
        (f) => f.properties.NAME === countryName
      );
      if (feature) {
        const centroid = path.centroid(feature);
        svg
          .append('text')
          .attr('class', 'country-label')
          .attr('x', centroid[0])
          .attr('y', centroid[1])
          .attr('text-anchor', 'middle')
          .attr('dy', '.35em')
          .text(countryName)
          .style('font-size', '14px')
          .style('fill', 'black')
          .style('pointer-events', 'none');
      }
    });

    createLegend(heatmapColorScale);
    console.log('Selected countries:', selectedCountries);
  }

  function createLegend(colorScale) {
    if (!colorScale) return;
    const domain = colorScale.domain();
    const legendWidth = 100;
    const legendHeight = 20;
    d3.select('#legend-container').selectAll('*').remove();
    const legend = d3
      .select('#legend-container')
      .append('svg')
      .attr('width', legendWidth + 50)
      .attr('height', legendHeight + 30);
    const defs = legend.append('defs');
    const gradient = defs
      .append('linearGradient')
      .attr('id', 'legend-gradient')
      .attr('x1', '0%')
      .attr('x2', '100%')
      .attr('y1', '0%')
      .attr('y2', '0%');
    for (let i = 0; i <= 10; i++) {
      const t = i / 10;
      const value = domain[0] + t * (domain[1] - domain[0]);
      gradient
        .append('stop')
        .attr('offset', `${t * 100}%`)
        .attr('stop-color', colorScale(value));
    }
    legend
      .append('rect')
      .attr('x', 0)
      .attr('y', 10)
      .attr('width', legendWidth)
      .attr('height', legendHeight)
      .style('fill', 'url(#legend-gradient)');
    legend
      .append('text')
      .attr('x', 0)
      .attr('y', legendHeight + 25)
      .style('text-anchor', 'start')
      .style('font-size', '12px')
      .text(domain[0].toFixed(1));
    legend
      .append('text')
      .attr('x', 0 + legendWidth)
      .attr('y', legendHeight + 25)
      .style('text-anchor', 'end')
      .style('font-size', '12px')
      .text(domain[1].toFixed(1));
  }

  onMount(async () => {
    const europeGeoJSON = await d3.json(
      'https://raw.githubusercontent.com/leakyMirror/map-of-europe/master/GeoJSON/europe.geojson'
    );
    euGeoData = {
      type: 'FeatureCollection',
      features: europeGeoJSON.features.filter((d) =>
        countries.includes(d.properties.NAME)
      )
    };
    drawMap();
  });

  function drawMap() {
    projection = d3.geoMercator().fitSize([width, height], euGeoData);
    path = d3.geoPath().projection(projection);
    const svg = d3
      .select('#eu-map')
      .attr('width', width)
      .attr('height', height);

    svg
      .selectAll('path')
      .data(euGeoData.features)
      .enter()
      .append('path')
      .attr('d', path)
      .attr('fill', 'green')
      .attr('stroke', 'black')
      .attr('stroke-width', 0.4)
      .style('cursor', 'pointer')
      .on('click', handleCountryClick)
      .on('mouseover', handleCountryHover)
      .on('mouseout', handleCountryHoverOut);

    updateMapColors();
  }

  function handleCountryHover(event, d) {
    const svg = d3.select('#eu-map');
    // Remove any existing hover labels
    svg.selectAll('.hover-label').remove();
    const feature = d;
    const countryName = feature.properties.NAME;
    if (feature) {
      const centroid = path.centroid(feature);
      svg
        .append('text')
        .attr('class', 'hover-label')
        .attr('x', centroid[0])
        .attr('y', centroid[1])
        .attr('text-anchor', 'middle')
        .attr('dy', '.35em')
        .text(countryName)
        .style('font-size', '14px')
        .style('fill', 'black')
        .style('pointer-events', 'none');
    }
  }

  function handleCountryHoverOut(event, d) {
    const svg = d3.select('#eu-map');
    svg.selectAll('.hover-label').remove();
  }

  function handleCountryClick(event, d) {
    event.stopPropagation();
    const countryName = d.properties.NAME;
    if (selectedCountries.includes(countryName)) {
      selectedCountries = selectedCountries.filter((c) => c !== countryName);
    } else {
      selectedCountries = [...selectedCountries, countryName];
    }
    updateMapColors();
    if (onCountrySelect) onCountrySelect(selectedCountries);
  }

  function resetSelection() {
    selectedCountries = ['EU'];
    updateMapColors();
    if (onCountrySelect) onCountrySelect(selectedCountries);
  }

  $effect(() => {
    console.log('Effect triggered: Data or selection changed');
    console.log('Selected file:', selectedFile);
    console.log('Data rows:', allCountriesData.length);
    console.log('Selected field:', selectedYear);
    console.log('Current year:', year);
    if (euGeoData) {
      updateMapColors();
    }
  });
</script>

<section>
  <h2>Heatmap for {selectedFile}</h2>
  <!-- <h3>Heatmap for dataset: {selectedFile}</h3> -->
  <div id="map-container">
    <h3 style="color: {labelColor}">{lastSelectedCountry}</h3>
    <svg id="eu-map"></svg>
    <div id="legend-container"></div>
  </div>
  <button onclick={resetSelection}>RESET</button>
</section>

<style>
  section {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    border-radius: 10px;
    border: 3px solid rgba(0, 0, 0, 0.8);
    background-color: white;
    position: relative;
  }

  h2 {
    color: #094c93;
    position: absolute;
    top: 10px;
  }

  #map-container {
    position: relative;
    padding-bottom: 15px;
  }

  h3 {
    font-size: 40px;
    white-space: nowrap;
    position: absolute;
    top: 20px;
    left: 0px;
  }

  #legend-container {
    position: absolute;
    top: 70px;
    left: 0;
  }

  button {
    width: 200px;
    height: 50px;
    background: #c4ddee;
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

  #eu-map {
    padding-top: 10px;
  }
</style>
