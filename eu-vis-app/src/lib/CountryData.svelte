<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';

  const { countryData = [], country = '' } = $props();
  console.log('This is the country data component');

  $effect(() => {
    console.log('countryData updated to: ', $state.snapshot(countryData));
    console.log('country updated to: ', country);
  });

  // let formattedData = $derived(countryData.forEach);

  let formattedData = Object.entries(countryData[0])
    .filter(([key]) => !['country', 'indicator', 'unit'].includes(key))
    .map(([year, value]) => ({
      year: Number(year),
      value: value === '' ? null : parseFloat(value)
    }));

  console.log('Formatted data : ', formattedData);

  let width = 500,
    height = 300,
    margin = 40;

  onMount(() => {
    drawChart();
    window.addEventListener('resize', resize);
  });

  function resize() {
    width = window.innerWidth * 0.8;
    height = window.innerHeight * 0.5;
    drawChart();
  }

  function drawChart() {
    d3.select('svg').selectAll('*').remove();
    const svg = d3
      .select('#line-chart')
      .attr('width', width)
      .attr('height', height);

    const xScale = d3
      .scaleLinear()
      .domain(d3.extent(formattedData, (d) => d.year))
      .range([margin, width - margin]);

    const yScale = d3
      .scaleLinear()
      .domain([0, d3.max(formattedData, (d) => d.value)])
      .range([height - margin, margin]);

    const line = d3
      .line()
      .x((d) => xScale(d.year))
      .y((d) => yScale(d.value))
      .curve(d3.curveMonotoneX); // Smooth curve

    svg
      .append('path')
      .datum(formattedData)
      .attr('fill', 'none')
      .attr('stroke', 'steelblue')
      .attr('stroke-width', 2)
      .attr('d', line);

    // Add Axes
    svg
      .append('g')
      .attr('transform', `translate(0,${height - margin})`)
      .call(d3.axisBottom(xScale));

    svg
      .append('g')
      .attr('transform', `translate(${margin},0)`)
      .call(d3.axisLeft(yScale));
  }
</script>

<svg id="line-chart"></svg>

<section>
  <h3>Country Data Component</h3>
  
  {#each countryData as d}
    <p>{d}</p>
  {/each}
  <!-- This is the Country Data Component

   {#if data.length > 0}
        <table>
            <thead>
                <tr>
                    {#each Object.keys(data[0]) as key}
                        <th>{key}</th>
                    {/each}
                </tr>
            </thead>
            <tbody>
                {#each data as row}
                    <tr>
                        {#each Object.values(row) as value}
                            <td>{value}</td>
                        {/each}
                    </tr>
                {/each}
            </tbody>
        </table>
    {:else}
        <p>No data to show</p>
    {/if} -->
</section>

<style></style>
