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
      drawChart();
      window.addEventListener("resize", resize);  
    
    });

    function resize(){
      width = window.innerWidth * 0.8;
      height = window.innerHeight * 0.5;
      drawChart();
    }

    function drawChart(){

      d3.select("svg").selectAll("*").remove();
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
        .curve(d3.curveMonotoneX); // Smooth curve
  
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


      const tooltip = d3.select("body")
        .append("div")
        .style("position", "absolute")
        .style("background", "white")
        .style("padding", "5px")
        .style("border", "1px solid black")
        .style("display", "none");

      svg.selectAll("circle")
        .data(data)
        .enter()
        .append("circle")
        .attr("cx", d => xScale(d.x))
        .attr("cy", d => yScale(d.y))
        .attr("r", 5)
        .attr("fill", "red")
        .on("mouseover", (event, d) => {
          tooltip.style("display", "block")
            .html(`X: ${d.x}, Y: ${d.y}`)
            .style("left", (event.pageX + 10) + "px")
            .style("top", (event.pageY - 10) + "px");
        })
        .on("mouseout", () => tooltip.style("display", "none"));
          }
  </script>

  <h2>A line plot for a specific country</h2>

  <style> h2 {
    color:aquamarine
  }</style>
  
  <svg id="line-chart"></svg>

