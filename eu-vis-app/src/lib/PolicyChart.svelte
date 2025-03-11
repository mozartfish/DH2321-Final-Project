<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';

  const { policyData = [], year } = $props();

  let width = 330;
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

  // const sectorColors = {
  //   'Energy consumption': '#FEFFE0',
  //   'Energy supply': '#FEE292',
  //   Transport: '#FFC559',
  //   'Industrial processes': '#FCAA39',
  //   Agriculture: '#F5841E',
  //   LULUCF: '#EE7B19',
  //   Waste: '#E1650F',
  //   'Other sectors': '#CF5309'
  // };

  const sectorColors = {
    Agriculture: '#FEFFE0',
    'Energy consumption': '#FEE292',
    'Energy supply': '#FFC559',
    'Industrial processes': '#FCAA39',
    LULUCF: '#F5841E',
    'Other sectors': '#EE7B19',
    Transport: '#E1650F',
    Waste: '#CF5309',
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
      .sort((a, b) => a.name.localeCompare(b.name));
    const pieData = pie(sectorsData);

    const innerRadius = radius * 0.5;
    const outerRadius = radius;
    const arcGenerator = d3
      .arc()
      .innerRadius(innerRadius)
      .outerRadius(outerRadius);

    // Add title to the SVG
    /*
    let titleText = d3.select(svg).select('text.chart-title');
    if (titleText.empty()) {
      titleText = d3
        .select(svg)
        .append('text')
        .attr('class', 'chart-title')
        .attr('x', width / 2 + 7)
        .attr('y', 35)
        .attr('text-anchor', 'middle')
        .style('font-size', '24px')
        .style('font-weight', 'bold')
        .text('Policies implemented in ' + year);
    } else {
      titleText.text('Policies implemented in ' + year);
    }
    */

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

      // Total label
      centerGroup
        .append('text')
        .attr('class', 'center-name')
        .attr('y', -20)
        .style('font-size', '16px')
        .style('fill', 'black')
        .text('Total');

      // Number of policies
      centerGroup
        .append('text')
        .attr('class', 'center-value')
        .attr('y', 32)
        .style('font-size', '62px')
        .style('fill', 'black')
        .text(filteredData.length);
    } else {
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
        const offset = -5;
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
              .style('font-size', '16px');
            d3.select(this)
              .select('text.center-value')
              .text(d.data.value)
              .style('font-size', '62px');
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
            .style('font-size', '16px')
            .style('fill', (d) => d3.color(sectorColors[d.data.name]).darker())
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
  <h2>Policies in {year}</h2>
  <svg bind:this={svg}></svg>
</section>

<style>
  section {
    width: 100%;
    height: 100%;
    border-radius: 10px;
    border: 3px solid rgba(0, 0, 0, 0.8);
    background-color: white;
    padding-top: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    text-align: center;
  }

  h2 {
    color: #094c93;
    position: absolute;
    top: 10px;
  }

  svg {
    overflow: visible;
  }

  path {
    cursor: pointer;
  }
</style>
