<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';

  let extraWidth = $state(0);
  let extraHeight = $state(0);
  let currentLegendPage = $state(0); // Track current legend page

  // Props – now selectedCountries is expected to be an array.
  let {
    allCountriesData = [],
    euCountries = [],
    selectedCountries = ['EU'],
    euCountry = 'EU',
    year,
    dataMin = $bindable(),
    selectedFile = ''
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
  let height = $state(250);
  const margin = 65;

  // Legend pagination variables
  let totalLegendPages = $state(1);
  let itemsPerPage = $state(7);

  // Color scale
  const countryColorScale = () => {
    const countries = formattedData.map((d) => d.country);
    const colorRange = countries.map((d, i) =>
      d3.interpolatePlasma(i / countries.length)
    );
    return d3.scaleOrdinal().domain(countries).range(colorRange);
  };

  onMount(() => {
    drawChart();
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

  // Navigation functions for legend pagination
  function nextLegendPage() {
    if (currentLegendPage < totalLegendPages - 1) {
      currentLegendPage++;
      drawChart();
    }
  }

  function prevLegendPage() {
    if (currentLegendPage > 0) {
      currentLegendPage--;
      drawChart();
    }
  }

  // Draw line chart
  function drawChart() {
    if (!formattedData || formattedData.length === 0) return;
    d3.select('#line-chart').selectAll('*').remove();
    const chartWidth = width - margin * 2;

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

    // Calculate pagination for legend
    const numCountries = selectedCountryEUData.length;
    if (numCountries <= 7) {
      itemsPerPage = 7;
      totalLegendPages = 1;
      currentLegendPage = 0;
    } else {
      itemsPerPage = 7; // Show 7 items per page
      totalLegendPages = Math.ceil(numCountries / itemsPerPage);

      // Ensure current page is valid
      if (currentLegendPage >= totalLegendPages) {
        currentLegendPage = totalLegendPages - 1;
      }
    }

    // Set dimensions
    extraWidth = 0;
    width = 700;
    extraHeight = Math.max(
      0,
      Math.min(itemsPerPage, numCountries) * 20 - (height - 20 * 2)
    );

    // Update SVG dimensions
    const svg = d3
      .select('#line-chart')
      .attr('width', width)
      .attr('height', height + extraHeight);

    const lineGroup = svg.append('g').attr('class', 'lines');

    // Create tooltip
    const tooltip = svg
      .append('g')
      .attr('class', 'tooltip')
      .style('display', 'none');

    tooltip
      .append('rect')
      .attr('width', 120)
      .attr('height', 24)
      .attr('fill', 'white')
      .attr('stroke', '#ccc')
      .attr('rx', 4)
      .attr('ry', 4)
      .attr('opacity', 0.9);

    tooltip
      .append('text')
      .attr('x', 60)
      .attr('y', 16)
      .attr('text-anchor', 'middle')
      .style('font-size', '12px');

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

    // Add transparent overlay for better hover detection
    lineGroup
      .append('rect')
      .attr('x', margin)
      .attr('y', margin)
      .attr('width', chartWidth - margin)
      .attr('height', height - margin * 2)
      .attr('fill', 'none')
      .attr('pointer-events', 'all')
      .on('mousemove', function (event) {
        tooltip.style('display', 'none');
      });

    // Draw a line for each country in selectedCountryEUData.
    selectedCountryEUData.forEach((country) => {
      const dateValues = country.yearDataObject
        .map((d) => ({
          date: new Date(d.year, 0),
          value: d.value,
          year: d.year
        }))
        .filter((d) => d.value !== null);

      // Invisible thicker path for easier hovering
      lineGroup
        .append('path')
        .datum(dateValues)
        .attr('fill', 'none')
        .attr('stroke', 'transparent')
        .attr('stroke-width', 10)
        .attr('d', line)
        .attr('pointer-events', 'all')
        .on('mouseover', function (event) {
          // Highlight this line - make it thicker (changed from 4 to 6)
          d3.selectAll(`.line-${country.country.replace(/\s+/g, '-')}`).attr(
            'stroke-width',
            6
          );

          // Show tooltip with country name
          tooltip.style('display', null);
          tooltip.select('text').text(country.country);
          const [mouseX, mouseY] = d3.pointer(event);
          tooltip.attr(
            'transform',
            `translate(${mouseX - 60}, ${mouseY - 30})`
          );
        })
        .on('mouseout', function () {
          // Reset line thickness
          d3.selectAll(`.line-${country.country.replace(/\s+/g, '-')}`).attr(
            'stroke-width',
            2.5
          );

          // Hide tooltip
          tooltip.style('display', 'none');
        })
        .on('mousemove', function (event) {
          // Update tooltip position
          const [mouseX, mouseY] = d3.pointer(event);
          tooltip.attr(
            'transform',
            `translate(${mouseX - 60}, ${mouseY - 30})`
          );
        });

      // Visible line
      lineGroup
        .append('path')
        .datum(dateValues)
        .attr('fill', 'none')
        .attr('stroke', colorScale(country.country))
        .attr('stroke-width', 2.5)
        .attr('stroke-dasharray', country.country === euCountry ? '5' : 'none')
        .attr('d', line)
        .attr('class', `line-${country.country.replace(/\s+/g, '-')}`);
    });

    // Create legend
    const legendX = width - margin - 18;
    const legend = svg.append('g').attr('class', 'legend');

    // Add pagination controls
    if (totalLegendPages > 1) {
      const paginationGroup = svg
        .append('g')
        .attr('class', 'pagination')
        .attr('transform', `translate(${legendX}, ${margin - 25})`);

      // Left arrow
      paginationGroup
        .append('text')
        .attr('x', 0)
        .attr('y', 0)
        .text('❮')
        .attr('class', 'pagination-arrow')
        .style('font-size', '16px')
        .style('cursor', currentLegendPage > 0 ? 'pointer' : 'default')
        .style('opacity', currentLegendPage > 0 ? 1 : 0.5)
        .style('user-select', 'none')
        .on('click', prevLegendPage);

      // Page indicator
      paginationGroup
        .append('text')
        .attr('x', 30)
        .attr('y', 0)
        .text(`${currentLegendPage + 1}/${totalLegendPages}`)
        .style('font-size', '12px')
        .style('user-select', 'none');

      // Right arrow
      paginationGroup
        .append('text')
        .attr('x', 60)
        .attr('y', 0)
        .text('❯')
        .attr('class', 'pagination-arrow')
        .style('font-size', '16px')
        .style(
          'cursor',
          currentLegendPage < totalLegendPages - 1 ? 'pointer' : 'default'
        )
        .style('opacity', currentLegendPage < totalLegendPages - 1 ? 1 : 0.5)
        .style('user-select', 'none')
        .on('click', nextLegendPage);
    }

    legend.attr('transform', `translate(${legendX}, ${margin})`);

    const startIdx = currentLegendPage * itemsPerPage;
    const endIdx = Math.min(startIdx + itemsPerPage, numCountries);

    // Show only countries for the current page
    selectedCountryEUData.slice(startIdx, endIdx).forEach((country, i) => {
      const yOffset = i * 20;
      const countryClass = `legend-${country.country.replace(/\s+/g, '-')}`;

      const legendGroup = legend
        .append('g')
        .attr('transform', `translate(0, ${yOffset})`)
        .attr('class', countryClass)
        .style('cursor', 'pointer')
        .on('mouseover', function () {
          // Highlight the corresponding line
          d3.selectAll(`.line-${country.country.replace(/\s+/g, '-')}`).attr(
            'stroke-width',
            6
          );

          // Don't show tooltip when hovering over legend items
          tooltip.style('display', 'none');
        })
        .on('mouseout', function () {
          // Reset line thickness
          d3.selectAll(`.line-${country.country.replace(/\s+/g, '-')}`).attr(
            'stroke-width',
            2.5
          );
        });

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

    // Draw a vertical line at the selected year.
    svg
      .append('line')
      .attr('x1', xScale(new Date(year, 0)))
      .attr('x2', xScale(new Date(year, 0)))
      .attr('y1', margin)
      .attr('y2', height - margin)
      .attr('stroke', 'black')
      .attr('stroke-opacity', 0.3);

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
      .attr('y', height - 25)
      .style('font-size', '14px')
      .style('font-weight', 'bold')
      .text('Year');

    const yAxis = d3.axisLeft(yScale).ticks(10);
    svg.append('g').attr('transform', `translate(${margin},0)`).call(yAxis);

    svg
      .append('text')
      .attr('text-anchor', 'middle')
      .attr('transform', 'rotate(-90)')
      .attr('y', margin / 2)
      .attr('x', -(height / 2))
      .style('font-size', '12px')
      .style('font-weight', 'bold')
      .text(dataUnits);

    svg
      .append('text')
      .attr('x', width / 2)
      .attr('y', 30) // Position at the top
      .attr('text-anchor', 'middle')
      .style('font-size', '24px')
      .style('font-weight', 'bold')
      .text('Evolution of ' + selectedFile);
  }
</script>

<section>
  <svg id="line-chart"></svg>
</section>

<style>
  section {
    width: 100%;
    border-radius: 10px;
    border: 3px solid rgba(0, 0, 0, 0.8);
    padding-top: 4px;
    align-items: stretch;
    background-color: white;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }
</style>
