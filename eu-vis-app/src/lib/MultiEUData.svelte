<script>
    import { onMount } from 'svelte';
    import * as d3 from 'd3';
  
    // props
    const {
      // data for all the countries
      allCountriesData = [],
      // eu countries name list
      euCountries = [],
      // country name of the country selected by user
      selectedCountries,
      // eu country name
      euCountry = 'EU'
    } = $props();
  
    $effect(() => {
      console.log('debug 9:', selectedCountries);
    });
  
    // derive a new dataset for updating the UI based on the data passed in
    let formattedData = $derived(
      allCountriesData.length > 0
        ? allCountriesData.map((countryData) => {
            // import country data
            const country = countryData.country;
            const indicator = countryData.indicator;
            const units = countryData.unit;
  
            // map year and data into an object
            const yearDataObject = Object.entries(countryData)
              .filter(([key]) => !['country', 'indicator', 'units'].includes(key))
              .map(([year, value]) => ({
                year: Number(year),
                value: value === '' ? null : parseFloat(value)
              }));
  
            // return new country object
            return {
              country,
              indicator,
              units,
              yearDataObject
            };
          })
        : []
    );
  
    // set up chart variables
    let width = $state(800);
    let height = $state(500);
    const margin = 60;
  
    // country color scale - there are 28 unique countries (EU countries + EU)
    const countryColorScale = () => {
      const countries = formattedData.map((d) => d.country);
      const colorRange = countries.map((d, i) =>
        d3.interpolateRainbow(i / countries.length)
      );
      return d3.scaleOrdinal().domain(countries).range(colorRange);
    };
  
    // load the visualization when the application loads
    onMount(() => {
      drawChart();
      window.addEventListener('resize', resize);
      return () => {
        window.removeEventListener('resize', resize);
      };
    });
  
    // resize chart when data changes
    $effect(() => {
      if (formattedData.length > 0) {
        drawChart();
      }
      console.log('debug 7:', selectedCountries);
    });
  
    // redraw chart when selected country changes
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
  
      // remove previous chart
      d3.select('#line-chart').selectAll('*').remove();
  
      // set up a width for the chart
      const chartWidth = width - margin * 2;
  
      const svg = d3
        .select('#line-chart')
        .attr('width', width)
        .attr('height', height);
  
      // filter elected country data and eu data
      let selectedCountriesEUData = formattedData;
      if (selectedCountries) {
        selectedCountriesEUData = formattedData.filter(
          (d) => selectedCountries.includes(d.country) || d.country === euCountry
        );
      }
  
      // process data for eu and selected country
      const selectedCountriesEUValues = [];
      selectedCountriesEUData.forEach((country) => {
        country.yearDataObject.forEach((year) => {
          if (year.value !== null) {
            selectedCountriesEUValues.push({
              country: country.country,
              date: new Date(year.year, 0),
              value: year.value
            });
          }
        });
      });
  
      // remove all null values for visualizing the data with a line chart
      const allValues = selectedCountriesEUValues
        .map((d) => d.value)
        .filter((v) => v !== null);
  
      // units of measurement for the data
      const dataUnits =
        selectedCountriesEUData.length > 0
          ? selectedCountriesEUData[0].units
          : '';
  
      // get all the dates for x scale
      const allDates = selectedCountriesEUValues.map((d) => d.date);
  
      // Scales
      // x scales
      const xScale = d3
        .scaleTime()
        .domain(d3.extent(allDates))
        .range([margin, chartWidth])
        .nice();
  
      // y scales
      const yScale = d3
        .scaleLinear()
        .domain([d3.min(allValues) * 0.9, d3.max(allValues) * 1.1])
        .range([height - margin, margin])
        .nice();
  
      // color scale for mapping countries to color
      const colorScale = countryColorScale();
  
      if (selectedCountries) {
        // Create legend
        const legend = svg
          .append('g')
          .attr('class', 'legend')
          .attr('transform', `translate(${chartWidth - 120}, ${margin})`);
  
        selectedCountriesEUData.forEach((country, i) => {
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
  
      // line generator
      const line = d3
        .line()
        .x((d) => xScale(d.date))
        .y((d) => yScale(d.value))
        .curve(d3.curveMonotoneX);
  
      // group for drawing and transforming lines
      const lineGroup = svg.append('g');
  
      // draw country lines
      selectedCountriesEUData.forEach((country) => {
        const dateValues = country.yearDataObject
          .map((d) => ({
            date: new Date(d.year, 0),
            value: d.value
          }))
          .filter((d) => d.value !== null);
  
        // draw lines
        lineGroup
          .append('path')
          .datum(dateValues)
          .attr('fill', 'none')
          .attr('stroke', colorScale(country.country))
          .attr('stroke-width', 2.5)
          .attr('d', line);
      });
  
      // draw axes
      // x axis
      const xAxis = d3
        .axisBottom(xScale)
        .tickFormat(d3.timeFormat('%Y'))
        .ticks(10);
      svg
        .append('g')
        .attr('transform', `translate(0,${height - margin})`)
        .call(xAxis);
  
      // x-axis label
      svg
        .append('text')
        .attr('text-anchor', 'middle')
        .attr('x', chartWidth / 2)
        .attr('y', height)
        .style('font-size', '12px')
        .text('Year');
  
      // y axis
      const yAxis = d3.axisLeft(yScale).ticks(10);
      svg.append('g').attr('transform', `translate(${margin},0)`).call(yAxis);
  
      // y-axis label
      svg
        .append('text')
        .attr('text-anchor', 'middle')
        .attr('transform', 'rotate(-90)')
        .attr('y', margin / 2 - 15)
        .attr('x', -(height / 2))
        .style('font-size', '12px')
        .text(dataUnits);
    }
  
    // for debugging
    $effect(() => {
      console.log('allcountries data updated to: ', allCountriesData);
      console.log('EU Countries updated to: ', euCountries);
      console.log('formatted EU DATA: ', formattedData);
      console.log('Selected country: ', selectedCountries);
    });
  </script>
  
  <h1>EU COUNTRIES DATA COMPONENT</h1>
  <svg id="line-chart"></svg>
  