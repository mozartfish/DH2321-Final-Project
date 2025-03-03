<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';

  export let data;
  export let selectedYear = '';

  let svg;
  let width = 500;
  let radius = width / 2;
  let colors = d3.schemeCategory10;

  let legendItems = [];

  onMount(() => {
    if (!data) return;

    d3.select('#sunburst').selectAll('*').remove();

    svg = d3
      .select('#sunburst')
      .attr('width', width)
      .attr('height', width)
      .append('g')
      .attr('transform', `translate(${width / 2},${width / 2})`);

    const partition = d3.partition().size([2 * Math.PI, radius]);

    const root = d3.hierarchy(data).sum((d) => d.value);

    partition(root);

    const arc = d3
      .arc()
      .startAngle((d) => d.x0)
      .endAngle((d) => d.x1)
      .innerRadius((d) => d.y0)
      .outerRadius((d) => d.y1);

    let paths = svg
      .selectAll('path')
      .data(root.descendants().slice(1))
      .enter()
      .append('path')
      .attr('d', arc)
      .style('fill', (d, i) => colors[i % colors.length])
      .style('stroke', '#fff')
      .append('title')
      .text((d) => `${d.data.name}: ${d.value}`);

    // 🏷️ Update legend items
    legendItems = root.children.map((d, i) => ({
      name: d.data.name,
      color: colors[i % colors.length],
      value: d.data.value
    }));

    // Center Year Label (Needs to be removed and re-added to update)
    d3.select('#year-label').remove();

    svg
      .append('text')
      .attr('id', 'year-label')
      .attr('text-anchor', 'middle')
      .attr('dy', '0.35em')
      .style('font-size', '24px')
      .style('font-weight', 'bold')
      .text(selectedYear);
  });
</script>

<svg id="sunburst"></svg>

<!-- 🎨 Legend Section -->
<div class="legend">
  {#each legendItems as item}
    <div class="legend-item">
      <span class="legend-color" style="background-color: {item.color};"></span>
      {item.name}: {item.value}
    </div>
  {/each}
</div>

<style>
  .legend {
    display: flex;
    flex-direction: column;
    margin-top: 10px;
  }

  .legend-item {
    display: flex;
    align-items: center;
    font-size: 14px;
    margin: 4px 0;
  }

  .legend-color {
    width: 16px;
    height: 16px;
    display: inline-block;
    margin-right: 8px;
    border-radius: 4px;
  }
</style>
