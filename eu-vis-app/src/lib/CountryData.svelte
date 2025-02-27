<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';

  const {
    countryData = [],
    country = '',
    euData = [],
    eu = '',
    policyData = []
  } = $props();

  console.log('This is the country data component');

  // print statement for printing the country data
  $effect(() => {
    console.log('countryData updated to: ', countryData);
    console.log('country updated to: ', country);
    console.log('euData updated to: ', euData);
    console.log('eu has been update: ', eu);
    selectedPolicies = [];
  });

  // derive a new dataset for updating the UI based on the data passed in
  let formattedData = $derived(
    countryData.length > 0
      ? Object.entries(countryData[0])
          .filter(([key]) => !['country', 'indicator', 'unit'].includes(key))
          .map(([year, value]) => ({
            year: Number(year),
            value: value === '' ? null : parseFloat(value)
          }))
      : []
  );

  let formattedeuData = $derived(
    euData.length > 0
      ? Object.entries(euData[0])
          .filter(([key]) => !['country', 'indicator', 'unit'].includes(key))
          .map(([year, value]) => ({
            year: Number(year),
            value: value === '' ? null : parseFloat(value)
          }))
      : []
  );

  let relevantPolicies = $derived(
    policyData.filter((policy) => policy.country === country)
  );

  let selectedPolicies = $state([]);

  $effect(() => {
    console.log('Formatted data: ', formattedData);
    console.log('Formatted eu data: ', formattedeuData);
  });

  let width = $state(500);
  let height = $state(300);
  const margin = 60;

  const legendX = width - margin - 100;
  const legendY = margin + 20;

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

  // Update the function to show all policies for the selected year
  function showPolicyDetails(policy) {
    selectedPolicies = relevantPolicies.filter(
      (p) => Number(p.year) === Number(policy.year)
    );
  }

  function drawChart() {
    if (
      ((!formattedData || formattedData.length === 0) && !formattedeuData) ||
      formattedeuData.length === 0
    )
      return;

    d3.select('#line-chart').selectAll('*').remove();
    const svg = d3
      .select('#line-chart')
      .attr('width', width)
      .attr('height', height);

    // Convert year numbers to JavaScript Date objects
    const dateFormattedData = formattedData.map((d) => ({
      date: new Date(d.year, 0),
      value: d.value
    }));

    const dateFormattedEUData = formattedeuData.map((d) => ({
      date: new Date(d.year, 0),
      value: d.value
    }));

    // x time scale for the country line
    const xScale = d3
      .scaleTime()
      .domain(d3.extent(dateFormattedData, (d) => d.date))
      .range([margin, width - margin])
      .nice();

    // y scale for the country line
    const yScale = d3
      .scaleLinear()
      .domain([
        d3.min(dateFormattedData, (d) => d.value) * 0.9,
        d3.max(dateFormattedData, (d) => d.value) * 1.1
      ])
      .range([height - margin, margin])
      .nice();

    // eu data x scale
    const euXScale = d3
      .scaleTime()
      .domain(d3.extent(dateFormattedEUData, (d) => d.date))
      .range([margin, width - margin])
      .nice();

    // eu data y scale
    const euYScale = d3
      .scaleLinear()
      .domain([
        d3.min(dateFormattedEUData, (d) => d.value) * 0.9,
        d3.max(dateFormattedEUData, (d) => d.value) * 1.1
      ])
      .range([height - margin, margin])
      .nice();

    // c
    const line = d3
      .line()
      .x((d) => xScale(d.date))
      .y((d) => yScale(d.value))
      .defined((d) => d.value !== null)
      .curve(d3.curveMonotoneX);

    const euLine = d3
      .line()
      .x((d) => euXScale(d.date))
      .y((d) => euYScale(d.value))
      .defined((d) => d.value !== null)
      .curve(d3.curveMonotoneX);

    svg
      .append('path')
      .datum(dateFormattedData)
      .attr('fill', 'none')
      .attr('stroke', 'peachpuff')
      .attr('stroke-width', 3)
      .attr('d', line);

    svg
      .append('path')
      .datum(dateFormattedEUData)
      .attr('fill', 'none')
      .attr('stroke', 'lightblue')
      .attr('stroke-width', 3)
      .attr('d', euLine);

    // x axis rendering
    const xAxis = d3
      .axisBottom(xScale)
      .tickFormat(d3.timeFormat('%Y'))
      .ticks(Math.min(dateFormattedData.length, 10));

    // render x axis
    svg
      .append('g')
      .attr('transform', `translate(0,${height - margin})`)
      .call(xAxis);

    svg
      .append('text')
      .attr('text-anchor', 'middle')
      .attr('x', width / 2)
      .attr('y', height - 10)
      .style('font-size', '12px')
      .text('Year');

    // render y axis
    svg
      .append('g')
      .attr('transform', `translate(${margin},0)`)
      .call(d3.axisLeft(yScale));

    svg
      .append('text')
      .attr('text-anchor', 'middle')
      .attr('transform', 'rotate(-90)')
      .attr('y', margin / 2 - 15)
      .attr('x', -(height / 2))
      .style('font-size', '12px')
      .text(countryData[0].unit);

    svg
      .append('line')
      .attr('x1', legendX)
      .attr('y1', legendY)
      .attr('x2', legendX + 20)
      .attr('y2', legendY)
      .attr('stroke', 'peachpuff')
      .attr('stroke-width', 3);

    svg
      .append('text')
      .attr('x', legendX + 25)
      .attr('y', legendY + 4)
      .text(country)
      .style('font-size', '12px');

    svg
      .append('line')
      .attr('x1', legendX)
      .attr('y1', legendY + 20)
      .attr('x2', legendX + 20)
      .attr('y2', legendY + 20)
      .attr('stroke', 'lightblue')
      .attr('stroke-width', 3);

    svg
      .append('text')
      .attr('x', legendX + 25)
      .attr('y', legendY + 24)
      .text('EU Average')
      .style('font-size', '12px');

    const validYears = new Set(
      dateFormattedData
        .filter((d) => d.value !== null)
        .map((d) => d.date.getFullYear())
    );
    const policiesWithValue = relevantPolicies.filter((p) =>
      validYears.has(Number(p.year))
    );

    // Add policy pins
    if (policiesWithValue.length > 0) {
      const policyGroup = svg.append('g').attr('class', 'policy-pins');

      // Create pin groups using filtered policies
      const pins = policyGroup
        .selectAll('.policy-pin')
        .data(policiesWithValue)
        .enter()
        .append('g')
        .attr('class', 'policy-pin')
        .attr(
          'transform',
          (d) =>
            `translate(${xScale(new Date(+d.year, 0))}, ${height - margin + 28})`
        )
        .style('cursor', 'pointer')
        .on('click', (event, d) => {
          showPolicyDetails(d);
        });

      // Draw pin head (circle)
      pins.append('circle').attr('r', 6).attr('fill', 'tomato');

      // Draw pin base (triangle pointing up)
      pins
        .append('path')
        .attr('d', 'M-5,-3 L5,-3 L0,-10 Z')
        .attr('fill', 'tomato');
    }
  }
</script>

<section>
  <div class="chart-container">
    <svg id="line-chart"></svg>
  </div>

  <h3>Country: {country}</h3>

  {#if countryData.length > 0}
    <div class="data-summary">
      <p>Indicator: {countryData[0].indicator || 'N/A'}</p>
      <p>Unit: {countryData[0].unit || 'N/A'}</p>

      {#if selectedPolicies.length > 0}
        {#each selectedPolicies as policy, i}
          <div class="policy-details">
            <h4>{policy.year}</h4>
            <strong>Policy:</strong>
            <p>
              {policy.policy || 'No details available'}
            </p>
            <br />
            <p><strong>Sector:</strong> {policy.sector}</p>
            <br />
            <p><strong>Description:</strong> {policy.description}</p>
          </div>
        {/each}
      {:else if relevantPolicies && relevantPolicies.length > 0}
        <p class="click-instruction">Click on a pin to view policy details</p>
      {/if}
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
  .policy-details {
    width: 500px;
    margin-top: 15px;
    padding: 10px;
    background-color: #e3f2fd;
    border-left: 4px solid #2196f3;
    border-radius: 2px;
  }
  .click-instruction {
    color: #666;
    font-style: italic;
    margin-top: 10px;
  }
</style>
