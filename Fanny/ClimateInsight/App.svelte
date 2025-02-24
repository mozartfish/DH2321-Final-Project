<script>
    import { onMount } from "svelte";
    import * as d3 from "d3";

    let message = "Welcome to European Climate Insights!";
    let width = 800, height = 500;

    onMount(() => {
        const svg = d3.select("#map")
            .append("svg")
            .attr("width", width)
            .attr("height", height);
        
        svg.append("circle")
            .attr("cx", width / 2)
            .attr("cy", height / 2)
            .attr("r", 50)
            .style("fill", "lightblue");
    });
</script>

<style>
    .map-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 500px;
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
    }
</style>

<h1>{message}</h1>
<div class="map-container">
    <div id="map"></div>
</div>
