<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';

  // Props
  let {
    countries,
    allCountriesData = [],
    onCountrySelect,
    selectedFile,
    year
  } = $props();

  // State variables
  let euGeoData;
  let width = 400;
  let height = 500;
  let selectedCountry = $state(null);
  let labelColor = $state('');
  let selectedYear = $state('');

  // update selected year when the year slider changes
  $effect(() => {
    if (allCountriesData.length > 0) {
      const firstDataPoint = allCountriesData[0];
      const fields = Object.keys(firstDataPoint).filter(
        (key) => key !== 'country'
      );

      // check year prop to make sure it is valid
      if (fields.length > 0) {
        if (year) {
          const exactYearMatch = fields.find((field) =>
            field.includes(year.toString())
          );
          if (exactYearMatch) {
            selectedYear = exactYearMatch;
          } else {
            selectedYear = fields[0];
          }
        } else {
          selectedYear = fields[0];
        }
      }
    }
  });

  // scale for the heatmap
  function createHeatmapColorScale() {
    if (!allCountriesData || allCountriesData.length === 0 || !selectedYear)
      return null;

    const values = allCountriesData
      .map((d) => parseFloat(d[selectedYear]))
      .filter((val) => !isNaN(val));

    if (values.length === 0) return null;

    // Get the minValue and max values for the scale domain
    const dataMin = d3.min(values);
    const dataMax = d3.max(values);

    return d3
      .scaleSequential()
      .domain([dataMin, dataMax])
      .interpolator(d3.interpolateGreys);
      //.interpolator(d3.interpolateBlues);
  }

  function createCountryColorScale() {
    const countryNames = allCountriesData
      .map((d) => d.country)
      .filter((country) => country !== undefined);
    if (countryNames.length === 0) return null;

    const colorRange = countryNames.map((d, i) =>
      d3.interpolateRainbow(i / countryNames.length)
    );

    return d3.scaleOrdinal().domain(countryNames).range(colorRange);
  }

  // update map color scales
  function updateMapColors() {
    if (!euGeoData || !allCountriesData || allCountriesData.length === 0)
      return;

    const heatmapColorScale = createHeatmapColorScale();
    const countryColorScale = createCountryColorScale();

    if (!heatmapColorScale || !countryColorScale) return;

    const svg = d3.select('#eu-map');
    svg.selectAll('path').attr('fill', (d) => {
      const countryName = d.properties.NAME;
      if (selectedCountry === countryName) {
        return countryColorScale(countryName);
      }
      const countryData = allCountriesData.find(
        (item) => item.country === countryName
      );
      if (countryData) {
        const value = parseFloat(countryData[selectedYear]);
        return !isNaN(value) ? heatmapColorScale(value) : '#ccc';
      }
      return '#F04A00'; // Default color for countries without data
    });

    createLegend(heatmapColorScale);
  }

  // heatmap legend
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

    // legend gradient
    const defs = legend.append('defs');
    const gradient = defs
      .append('linearGradient')
      .attr('id', 'legend-gradient')
      .attr('x1', '0%')
      .attr('x2', '100%')
      .attr('y1', '0%')
      .attr('y2', '0%');

    // Add color stops to gradient
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
      .attr('x', 10)
      .attr('y', 10)
      .attr('width', legendWidth)
      .attr('height', legendHeight)
      .style('fill', 'url(#legend-gradient)');

    legend
      .append('text')
      .attr('x', 10)
      .attr('y', legendHeight + 25)
      .style('text-anchor', 'start')
      .style('font-size', '12px')
      .text(domain[0].toFixed(1));

    legend
      .append('text')
      .attr('x', 10 + legendWidth)
      .attr('y', legendHeight + 25)
      .style('text-anchor', 'end')
      .style('font-size', '12px')
      .text(domain[1].toFixed(1));
  }

  // load and visualize map data
  onMount(async () => {
    const europeGeoJSON = await d3.json(
      'https://raw.githubusercontent.com/leakyMirror/map-of-europe/master/GeoJSON/europe.geojson'
    );

    // Filter eu data geography
    euGeoData = {
      type: 'FeatureCollection',
      features: europeGeoJSON.features.filter((d) =>
        countries.includes(d.properties.NAME)
      )
    };

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
      .attr('fill', 'green')
      .attr('stroke', 'black')
      .attr('stroke-width', 0.4)
      .on('click', handleCountryClick);

    // apply color scales
    updateMapColors();
  }

  // handle country selection event
  function handleCountryClick(event, d) {
    const countryName = d.properties.NAME;

    if (selectedCountry === countryName) {
      // deselect country if it is selected
      selectedCountry = null;
      labelColor = '';
    } else {
      // select new country
      selectedCountry = countryName;

      // apply color scale to selected country
      const countryColorScale = createCountryColorScale();
      if (countryColorScale) {
        labelColor = countryColorScale(countryName);
      }
    }

    // Update map colors to reflect the new selection
    updateMapColors();

    // if callback provided, call the callback function
    if (onCountrySelect) {
      onCountrySelect(selectedCountry);
    }
  }

  // for debugging
  $effect(() => {
    console.log('Effect triggered: Data or selection changed');
    console.log('Selected file:', selectedFile);
    console.log('Data rows:', allCountriesData.length);
    console.log('Selected field:', selectedYear);
    console.log('Current year:', year);

    // update the map if eu data changes
    if (euGeoData) {
      updateMapColors();
    }
  });
</script>

<section>
  <h3>Heatmap for dataset: {selectedFile}</h3>

  <div class="map-container">
    <h2 style="color: {labelColor}">
      {selectedCountry || 'EU'}
    </h2>
    <svg id="eu-map"></svg>
    <div id="legend-container"></div>
  </div>
</section>

<style>
  .map-container {
    position: relative;
    height: 530px;
  }

  h2 {
    font-size: 40px;
    white-space: nowrap;
    position: absolute;
    top: 20px;
    left: 0;
  }

  #eu-map {
    padding-top: 50px;
    overflow: visible;
  }

  #legend-container {
    position: absolute;
    top: 70px;
    left: 0;
  }
</style>
