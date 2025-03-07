<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';

  let extraWidth = $state(0);

  // Props – now selectedCountries is expected to be an array.
  let {
    allCountriesData = [],
    euCountries = [],
    selectedCountries = ['EU'],
    euCountry = 'EU',
    year,
    dataMin = $bindable()
  } = $props();

  let formattedData = $derived(
    allCountriesData.length > 0
      ? allCountriesData.map((countryData) => {
          const country = countryData.country;
          const indicator = countryData.indicator;
          const units = countryData.unit;

          const yearDataObject = Object.entries(countryData)
            .filter(([key]) => !['country', 'indicator', 'units'].includes(key))
            .map(([yr, value]) => ({
              year: Number(yr),
              value: value === '' ? null : parseFloat(value)
            }))
            .filter((d) => d.year <= 2022);

          return { country, indicator, units, yearDataObject };
        })
      : []
  );

  // Chart dimensions
  let width = $state(800);
  let height = $state(500);
  const margin = 60;

  // Color scale
  const countryColorScale = () => {
    const countries = formattedData.map((d) => d.country);
    const colorRange = countries.map((d, i) =>
      d3.interpolateRainbow(i / countries.length)
    );
    return d3.scaleOrdinal().domain(countries).range(colorRange);
  };

  onMount(() => {
    drawChart();
    window.addEventListener('resize', resize);
    return () => window.removeEventListener('resize', resize);
  });

  $effect(() => {
    if (formattedData.length > 0) {
      drawChart();
      const minYear = d3.min(formattedData, (d) =>
        d3.min(
          d.yearDataObject.filter((y) => y.value !== null),
          (y) => y.year
        )
      );
      dataMin = minYear;
      console.log('dataMin', dataMin);
    }
  });

  // Handle window resize
  function resize() {
    width = window.innerWidth * 0.8;
    height = window.innerHeight * 0.5;
    drawChart();
  }

  // Draw line chart
  function drawChart() {
    if (!formattedData || formattedData.length === 0) return;
    d3.select('#line-chart').selectAll('*').remove();
    const chartWidth = width - margin * 2;

    const svg = d3
      .select('#line-chart')
      .attr('width', width + extraWidth)
      .attr('height', height);

    const lineGroup = svg.append('g').attr('class', 'lines');

    // If selectedCountries is empty or equals [euCountry], show all data.
    // Otherwise, filter to only show the selected countries plus the EU.
    let selectedCountryEUData;
    if (
      !selectedCountries ||
      selectedCountries.length === 0 ||
      (selectedCountries.length === 1 && selectedCountries[0] === euCountry)
    ) {
      selectedCountryEUData = formattedData;
    } else {
      selectedCountryEUData = formattedData.filter(
        (d) => selectedCountries.includes(d.country) || d.country === euCountry
      );
    }

    const selectedCountryEUValues = [];
    selectedCountryEUData.forEach((country) => {
      country.yearDataObject.forEach((yearData) => {
        if (yearData.value !== null) {
          selectedCountryEUValues.push({
            country: country.country,
            date: new Date(yearData.year, 0),
            value: yearData.value,
            year: yearData.year
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

    // Scales
    const xScale = d3
      .scaleTime()
      .domain(d3.extent(allDates))
      .range([margin, chartWidth])
      .nice(d3.timeYear.every(1));

    const yScale = d3
      .scaleLinear()
      .domain([d3.min(allValues) * 0.9, d3.max(allValues) * 1.1])
      .range([height - margin, margin])
      .nice();

    const colorScale = countryColorScale();

    // Line generator
    const line = d3
      .line()
      .x((d) => xScale(d.date))
      .y((d) => yScale(d.value))
      .curve(d3.curveMonotoneX);

    // Draw a line for each country in selectedCountryEUData.
    selectedCountryEUData.forEach((country) => {
      const dateValues = country.yearDataObject
        .map((d) => ({
          date: new Date(d.year, 0),
          value: d.value,
          year: d.year
        }))
        .filter((d) => d.value !== null);

      lineGroup
        .append('path')
        .datum(dateValues)
        .attr('fill', 'none')
        .attr('stroke', colorScale(country.country))
        .attr('stroke-width', 2.5)
        .attr('stroke-dasharray', country.country === euCountry ? '5' : 'none')
        .attr('d', line);
    });

    // Create legend positioned to the right outside the chart area.
    let legendX;
    const numCountries = selectedCountryEUData.length;
    if (numCountries > 10) {
      legendX = width - margin - 40;
      extraWidth = 140;
    } else {
      legendX = width - margin - 50;
      extraWidth = 0;
    }
    const legend = svg
      .append('g')
      .attr('class', 'legend')
      .attr('transform', `translate(${legendX}, ${margin})`);

    if (numCountries > 10) {
      // Split into two columns.
      const half = Math.ceil(numCountries / 2);
      selectedCountryEUData.forEach((country, i) => {
        const col = i < half ? 0 : 1;
        const row = i < half ? i : i - half;
        const xOffset = col * 140;
        const yOffset = row * 20;
        const legendGroup = legend
          .append('g')
          .attr('transform', `translate(${xOffset}, ${yOffset})`);

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
    } else {
      // One column layout.
      selectedCountryEUData.forEach((country, i) => {
        const xOffset = 0;
        const yOffset = i * 20;
        const legendGroup = legend
          .append('g')
          .attr('transform', `translate(${xOffset}, ${yOffset})`);

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

    // Draw a vertical line at the selected year.
    svg
      .append('line')
      .attr('x1', xScale(new Date(year, 0)))
      .attr('x2', xScale(new Date(year, 0)))
      .attr('y1', margin)
      .attr('y2', height - margin)
      .attr('stroke', 'black')
      .attr('stroke-opacity', 0.3)
      .attr('stroke-width', 2)
      .attr('stroke-dasharray', '10');

    // Draw axes.
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

<svg id="line-chart"></svg>
