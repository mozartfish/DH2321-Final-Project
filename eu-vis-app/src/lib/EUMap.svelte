<script>
    import { onMount } from 'svelte';
    import * as d3 from 'd3';
  
    let width = 800;
    let height = 600;
    let { countries } = $props();
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
        .attr('height', height
        );

        const countryText = svg.append('text')
            .attr('id', 'selected-country')
            .attr('x', width - 10)
            .attr('y', 30)
            .attr('text-anchor', 'end')
            .attr('font-size', '40px')
            .text('');


  
      svg.selectAll('path')
        .data(geoData.features)
        .enter()
        .append('path')
        .attr('d', path)
        .attr('fill', '#ccc')
        .attr('stroke', 'white')
        .on('click', (event, d) => {
            svg.selectAll('path').attr('fill', '#ccc');
            d3.select(event.target).attr('fill', 'peachpuff');
            countryText.text(d.properties.NAME);
            console.log(d.properties.NAME);
        });
    }
</script>

<h3>
EU Map Component
</h3>
<svg id="eu-map"></svg>