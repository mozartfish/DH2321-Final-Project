<script>
    import { onMount } from "svelte";
    import * as d3 from "d3";
  
    let data = [
      { x: 0, y: 10 },
      { x: 1, y: 40 },
      { x: 2, y: 30 },
      { x: 3, y: 60 },
      { x: 4, y: 20 },
      { x: 5, y: 50 }
    ];

    // Add the real data here
  
    let width = 500, height = 300, margin = 40;
  
    onMount(() => {
      const svg = d3.select("#line-chart")
        .attr("width", width)
        .attr("height", height);
  
      const xScale = d3.scaleLinear()
        .domain([0, d3.max(data, d => d.x)])
        .range([margin, width - margin]);
  
      const yScale = d3.scaleLinear()
        .domain([0, d3.max(data, d => d.y)])
        .range([height - margin, margin]);
  
      const line = d3.line()
        .x(d => xScale(d.x))
        .y(d => yScale(d.y))
        .curve(d3.curveBasis); // Smooth curve
  
      svg.append("path")
        .datum(data)
        .attr("fill", "none")
        .attr("stroke", "steelblue")
        .attr("stroke-width", 2)
        .attr("d", line);
  
      // Add Axes
      svg.append("g")
        .attr("transform", `translate(0,${height - margin})`)
        .call(d3.axisBottom(xScale));
  
      svg.append("g")
        .attr("transform", `translate(${margin},0)`)
        .call(d3.axisLeft(yScale));
    });
  </script>

  <h2>A line plot for a specific country</h2>

  <style> h2 {
    color:aquamarine
  }</style>
  
  <svg id="line-chart"></svg>

