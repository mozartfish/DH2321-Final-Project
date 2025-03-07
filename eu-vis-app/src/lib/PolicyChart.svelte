<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';

  const { policyData = [], year } = $props();

  let width = 300;
  let radius = width / 2;
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

    // Select or create container group.
    let container = d3.select(svg).select('g');
    if (container.empty()) {
      container = d3
        .select(svg)
        .append('g')
        .attr('transform', `translate(${width / 2}, ${width / 2})`);

      // Create the central text group.
      const centerGroup = container
        .append('g')
        .attr('class', 'center-text')
        .attr('text-anchor', 'middle');

      centerGroup
        .append('text')
        .attr('class', 'center-name')
        .attr('y', -27)
        .style('font-size', '18px')
        .style('fill', 'black')
        .text('Total');

      centerGroup
        .append('text')
        .attr('class', 'center-value')
        .attr('y', 19)
        .style('font-size', '50px')
        .style('fill', 'black')
        .text(filteredData.length);

      centerGroup
        .append('text')
        .attr('class', 'center-text')
        .attr('y', 42)
        .style('font-size', '18px')
        .style('fill', 'black')
        .text('policies');
    } else {
      // Update the overall total if needed.
      d3.select(svg)
        .select('g.center-text')
        .select('text.center-value')
        .text(filteredData.length);
    }

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
      .on('mouseover', function (event, d) {
        // Pull the arc outward.
        const offset = -10;
        const angle = (d.startAngle + d.endAngle) / 2;
        const translateX = Math.sin(angle) * offset;
        const translateY = -Math.cos(angle) * offset;
        d3.select(this)
          .transition()
          .duration(200)
          .attr('transform', `translate(${translateX}, ${translateY})`);

        // Update the center text with hovered sector details.
        const centerGroup = container.select('g.center-text');
        centerGroup
          .transition()
          .duration(200)
          .style('opacity', 0)
          .on('end', function () {
            d3.select(this)
              .select('text.center-name')
              .text(d.data.name)
              .style('font-size', '14px');
            d3.select(this)
              .select('text.center-value')
              .text(d.data.value)
              .style('font-size', '50px');
            d3.select(this).transition().duration(100).style('opacity', 1);
          });
      })
      .on('mouseout', function (event, d) {
        d3.select(this)
          .transition()
          .duration(200)
          .attr('transform', 'translate(0,0)');

        // Revert the center text to show the overall total.
        const centerGroup = container.select('g.center-text');
        centerGroup
          .transition()
          .duration(150)
          .style('opacity', 0)
          .on('end', function () {
            d3.select(this).select('text.center-name').text('Total');
            d3.select(this)
              .select('text.center-value')
              .text(filteredData.length);
            d3.select(this).transition().duration(200).style('opacity', 1);
          });
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

    // Bring labels to the front.
    container.selectAll('text.label').raise();
  }

  $effect(() => {
    if (policyData && policyData.length) {
      updateChart();
    }
  });
</script>

<section>
  <svg bind:this={svg}></svg>
  <!-- <button>RESET??</button> -->
</section>

<style>
  section {
    width: 100%;
    border-radius: 10px;
    border: 3px solid rgba(0, 0, 0, 0.8);
    padding: 40px;
    align-items: stretch;
    background-color: white;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }

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
