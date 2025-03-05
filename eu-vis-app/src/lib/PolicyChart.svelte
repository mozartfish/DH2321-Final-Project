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

  const sectorColors = {
    'Energy consumption': '#2C3E50',
    'Energy supply': '#E74C3C',
    Transport: '#2980B9',
    'Industrial processes': '#F39C12',
    Agriculture: '#27AE60',
    LULUCF: '#145A32',
    Waste: '#9B59B6',
    'Other sectors': '#7F8C8D'
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
      .join(
        (enter) =>
          enter
            .append('text')
            .attr('class', 'label')
            .attr('text-anchor', 'middle')
            .attr('dy', '0.35em')
            .style('pointer-events', 'none')
            .style('font-size', '12px')
            .style('fill', '#fff')
            .attr('transform', (d) => `translate(${arcGenerator.centroid(d)})`)
            .text((d) => d.data.name),
        (update) =>
          update
            .transition()
            .duration(200)
            .attrTween('transform', function (d) {
              const previous = d3.select(this).attr('transform');
              const current = `translate(${arcGenerator.centroid(d)})`;
              return d3.interpolateTransformSvg(previous, current);
            })
            .text((d) => d.data.name),
        (exit) => exit.remove()
      );

    // Ensure that text labels are on top of the arcs.
    container.selectAll('text.label').raise();
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
