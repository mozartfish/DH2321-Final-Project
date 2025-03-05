<script>
    import { onMount } from 'svelte';
    import * as d3 from 'd3';
  
    const {
      countriesData = [],
      countries = [],
      euData = [],
      eu = '',
    } = $props();
  
    console.log('This is the multy country data component');
  
    // print statement for printing the country data
    $effect(() => {
      console.log('countryData updated to: ', countriesData);
      console.log('country updated to: ', countries);
      console.log('euData updated to: ', euData);
      console.log('eu has been update: ', eu);
    });
  
    // Group data by country
    let dataByCountry = $derived(
        Object.fromEntries(
            countries.map(country => {
            const countryData = countriesData.filter(d => d.country === country);
            return [
                country, 
                countryData.length > 0
                ? Object.entries(countryData[0])
                    .filter(([key]) => !['country', 'indicator', 'unit'].includes(key))
                    .map(([year, value]) => ({
                        year: Number(year),
                        value: value === '' ? null : parseFloat(value)
                    }))
                : []
            ];
            })
        )
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
  
  
    let indicator = $state('');
    let unit = $state('');
  
    $effect(() => {
      // Get indicator and unit from the first country data
      if (countriesData.length > 0) {
        indicator = countriesData[0].indicator || '';
        unit = countriesData[0].unit || '';
      }
      
      console.log('Data by country: ', dataByCountry);
      console.log('Formatted EU data: ', formattedeuData);
    });
  
    let width = $state(500);
    let height = $state(300);
    const margin = 60;
  
    const legendX = width - margin - 100;
    const legendY = margin + 20;
  
    const colorScale = d3.scaleOrdinal()
      .domain(countries)
      .range(['peachpuff', 'salmon', 'goldenrod', 'mediumaquamarine', 'mediumpurple', 'coral', 'cornflowerblue']);
  
  
    onMount(() => {
      drawChart();
      window.addEventListener('resize', resize);
  
      return () => {
        window.removeEventListener('resize', resize);
      };
    });
  
  
    // Reactive effect to redraw chart when data changes
    $effect(() => {
      if (Object.keys(dataByCountry).length > 0) {
        drawChart();
      }
    });
  
    function resize() {
      width = window.innerWidth * 0.8;
      height = window.innerHeight * 0.5;
      drawChart();
    }
  
    function drawChart() {
      if (Object.keys(dataByCountry).length === 0) return;
  
      d3.select('#multi-line-chart').selectAll('*').remove();
      const svg = d3
        .select('#multi-line-chart')
        .attr('width', width)
        .attr('height', height);

      // Prepare all data points for scaling
      let allDataPoints = [];
  
      // Convert year numbers to JavaScript Date objects
      const dateFormattedDataByCountry = {};
      for (const [country, data] of Object.entries(dataByCountry)) {
        dateFormattedDataByCountry[country] = data.map(d => ({
            date: new Date(d.year, 0),
            value: d.value,
            year: d.year,
            country: country
        }));
      
        allDataPoints = [...allDataPoints, ...dateFormattedDataByCountry[country]];
        }
  
        const dateFormattedEUData = formattedeuData.map((d) => ({
            date: new Date(d.year, 0),
            value: d.value
        }));

        allDataPoints = [...allDataPoints, ...dateFormattedEUData];

        // Find extent of all values and dates
        const allValues = allDataPoints
            .map(d => d.value)
            .filter(v => v !== null);
        
        const allDates = allDataPoints
            .map(d => d.date);
  
  
        // x time scale for the country line
        const xScale = d3
            .scaleTime()
            .domain(d3.extent(allDates))
            .range([margin, width - margin])
            .nice();
  
        // y scale for the country line
        const yScale = d3
            .scaleLinear()
            .domain([
            d3.min(allValues) * 0.9,
            d3.max(allValues) * 1.1
            ])
            .range([height - margin, margin])
            .nice();

        // Create tooltip div
        const tooltip = d3.select('body')
        .selectAll('.tooltip')
        .data([0])
        .enter()
        .append('div')
        .attr('class', 'tooltip')
        .style('position', 'absolute')
        .style('background-color', 'white')
        .style('border', '1px solid #ddd')
        .style('border-radius', '4px')
        .style('padding', '5px')
        .style('display', 'none')
        .style('pointer-events', 'none')
        .style('font-size', '12px')
        .style('z-index', '10');

  
        // Create line generator      
        const line = d3
        .line()
        .x((d) => xScale(d.date))
        .y((d) => yScale(d.value))
        .defined((d) => d.value !== null)
        .curve(d3.curveMonotoneX);

        for (const country of countries) {
            if (dateFormattedDataByCountry[country] && dateFormattedDataByCountry[country].length > 0) {
                svg
                .append('path')
                .datum(dateFormattedDataByCountry[country])
                .attr('fill', 'none')
                .attr('stroke', colorScale(country))
                .attr('stroke-width', 2)
                .attr('d', line);
                
            }
        }
  
        svg
            .append('path')
            .datum(dateFormattedEUData)
            .attr('fill', 'none')
            .attr('stroke', 'lightblue')
            .attr('stroke-width', 3)
            .attr('d', line);
    
  
        // x axis rendering
        const xAxis = d3
        .axisBottom(xScale)
        .tickFormat(d3.timeFormat('%Y'))
        .ticks(Math.min(10, dateFormattedEUData.length));

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

        if (countriesData.length > 0) {
        svg
            .append('text')
            .attr('text-anchor', 'middle')
            .attr('transform', 'rotate(-90)')
            .attr('y', margin / 2 - 15)
            .attr('x', -(height / 2))
            .style('font-size', '12px')
            .text(countriesData[0].unit || '');
        }
       
        const legendWidth = 250; // Fixed width for legend
        const effectiveWidth = width - legendWidth;

        // Prepare legend entries
        const legendEntries = [
            ...countries.map(country => ({
            label: country,
            color: colorScale(country),
            type: 'solid'
            })),
            {
            label: 'EU Average',
            color: 'lightblue',
            type: 'dashed'
            }
        ];

        // Draw Legend with Two Columns
        const legendGroup = svg.append('g')
            .attr('class', 'legend')
            .attr('transform', `translate(${effectiveWidth}, ${margin})`);

        const columnCount = 2;
        const itemHeight = 20; // Reduced from 25 to 20
        const itemWidth = 125; // Width for each column

        legendEntries.forEach((entry, index) => {
            // Calculate column and row
            const col = Math.floor(index / Math.ceil(legendEntries.length / columnCount));
            const row = index % Math.ceil(legendEntries.length / columnCount);

            // Legend line
            legendGroup.append('line')
            .attr('x1', col * itemWidth)
            .attr('y1', row * itemHeight)
            .attr('x2', col * itemWidth + 20)
            .attr('y2', row * itemHeight)
            .attr('stroke', entry.color)
            .attr('stroke-width', 3)
            .attr('stroke-dasharray', entry.type === 'dashed' ? '5,5' : 'none');

            // Legend text
            legendGroup.append('text')
            .attr('x', col * itemWidth + 25)
            .attr('y', row * itemHeight + 5)
            .text(entry.label)
            .style('font-size', '12px');
        });

        // Compact background for legend
        svg.insert('rect', '.legend')
            .attr('x', effectiveWidth - 10)
            .attr('y', margin - 10)
            .attr('width', legendWidth)
            .attr('height', Math.ceil(legendEntries.length / columnCount) * itemHeight + 10) // Reduced padding
            .attr('fill', 'rgba(255,255,255,0.8)')
            .attr('stroke', '#e0e0e0')
            .attr('stroke-width', 1)
            .attr('rx', 5)
            .attr('ry', 5);


    }

</script>
  
  <section>
    <div class="chart-container">
      <svg id="multi-line-chart"></svg>
    </div>
  
    <h3>Countries: {countries}</h3>

  </section>
  
  <style>
    .chart-container {
      width: 100%;
      overflow-x: auto;
    }
  </style>
  