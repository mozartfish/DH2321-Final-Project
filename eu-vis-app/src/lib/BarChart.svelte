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

  const colorMain = '#094C93';
  const colorSecondary = '#002357';

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

    const margin = { top: 4, right: 30, bottom: 34, left: 160 };
    const width = 450 - margin.left - margin.right;
    const height = 340 - margin.top - margin.bottom;

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

    svg
      .append('text')
      .attr('text-anchor', 'middle')
      .attr('x', width / 2)
      .attr('y', height + margin.bottom - 1)
      .style('font-size', '14px')
      .style('font-weight', 'bold')
      .text('Difference from mean');

    // Y-axis with class for each tick text
    const yAxis = svg.append('g').call(d3.axisLeft(y));

    // Add a unique class to each y-axis label based on the file name
    yAxis
      .selectAll('.tick text')
      .attr(
        'class',
        (d) => `file-label-${d.replace(/\s+/g, '-').replace(/[^\w-]/g, '')}`
      )
      .style('text-anchor', 'end')
      .attr('dx', '-0.5em');

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

      // Create a unique CSS-safe class name from the file name
      const fileClass = item.file.replace(/\s+/g, '-').replace(/[^\w-]/g, '');

      // Create a group for the row
      const rowGroup = svg.append('g').attr('class', 'row-group');

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
            d3.select(objectSelected).attr('fill', '#6C55A4');
          }
          isclicked = true;
          selectedFileBar = item.file;
          // Save a reference to the bar rectangle
          objectSelected = rowGroup.select('.bar').node();
          handleDataSelect(item.file);
          rowGroup.select('.bar').attr('fill', colorSecondary);
        })
        .on('mouseover', function () {
          rowGroup.select('.bar').attr('fill', colorSecondary);
          // Make the corresponding y-axis label bold
          d3.select(`.file-label-${fileClass}`).style('font-weight', 'bold');
        })
        .on('mouseout', function () {
          if (!isclicked || item.file !== selectedFileBar) {
            rowGroup.select('.bar').attr('fill', colorMain);
          }
          // Reset the y-axis label to normal weight unless it's the selected file
          if (item.file !== selectedFileBar) {
            d3.select(`.file-label-${fileClass}`).style(
              'font-weight',
              'normal'
            );
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
        .attr('fill', colorMain)
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
      .attr('fill', colorSecondary);

    // Make the selected file label bold
    if (selectedFileBar) {
      const selectedFileClass = selectedFileBar
        .replace(/\s+/g, '-')
        .replace(/[^\w-]/g, '');
      d3.select(`.file-label-${selectedFileClass}`).style(
        'font-weight',
        'bold'
      );
    }

    // Title
    /*
    svg
      .append('text')
      .attr('x', width / 2 - 30)
      .attr('y', 0 - margin.top / 2)
      .attr('text-anchor', 'middle')
      .style('font-size', '24px')
      .style('font-weight', 'bold')
      .text(selectedCountryBar + ' scores for year ' + year);
  */
  }

  $effect(() => {
    if (chartContainer && allData && selectedCountryBar != null) {
      renderChart();
    }
  });
</script>

<section>
  <h2>{selectedCountryBar} in year {year}</h2>
  <div bind:this={chartContainer}></div>
</section>

<style>
  section {
    width: 100%;
    padding-top: 4px;
    padding-bottom: 4px;
    display: flex;
    flex-direction: column;
    align-items: center;
    border-radius: 10px;
    border: 3px solid rgba(0, 0, 0, 0.8);
    background-color: white;
  }

  h2 {
    color: #094C93;
  }
</style>
