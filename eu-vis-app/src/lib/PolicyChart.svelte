<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';

  const { policyData = [], year = 2024 } = $props();

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
    Transport: '#2ca02c',
    'Industrial processes': '#a98467',
    Agriculture: '#adc178',
    LULUCF: '#8c564b',
    Waste: '#FDA286',
    'Other sectors': '#7f7f7f'
  };

  // Initialize the SVG element.
  onMount(() => {
    d3.select(svg).attr('width', width).attr('height', width);
  });

  // Function to build/update the full-circle pie chart.
  function updateChart() {
    // Filter data for the selected year.
    const filteredData = policyData.filter((d) => +d.year === year);

    // Compute counts per sector.
    const sectorCounts = new Map();
    filteredData.forEach((d) => {
      const sectorsList = d.sector.split(';').map((s) => s.trim());
      sectorsList.forEach((s) => {
        const count = sectorCounts.get(s) || 0;
        sectorCounts.set(s, count + 1);
      });
    });

    const sectorsData = Array.from(sectorCounts, ([name, value]) => ({
      name,
      value
    }));

    // Create a pie layout.
    const pie = d3
      .pie()
      .value((d) => d.value)
      .sort((a, b) => sectors.indexOf(a.name) - sectors.indexOf(b.name));
    const pieData = pie(sectorsData);

    const innerRadius = radius * 0.5;
    const outerRadius = radius;
    const arcGenerator = d3
      .arc()
      .innerRadius(innerRadius)
      .outerRadius(outerRadius);

    let container = d3.select(svg).select('g');
    if (container.empty()) {
      container = d3
        .select(svg)
        .append('g')
        .attr('transform', `translate(${width / 2}, ${width / 2})`);

      // Create the central label once.
      container
        .append('text')
        .attr('class', 'total')
        .attr('text-anchor', 'middle')
        .attr('dy', '0.35em')
        .style('font-size', '20px')
        .style('fill', 'black');
    }
    container.select('text.total').text(`Total: ${filteredData.length}`);

    const paths = container
      .selectAll('path.arc')
      .data(pieData, (d) => d.data.name);

    paths.exit().remove();

    paths
      .enter()
      .append('path')
      .attr('class', 'arc')
      .each(function (d) {
        this._current = d;
      })
      .style('fill', (d) => sectorColors[d.data.name])
      .on('mouseover', (event, d) => {
        d3.select(event.target)
          .transition()
          .duration(200)
          .attr(
            'd',
            d3
              .arc()
              .innerRadius(innerRadius)
              .outerRadius(outerRadius + 10)
          );
      })
      .on('mouseout', (event, d) => {
        d3.select(event.target)
          .transition()
          .duration(200)
          .attr(
            'd',
            d3.arc().innerRadius(innerRadius).outerRadius(outerRadius)
          );
      })
      .merge(paths)
      .transition()
      .duration(200)
      .attrTween('d', function (d) {
        const interpolate = d3.interpolate(this._current, d);
        this._current = interpolate(0);
        return (t) => arcGenerator(interpolate(t));
      });

    container
      .selectAll('text.label')
      .data(pieData, (d) => d.data.name)
      .join('text')
      .attr('class', 'label')
      .attr('transform', (d) => `translate(${arcGenerator.centroid(d)})`)
      .attr('text-anchor', 'middle')
      .attr('dy', '0.35em')
      .style('pointer-events', 'none')
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
  <svg bind:this={svg}></svg>
  <button>RESET??</button>
</section>

<style>
  button {
    margin-top: 20px;
    width: 200px;
    height: 50px;
    border: 2px solid black;
    box-shadow: 3px 3px 0px rgba(0, 0, 0, 1);
    border-radius: 10px;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 20px;
    cursor: pointer;
    transition-property: box-shadow, transform;
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

  path {
    cursor: pointer;
  }
</style>
