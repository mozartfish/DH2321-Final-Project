<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';

  let { policyData = [], year, sector = $bindable() } = $props();

  let width = 240;
  let radius = width / 2;
  let svg;

  const sectorColors = {
    Agriculture: '#FEFFE0',
    'Energy consumption': '#FEE292',
    'Energy supply': '#FFC559',
    'Industrial processes': '#FCAA39',
    LULUCF: '#F5841E',
    'Other sectors': '#EE7B19',
    Transport: '#E1650F',
    Waste: '#CF5309'
  };

  onMount(() => {
    d3.select(svg).attr('width', width).attr('height', width);
  });

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

    // Create pie layout.
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

    // Create or select container group.
    let container = d3.select(svg).select('g');
    if (container.empty()) {
      container = d3
        .select(svg)
        .append('g')
        .attr('transform', `translate(${width / 2}, ${width / 2})`);

      const centerGroup = container
        .append('g')
        .attr('class', 'center-text')
        .attr('text-anchor', 'middle');

      if (sector) {
        const selectedData = pieData.find((p) => p.data.name === sector);
        centerGroup
          .append('text')
          .attr('class', 'center-name')
          .attr('y', -20)
          .style('font-size', '16px')
          .style('fill', 'black')
          .text(sector);
        centerGroup
          .append('text')
          .attr('class', 'center-value')
          .attr('y', 32)
          .style('font-size', '62px')
          .style('fill', 'black')
          .text(selectedData ? selectedData.data.value : 0);
      } else {
        centerGroup
          .append('text')
          .attr('class', 'center-name')
          .attr('y', -20)
          .style('font-size', '16px')
          .style('fill', 'black')
          .text('Total');
        centerGroup
          .append('text')
          .attr('class', 'center-value')
          .attr('y', 32)
          .style('font-size', '62px')
          .style('fill', 'black')
          .text(filteredData.length);
      }
    } else {
      const centerGroup = d3.select(svg).select('g.center-text');
      if (sector) {
        const selectedData = pieData.find((p) => p.data.name === sector);
        centerGroup.select('text.center-name').text(sector);
        centerGroup
          .select('text.center-value')
          .text(selectedData ? selectedData.data.value : 0);
      } else {
        centerGroup.select('text.center-name').text('Total');
        centerGroup.select('text.center-value').text(filteredData.length);
      }
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
        const offset = -5;
        const angle = (d.startAngle + d.endAngle) / 2;
        const translateX = Math.sin(angle) * offset;
        const translateY = -Math.cos(angle) * offset;
        d3.select(this)
          .transition()
          .duration(200)
          .attr('transform', `translate(${translateX}, ${translateY})`);

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

        if (sector == d.data.name) {
          return;
        }
        const centerGroup = container.select('g.center-text');
        centerGroup
          .transition()
          .duration(150)
          .style('opacity', 0)
          .on('end', function () {
            if (sector) {
              const selectedData = pieData.find((p) => p.data.name === sector);
              d3.select(this).select('text.center-name').text(sector);
              d3.select(this)
                .select('text.center-value')
                .text(selectedData ? selectedData.data.value : 0);
            } else {
              d3.select(this).select('text.center-name').text('Total');
              d3.select(this)
                .select('text.center-value')
                .text(filteredData.length);
            }
            d3.select(this).transition().duration(200).style('opacity', 1);
          });
      })
      .on('click', function (event, d) {
        sector = d.data.name;
        console.log('Sector selected:', sector);
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

    container.selectAll('text.label').raise();
  }

  function resetSelection() {
    sector = null;
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
  <button onclick={resetSelection}>RESET</button>
</section>

<style>
  section {
    width: 100%;
    height: 100%;
    border-radius: 10px;
    border: 3px solid rgba(0, 0, 0, 0.8);
    background-color: white;
    padding-top: 30px;
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

  button {
    width: 150px;
    height: 45px;
    margin-top: 10px;
    background: #feebb8;
    border: 2px solid black;
    box-shadow: 3px 3px 0px rgba(0, 0, 0, 1);
    border-radius: 10px;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 20px;
    cursor: pointer;
    transition-property: box-shadow, transform, background-color;
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
</style>
