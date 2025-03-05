<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';

  const { allData = [], handleDataSelect } = $props();

  let selectedYear = $state(2020);
  let chartContainer;

  // Function to extract EU data for the selected year
  function extractEUData(year) {
    return allData
      .map((area) => ({
        file: area.file,
        value: parseFloat(
          area.data.find(
            (entry) => entry.country === 'EU' && entry[year] !== undefined
          )?.[year] || '0'
        ),
        // Extract min and max values for this area across all countries
        valueRange: calculateAreaValueRange(area, year)
      }))
      .filter((item) => !isNaN(item.value) && item.value !== 0);
  }

  // Calculate value range for an area
  function calculateAreaValueRange(area, selectedYear) {
    const values = area.data
      .map((entry) => parseFloat(entry[selectedYear] || '0'))
      .filter((value) => !isNaN(value));

    return {
      min: Math.min(...values),
      max: Math.max(...values)
    };
  }

  // Render chart function
  function renderChart(year) {
    // Clear previous chart
    d3.select(chartContainer).selectAll('*').remove();

    // Prepare data
    const data = extractEUData(selectedYear);

    // Chart dimensions
    const margin = { top: 50, right: 20, bottom: 150, left: 60 };
    const width = 1000 - margin.left - margin.right;
    const height = 500 - margin.top - margin.bottom;

    // Create SVG
    const svg = d3
      .select(chartContainer)
      .append('svg')
      .attr('width', width + margin.left + margin.right)
      .attr('height', height + margin.top + margin.bottom)
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    // X Scale
    const x = d3
      .scaleBand()
      .domain(data.map((d) => d.file))
      .range([0, width])
      .padding(0.1);

    // Create individual Y scales for each area
    const yScales = data.map((item) =>
      d3
        .scaleLinear()
        .domain([item.valueRange.min, item.valueRange.max])
        .range([height, 0])
    );

    // X Axis
    svg
      .append('g')
      .attr('transform', `translate(0,${height})`)
      .call(d3.axisBottom(x))
      .selectAll('text')
      .style('text-anchor', 'end')
      .attr('dx', '-.8em')
      .attr('dy', '.15em')
      .attr('transform', 'rotate(-65)');

    let isclicked;

    // Bars with individual scaling
    data.forEach((item, index) => {
      svg
        .append('rect')
        .attr('class', 'bar')
        .attr('x', x(item.file) || 0)
        .attr('width', x.bandwidth())
        .attr('y', yScales[index](item.value))
        .attr('height', height - yScales[index](item.value))
        .attr('fill', 'steelblue')
        .style('cursor', 'pointer')
        .on('click', () => {
          isclicked = true;
          handleDataSelect(item.file);
          console.log('debug2', item.file);
          d3.select(this).attr('fill', 'green');
        })
        .on('mouseover', function () {
          if (!isclicked) {
            d3.select(this).attr('fill', 'orange');
          }
        })
        .on('mouseout', function () {
          if (!isclicked) {
            d3.select(this).attr('fill', 'steelblue');
          }
        });

      // Individual Y axis for each area
      svg
        .append('g')
        .attr('transform', `translate(${x(item.file) || 0}, 0)`)
        .call(d3.axisLeft(yScales[index]).ticks(5));
    });

    // Title
    svg
      .append('text')
      .attr('x', width / 2)
      .attr('y', 0 - margin.top / 2)
      .attr('text-anchor', 'middle')
      .style('font-size', '16px')
      .text(`EU Data for ${year}`);
  }

  // Reactive statement to re-render chart when year changes
  $effect(() => {
    if (chartContainer && allData) {
      renderChart(selectedYear);
    }
  });

  // Years for dropdown
  const years = Array.from({ length: 16 }, (_, i) => 2008 + i);
</script>

<div class="chart-container">
  <select bind:value={selectedYear}>
    {#each years as year}
      <option value={year}>{year}</option>
    {/each}
  </select>

  <div bind:this={chartContainer}></div>
</div>

<style>
  .chart-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    max-width: 1200px;
    margin: 0 auto;
  }

  select {
    margin-bottom: 20px;
    padding: 5px;
  }
</style>
