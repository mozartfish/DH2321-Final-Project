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
    'Energy consumption': '#240490',
    'Energy supply': '#5E01A7',
    Transport: '#98159F',
    'Industrial processes': '#DE5F64',
    Agriculture: '#EE7D51',
    LULUCF: '#FA963E',
    Waste: '#FDB42E',
    'Other sectors': '#F4E926'
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
        .attr('y', -22)
        .style('font-size', '18px')
        .style('fill', 'black')
        .text('Total');

      // Number of policies
      centerGroup
        .append('text')
        .attr('class', 'center-value')
        .attr('y', 25)
        .style('font-size', '50px')
        .style('fill', 'black')
        .text(filteredData.length);

      // // Policies label
      // centerGroup
      //   .append('text')
      //   .attr('class', 'center-text')
      //   .attr('y', 33)
      //   .style('font-size', '18px')
      //   .style('fill', 'black')
      //   .text('policies');

      // // Year label
      // centerGroup
      //   .append('text')
      //   .attr('class', 'center-year')
      //   .attr('y', 55)
      //   .style('font-size', '18px')
      //   .style('fill', 'black')
      //   .text('in ' + year);
    } else {
      // Update the overall total (an dthe year) if needed.
      d3.select(svg)
        .select('g.center-text')
        .select('text.center-value')
        .text(filteredData.length);

      // d3.select(svg)
      //   .select('g.center-text')
      //   .select('text.center-year')
      //   .text('in ' + year);
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
            .style('stroke', 'black')
            .style('stroke-width', 0.1)
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
    border-radius: 10px;
    border: 3px solid rgba(0, 0, 0, 0.8);
    padding-top: 4px;
    padding-bottom: 4px;
    align-items: stretch;
    background-color: white;
    display: flex;
    flex-direction: column;
    position: relative;
    text-align: center;
  }

  svg {
    width: 100%; /* Make SVG take full width of container */
    height: 100%;
    max-width: 100%; /* Ensure it doesn't overflow */
    padding: 20px;
  }

  path {
    cursor: pointer;
  }
</style>
