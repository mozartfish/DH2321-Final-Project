<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';

  let width = 600;
  let height = 500;
  let { countries } = $props();
  let geoData;
  let selectedCountry = $state('');

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
        svg.selectAll('path').attr('fill', 'lightblue');
        d3.select(event.target).attr('fill', 'peachpuff');
        selectedCountry = d.properties.NAME;
        console.log(selectedCountry);
      });
  }
</script>

<section>
  <h3>EU Map Component</h3>
  <div>
    <h2>
      {selectedCountry}
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
    color: peachpuff;
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
