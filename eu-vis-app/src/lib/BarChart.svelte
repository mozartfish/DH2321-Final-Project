<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';

  const {
    allData = [],
    handleDataSelect,
    selectedFile,
    selectedCountry,
    year
  } = $props();

  let chartContainer;
  let isclicked;
  let selectedCountryBar = $state();
  let selectedFileBar = $state();
  let objectSelected = $state();

  $effect(() => {
    selectedCountryBar = selectedCountry != null ? selectedCountry : 'EU';
    selectedFileBar = selectedFile;
  });

  // Function to extract EU data for the given year
  function extractEUData() {
    return allData
      .map((area) => ({
        file: area.file,
        value: parseFloat(
          area.data.find(
            (entry) =>
              entry.country === selectedCountryBar && entry[year] !== undefined
          )?.[year] || '0'
        ),
        valueRange: calculateAreaValueRange(area)
      }))
      .filter((item) => !isNaN(item.value) && item.value !== 0);
  }

  // Calculate value range for an area
  function calculateAreaValueRange(area) {
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
    // Clear previous chart
    d3.select(chartContainer).selectAll('*').remove();

    // Prepare data
    const data = extractEUData();

    // Chart dimensions
    const margin = { top: 50, right: 100, bottom: 50, left: 200 };
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

    // Calculate stick height and vertical positioning
    const stickHeight = y.bandwidth() * 0.4;
    const stickVerticalOffset = (y.bandwidth() - stickHeight) / 2;

    // Bars with value labels
    data.forEach((item) => {
      const bar = svg
        .append('rect')
        .attr('class', 'bar')
        .attr('data-file', item.file)
        .attr('y', (y(item.file) || 0) + stickVerticalOffset)
        .attr('height', stickHeight)
        .attr('x', 0)
        .attr('width', x(item.value))
        .attr('rx', stickHeight / 2)
        .attr('ry', stickHeight / 2)
        .attr('fill', 'steelblue')
        .style('cursor', 'pointer')
        .on('click', function () {
          if (isclicked) {
            d3.select(objectSelected).attr('fill', 'steelblue');
          }
          isclicked = true;
          selectedFileBar = item.file;
          objectSelected = this;
          handleDataSelect(item.file);
          d3.select(this).attr('fill', '#F7DC6F');
        })
        .on('mouseover', function () {
          d3.select(this).attr('fill', '#F7DC6F');
        })
        .on('mouseout', function () {
          if (!isclicked || item.file != selectedFileBar) {
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

    d3.selectAll('rect')
      .filter(function () {
        return d3.select(this).attr('data-file') === selectedFileBar;
      })
      .attr('fill', '#F7DC6F');

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
    if (chartContainer && allData && selectedCountryBar != null) {
      renderChart();
    }
  });
</script>

<section>
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
