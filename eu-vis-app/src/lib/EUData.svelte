<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';

  // Props
  const {
    // all country data
    allCountriesData = [],
    // eu country names
    euCountries = [],
    // selected country from map
    selectedCountry = null,
    // eu country name constant
    euCountry = 'EU',
    // year passed from parent component
    year
  } = $props();

  // process data for visualization
  let formattedData = $derived(
    allCountriesData.length > 0
      ? allCountriesData.map((countryData) => {
          const country = countryData.country;
          const indicator = countryData.indicator;
          const units = countryData.unit;

          // process data to map year to data for visualization
          const yearDataObject = Object.entries(countryData)
            .filter(([key]) => !['country', 'indicator', 'units'].includes(key))
            .map(([year, value]) => ({
              year: Number(year),
              value: value === '' ? null : parseFloat(value)
            }))


          return { country, indicator, units, yearDataObject };
        })
      : []
  );

  // chart dimensions
  let width = $state(800);
  let height = $state(500);
  const margin = 60;

  // color scales
  const countryColorScale = () => {
    const countries = formattedData.map((d) => d.country);
    const colorRange = countries.map((d, i) =>
      d3.interpolateRainbow(i / countries.length)
    );
    return d3.scaleOrdinal().domain(countries).range(colorRange);
  };

  // initialize, load and draw visualization upon app load
  onMount(() => {
    drawChart();
    window.addEventListener('resize', resize);
    return () => window.removeEventListener('resize', resize);
  });

  // react to change in data and year -> redraw chart
  $effect(() => {
    if (formattedData.length > 0 && year) {
      drawChart();
    }
  });

  // window resize
  function resize() {
    width = window.innerWidth * 0.8;
    height = window.innerHeight * 0.5;
    drawChart();
  }

  // draw line chart
  function drawChart() {
    if (!formattedData || formattedData.length === 0) return;

    d3.select('#line-chart').selectAll('*').remove();
    const chartWidth = width - margin * 2;
    const svg = d3
      .select('#line-chart')
      .attr('width', width)
      .attr('height', height);
    // data element groups for drawing
    const lineGroup = svg.append('g').attr('class', 'lines');
    const circleGroup = svg.append('g').attr('class', 'year-indicators');

    // filter out eu  and selected country data
    let selectedCountryEUData = formattedData;
    if (selectedCountry) {
      selectedCountryEUData = formattedData.filter(
        (d) => d.country === selectedCountry || d.country === euCountry
      );
    }
    // process data for visualization
    const selectedCountryEUValues = [];
    selectedCountryEUData.forEach((country) => {
      country.yearDataObject.forEach((yearData) => {
        if (yearData.value !== null) {
          selectedCountryEUValues.push({
            country: country.country,
            date: new Date(yearData.year, 0),
            value: yearData.value
          });
        }
      });
    });
    const allValues = selectedCountryEUValues
      .map((d) => d.value)
      .filter((v) => v !== null);
    const allDates = selectedCountryEUValues.map((d) => d.date);
    const dataUnits =
      selectedCountryEUData.length > 0 ? selectedCountryEUData[0].units : '';

    // scales
    const xScale = d3
      .scaleTime()
      .domain(d3.extent(allDates))
      .range([margin, chartWidth])
      .nice();

    const yScale = d3
      .scaleLinear()
      .domain([d3.min(allValues) * 0.9, d3.max(allValues) * 1.1])
      .range([height - margin, margin])
      .nice();

    const colorScale = countryColorScale();

    // line generator
    const line = d3
      .line()
      .x((d) => xScale(d.date))
      .y((d) => yScale(d.value))
      .curve(d3.curveMonotoneX);

    // draw country lines
    selectedCountryEUData.forEach((country) => {
      const dateValues = country.yearDataObject
        .map((d) => ({
          date: new Date(d.year, 0),
          value: d.value
        }))
        .filter((d) => d.value !== null);

      // draw line
      lineGroup
        .append('path')
        .datum(dateValues)
        .attr('fill', 'none')
        .attr('stroke', colorScale(country.country))
        .attr('stroke-width', 2.5)
        .attr('d', line);
    });

    // if a country is selected
    if (selectedCountry) {
      const legend = svg
        .append('g')
        .attr('class', 'legend')
        .attr('transform', `translate(${chartWidth - 120}, ${margin})`);

      selectedCountryEUData.forEach((country, i) => {
        // policy indicator
        const yearDataObject = country.yearDataObject.find(
          (d) => d.year === year
        );
        if (yearDataObject && yearDataObject.value !== null) {
          circleGroup
            .append('circle')
            .attr('cx', xScale(new Date(year, 0)))
            .attr('cy', yScale(yearDataObject.value))
            .attr('r', 6)
            .attr('fill', colorScale(country.country))
            .attr('stroke', 'black')
            .attr('stroke-width', 2);
        }

        // legend
        const legendGroup = legend
          .append('g')
          .attr('transform', `translate(0, ${i * 20})`);
        legendGroup
          .append('rect')
          .attr('width', 12)
          .attr('height', 12)
          .attr('fill', colorScale(country.country));
        legendGroup
          .append('text')
          .attr('x', 16)
          .attr('y', 10)
          .text(country.country)
          .style('font-size', '12px');
      });
    }

    // draw axes
    const xAxis = d3
      .axisBottom(xScale)
      .tickFormat(d3.timeFormat('%Y'))
      .ticks(10);
    svg
      .append('g')
      .attr('transform', `translate(0,${height - margin})`)
      .call(xAxis);
    svg
      .append('text')
      .attr('text-anchor', 'middle')
      .attr('x', chartWidth / 2)
      .attr('y', height)
      .style('font-size', '12px')
      .text('Year');

    const yAxis = d3.axisLeft(yScale).ticks(10);
    svg.append('g').attr('transform', `translate(${margin},0)`).call(yAxis);
    svg
      .append('text')
      .attr('text-anchor', 'middle')
      .attr('transform', 'rotate(-90)')
      .attr('y', margin / 2 - 15)
      .attr('x', -(height / 2))
      .style('font-size', '12px')
      .text(dataUnits);
  }
</script>

<h1>EU COUNTRIES DATA COMPONENT</h1>
<svg id="line-chart"></svg>
