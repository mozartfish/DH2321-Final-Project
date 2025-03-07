<script>
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
    selectedCountryBar = selectedCountry || 'EU';
    selectedFileBar = selectedFile;
  });

  // Compute mean values for each file
  function extractEUData() {
    const col = year + '_z';
    return allData
      .map((area) => {
        const values = area.data
          .filter(
            (entry) =>
              entry.country === selectedCountryBar && entry[col] !== undefined
          )
          .map((entry) => parseFloat(entry[col]))
          .filter((num) => !isNaN(num)); // Remove NaN values

        if (values.length === 0) return null; // Skip if no valid numbers

        return {
          file: area.file,
          mean: d3.mean(values)
        };
      })
      .filter((item) => item !== null);
  }

  function renderChart() {
    d3.select(chartContainer).selectAll('*').remove();
    const data = extractEUData();

    const margin = { top: 24, right: 24, bottom: 20, left: 120 };
    const width = 450 - margin.left - margin.right;
    const height = 260 - margin.top - margin.bottom;

    const svg = d3
      .select(chartContainer)
      .append('svg')
      .attr('width', width + margin.left + margin.right)
      .attr('height', height + margin.top + margin.bottom)
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    // Y scale for file names
    const y = d3
      .scaleBand()
      .domain(data.map((d) => d.file))
      .range([0, height])
      .padding(0.1);

    // X scale fixed to [-1, 1]
    const x = d3.scaleLinear().domain([-1, 1]).range([10, width]);

    // X-axis
    svg
      .append('g')
      .attr('transform', `translate(0,${height})`)
      .call(d3.axisBottom(x));

    // Y-axis
    svg
      .append('g')
      .call(d3.axisLeft(y))
      .selectAll('text')
      .style('text-anchor', 'end')
      .attr('dx', '-0.5em')

    // Vertical line at x=0
    svg
      .append('line')
      .attr('x1', x(0))
      .attr('x2', x(0))
      .attr('y1', 0)
      .attr('y2', height)
      .attr('stroke', 'black')
      .attr('stroke-width', 1);

    data.forEach((item) => {
      const yPos = y(item.file) || 0;
      const rowHeight = y.bandwidth();
      const barHeight = rowHeight * 1;
      const barY = yPos + (rowHeight - barHeight) / 2;
      const barX = x(Math.min(0, item.mean));
      const barWidth = Math.abs(x(item.mean) - x(0));

      // Create a group for the row
      const rowGroup = svg.append('g').attr('class', 'row-group');

      // Add an invisible rectangle spanning the entire row as the clickable area
      rowGroup
        .append('rect')
        .attr('class', 'clickable-row')
        .attr('x', 0)
        .attr('y', yPos)
        .attr('width', width)
        .attr('height', rowHeight)
        .attr('fill', 'transparent')
        .style('cursor', 'pointer')
        .on('click', function () {
          if (isclicked) {
            d3.select(objectSelected).attr('fill', '#26AE60');
          }
          isclicked = true;
          selectedFileBar = item.file;
          // Save a reference to the bar rectangle (inside this row)
          objectSelected = rowGroup.select('.bar').node();
          handleDataSelect(item.file);
          rowGroup.select('.bar').attr('fill', '#F49C12');
        })
        .on('mouseover', function () {
          rowGroup.select('.bar').attr('fill', '#F49C12');
        })
        .on('mouseout', function () {
          if (!isclicked || item.file !== selectedFileBar) {
            rowGroup.select('.bar').attr('fill', '#26AE60');
          }
        });

      // Draw the actual bar
      rowGroup
        .append('rect')
        .attr('class', 'bar')
        .attr('x', barX)
        .attr('y', barY)
        .attr('width', barWidth)
        .attr('height', barHeight)
        .attr('fill', '#26AE60')
        .style('pointer-events', 'none')
        .attr('data-file', item.file);

      // Add the value label for the mean
      const labelOffset = item.mean >= 0 ? 5 : -5;
      const anchor = item.mean >= 0 ? 'start' : 'end';
      const labelX = x(item.mean) + labelOffset;
      const labelY = barY + barHeight / 2;
      rowGroup
        .append('text')
        .attr('x', labelX)
        .attr('y', labelY)
        .attr('dy', '0.35em')
        .text(item.mean.toFixed(2))
        .style('font-size', '10px')
        .style('fill', 'black')
        .style('pointer-events', 'none')
        .attr('text-anchor', anchor);
    });

    // Highlight any already-selected file
    svg
      .selectAll('rect[data-file]')
      .filter(function () {
        return d3.select(this).attr('data-file') === selectedFileBar;
      })
      .attr('fill', '#F49C12');

    // Title
    svg
      .append('text')
      .attr('x', width / 2)
      .attr('y', 0 - margin.top / 2)
      .attr('text-anchor', 'middle')
      .style('font-size', '16px')
      .text(`${selectedCountryBar} ${year}`);
  }

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
