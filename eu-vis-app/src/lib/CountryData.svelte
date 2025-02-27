<script>  
  import { onMount } from 'svelte';
  import * as d3 from 'd3';

  const { countryData = [], country = '' } = $props();
  
  console.log('This is the country data component');

  $effect(() => {
    console.log('countryData updated to: ', countryData);
    console.log('country updated to: ', country);
  });

  // Create a reactive statement to format data whenever countryData changes
  let formattedData = $derived(countryData.length > 0 
    ? Object.entries(countryData[0])
      .filter(([key]) => !['country', 'indicator', 'unit'].includes(key))
      .map(([year, value]) => ({
        year: Number(year),
        value: value === '' ? null : parseFloat(value)
      }))
    : []);

  $effect(() => {
    console.log('Formatted data: ', formattedData);
  });

  let width = $state(500);
  let height = $state(300);
  const margin = 40;

  onMount(() => {
    drawChart();
    window.addEventListener('resize', resize);
    
    return () => {
      window.removeEventListener('resize', resize);
    };
  });

  // Reactive effect to redraw chart when data changes
  $effect(() => {
    if (formattedData.length > 0) {
      drawChart();
    }
  });

  function resize() {
    width = window.innerWidth * 0.8;
    height = window.innerHeight * 0.5;
    drawChart();
  }

  function drawChart() {
    if (!formattedData || formattedData.length === 0) return;
    
    d3.select('#line-chart').selectAll('*').remove();
    const svg = d3
        .select('#line-chart')
        .attr('width', width)
        .attr('height', height);
    
    // Convert year numbers to JavaScript Date objects
    const dateFormattedData = formattedData.map(d => ({
        date: new Date(d.year, 0), // January 1st of the year
        value: d.value
    }));
    
    // Use scaleTime instead of scaleLinear for years
    const xScale = d3
        .scaleTime()
        .domain(d3.extent(dateFormattedData, d => d.date))
        .range([margin, width - margin]);
    
    const yScale = d3
        .scaleLinear()
        .domain([0, d3.max(dateFormattedData, d => d.value) || 1])
        .range([height - margin, margin]);
    
    const line = d3
        .line()
        .x(d => xScale(d.date))
        .y(d => yScale(d.value))
        .defined(d => d.value !== null)
        .curve(d3.curveMonotoneX);
    
    svg
        .append('path')
        .datum(dateFormattedData)
        .attr('fill', 'none')
        .attr('stroke', 'steelblue')
        .attr('stroke-width', 2)
        .attr('d', line);
    
    // Add a more appropriate time format for the x-axis
    const xAxis = d3.axisBottom(xScale)
        .tickFormat(d3.timeFormat('%Y')) // Format as year only
        .ticks(Math.min(dateFormattedData.length, 10)); // Limit number of ticks
    
    svg
        .append('g')
        .attr('transform', `translate(0,${height - margin})`)
        .call(xAxis);
    
    svg
        .append('g')
        .attr('transform', `translate(${margin},0)`)
        .call(d3.axisLeft(yScale));

    // Add title with country name
    svg
        .append('text')
        .attr('x', width / 2)
        .attr('y', margin / 2)
        .attr('text-anchor', 'middle')
        .style('font-size', '16px')
        .text(`${country} Data`);
  }
</script>

<div class="chart-container">
  <svg id="line-chart"></svg>
</div>

<section>
  <h3>Country: {country}</h3>
  
  {#if countryData.length > 0}
    <div class="data-summary">
      <p>Indicator: {countryData[0].indicator || 'N/A'}</p>
      <p>Unit: {countryData[0].unit || 'N/A'}</p>
    </div>
  {:else}
    <p>No data available for {country}</p>
  {/if}
</section>

<style>
  .chart-container {
    width: 100%;
    overflow-x: auto;
  }
  
  .data-summary {
    margin-top: 20px;
    padding: 10px;
    background-color: #f5f5f5;
    border-radius: 4px;
  }
</style>