<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';

  const { policyData = [] } = $props();
  let year = 2024;

  let width = 500;
  let radius = width / 2;
  // Remove the existing color scheme variable if not used.
  // let colors = d3.schemeCategory10;
  let svg;

  // sector names
  let sectors = [
    'Energy consumption',
    'Energy supply',
    'Transport',
    'Industrial processes',
    'Agriculture',
    'LULUCF',
    'Waste',
    'Other sectors'
  ];

  // Map each sector to a specific color.
  const sectorColors = {
    'Energy consumption': '#C197F3',
    'Energy supply': '#ff7f0e',
    'Transport': '#2ca02c',
    'Industrial processes': '#a98467',
    'Agriculture': '#adc178',
    'LULUCF': '#8c564b',
    'Waste': '#FDA286',
    'Other sectors': '#7f7f7f'
  };

  // Initialize the SVG element.
  onMount(() => {
    d3.select(svg).attr('width', width).attr('height', width);
  });

  // Function to build/update the full-circle pie chart.
  function updateChart() {
    // Clear any previous chart content.
    d3.select(svg).selectAll('*').remove();

    // Filter policyData for the selected year.
    const filteredData = policyData.filter((d) => +d.year === year);

    // Compute counts per sector.
    const sectorCounts = new Map();
    filteredData.forEach((d) => {
      const sectors = d.sector.split(';').map((s) => s.trim());
      sectors.forEach((s) => {
        const count = sectorCounts.get(s) || 0;
        sectorCounts.set(s, count + 1);
      });
    });

    // Create an array with each sector's name and policy count.
    const sectorsData = Array.from(sectorCounts, ([name, value]) => ({
      name,
      value
    }));

    // Create a pie layout for a full circle.
    const pie = d3
      .pie()
      .value((d) => d.value)
      .sort(null);

    const pieData = pie(sectorsData);

    // Define inner and outer radii for a donut chart.
    const innerRadius = radius * 0.3;
    const outerRadius = radius;

    // Define the arc generator.
    const arc = d3.arc().innerRadius(innerRadius).outerRadius(outerRadius);

    // Create a container group and center the chart.
    const container = d3
      .select(svg)
      .append('g')
      .attr('transform', `translate(${width / 2}, ${width / 2})`);

    // Append a centered label for the current year.
    container
      .append('text')
      .attr('text-anchor', 'middle')
      .attr('dy', '0.35em')
      .style('font-size', '52px')
      .style('fill', 'white')
      .text(filteredData.length);

    // Draw the arcs for each sector using the specific sector colors.
    container
      .selectAll('path')
      .data(pieData)
      .enter()
      .append('path')
      .attr('d', arc)
      .style('fill', (d) => sectorColors[d.data.name])
      .style('stroke', '#fff')
      .on('mouseover', (event, d) => {
        console.log(`${d.data.name}: ${d.data.value}`);
      });

    // Append sector names at the centroid of each arc.
    container
      .selectAll('text.label')
      .data(pieData)
      .enter()
      .append('text')
      .attr('class', 'label')
      .attr('transform', (d) => `translate(${arc.centroid(d)})`)
      .attr('text-anchor', 'middle')
      .attr('dy', '0.35em')
      .style('font-size', '12px')
      .style('fill', '#fff')
      .text((d) => d.data.name);
  }

  // Use $effect to run the chart update whenever policyData changes.
  $effect(() => {
    if (policyData && policyData.length) {
      updateChart();
    }
  });

  $effect(() => {
    console.log('POLICIES policyData: ', policyData);
    console.log('POLICIES year: ', year);
  });
</script>

<section>
  <h3>Pie Chart Policies</h3>
  <div id="chart">
    <svg bind:this={svg}></svg>
  </div>
  <div id="legend"></div>
</section>

<style>
  #chart {
    background-color: #303F4A;
    box-shadow: 0 5px 10px #303F4A;
    border-radius: 100%;
    padding: 30px;
  }

  #legend {
    margin-top: 20px;
    width: 200px;
    height: 50px;
    background-color: rgb(255, 0, 255);
    border-radius: 100px;
    box-shadow: 0 5px 10px rgba(255, 0, 255, 0.7);
  }

  path {
    cursor: pointer;
  }
</style>
