<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';

  const { allData = [], year, handleDataSelect } = $props();

  let chartContainer;

  // Function to extract EU data for the selected year
  function extractEUData() {
    return allData
      .map((area) => ({
        file: area.file,
        value: parseFloat(
          area.data.find(
            (entry) => entry.country === 'EU' && entry[year] !== undefined
          )?.[year] || '0'
        ),
        valueRange: calculateAreaValueRange(area, year)
      }))
      .filter((item) => !isNaN(item.value) && item.value !== 0);
  }

  // Calculate value range for an area
  function calculateAreaValueRange(area, year) {
    const values = area.data
      .map((entry) => parseFloat(entry[year] || '0'))
      .filter((value) => !isNaN(value));

    return {
      min: Math.min(...values),
      max: Math.max(...values)
    };
  }

  // Render chart function
  function renderChart() {
    if (!chartContainer) return;
    
    // Clear previous chart
    d3.select(chartContainer).selectAll('*').remove();

    // Prepare data using the current `year`
    const data = extractEUData();

    // Chart dimensions
    const margin = { top: 0, right: 60, bottom: 0, left: 200 };
    const width = 600 - margin.left - margin.right;
    const height = 400 - margin.top - margin.bottom;

    // Create SVG
    const svg = d3
      .select(chartContainer)
      .append('svg')
      .attr('width', width + margin.left + margin.right)
      .attr('height', height + margin.top + margin.bottom)
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    // Y Scale (for file names)
    const y = d3
      .scaleBand()
      .domain(data.map((d) => d.file))
      .range([0, height])
      .padding(0.1);

    // X Scale (for values) using log scale to handle large value ranges
    const x = d3
      .scaleLog()
      .domain([
        Math.max(0.1, Math.min(...data.map((d) => d.value))),
        Math.max(...data.map((d) => d.value))
      ])
      .range([0, width]);

    // Y Axis (file names)
    svg
      .append('g')
      .call(d3.axisLeft(y))
      .selectAll('text')
      .style('text-anchor', 'end');

    let isclicked;
    let itemSelected;
    let objectSelected;

    // Bars with value labels
    data.forEach((item) => {
      const bar = svg
        .append('rect')
        .attr('class', 'bar')
        .attr('y', y(item.file) || 0)
        .attr('height', y.bandwidth())
        .attr('x', 0)
        .attr('width', x(item.value))
        .attr('fill', 'steelblue')
        .style('cursor', 'pointer')
        .on('click', function () {
          if (isclicked) {
            d3.select(objectSelected).attr('fill', 'steelblue');
          }
          isclicked = true;
          itemSelected = item;
          objectSelected = this;
          handleDataSelect(item.file);
          d3.select(this).attr('fill', '#F7DC6F');
        })
        .on('mouseover', function () {
          d3.select(this).attr('fill', '#F7DC6F');
        })
        .on('mouseout', function () {
          if (!isclicked || item.file !== itemSelected.file) {
            d3.select(this).attr('fill', 'steelblue');
          }
        });

      // Value label
      svg
        .append('text')
        .attr('x', x(item.value) + 5)
        .attr('y', (y(item.file) || 0) + y.bandwidth() / 2)
        .attr('dy', '0.35em')
        .text(item.value.toFixed(2))
        .style('font-size', '12px')
        .style('fill', 'black');
    });

    // Title
    svg
      .append('text')
      .attr('x', width / 2)
      .attr('y', -10)
      .attr('text-anchor', 'middle')
      .style('font-size', '16px')
      .text(`EU Data for ${year}`);
  }

  // Reactive effect to update chart when `year` changes
  $effect(() => {
    if (chartContainer && allData.length) {
      renderChart();
    }
  });
</script>

<section class="chart-container">
  <div bind:this={chartContainer}></div>
</section>

<style>
  section {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    border-radius: 10px;
    border: 3px solid rgba(0, 0, 0, 0.8);
    padding: 20px;
    background-color: white;
  }
</style>