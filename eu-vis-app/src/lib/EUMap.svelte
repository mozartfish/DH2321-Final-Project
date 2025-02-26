<script>
    import { onMount } from 'svelte';
    import * as d3 from 'd3';
  
    let width = 800;
    let height = 600;
    export let countries = [];
    let geoData;
  
    onMount(async () => {
      // Fetch GeoJSON data for Europe
      const europeGeoJSON = await d3.json(
        'https://raw.githubusercontent.com/leakyMirror/map-of-europe/master/GeoJSON/europe.geojson'
      );
      // Filter the features to include only EU countries
      geoData = {
        type: "FeatureCollection",
        features: europeGeoJSON.features.filter(d => countries.includes(d.properties.NAME))
      };
      drawMap();
    });
  
    function drawMap() {
      const projection = d3.geoMercator()
        .fitSize([width, height], geoData);
      const path = d3.geoPath().projection(projection);
  
      const svg = d3.select('#eu-map')
        .attr('width', width)
        .attr('height', height);
  
      svg.selectAll('path')
        .data(geoData.features)
        .enter()
        .append('path')
        .attr('d', path)
        .attr('fill', '#ccc')
        .attr('stroke', '#333')
        .on('click', (event, d) => {
            svg.selectAll('path').attr('fill', '#ccc');
            d3.select(event.target).attr('fill', 'orange');
            console.log(d.properties.NAME);
        });
    }
  </script>
  
  <svg id="eu-map"></svg>
  
  <style>
    svg {
      border: 1px solid #aaa;
    }
  </style>