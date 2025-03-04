<script>
  const { year = 2024 } = $props();

  let selectedYear = $state(year);

  const minYear = 2000;
  const maxYear = 2024;

  function handleOnChange(event) {
    console.log(event.target.value);
  }

  $effect(() => {
    console.log(`Year value updated: ${selectedYear}`);
  });
</script>

<div class="year-slider">
  <h2>Year: {selectedYear}</h2>

  <div class="slider-container">
    <input
      type="range"
      min={minYear}
      max={maxYear}
      bind:value={selectedYear}
      on:change={handleOnChange}
      class="slider"
    />

    <div class="year-labels">
      <span class="min-year">{minYear}</span>
      <span class="max-year">{maxYear}</span>
    </div>
  </div>
</div>

<style>
  .year-slider {
    font-family: Arial, sans-serif;
    max-width: 500px;
    margin: 2rem auto;
    padding: 1.5rem;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }

  h2 {
    color: #333;
    margin-top: 0;
    margin-bottom: 1.5rem;
  }

  .slider-container {
    margin-bottom: 1rem;
  }

  .slider {
    width: 100%;
    height: 6px;
    -webkit-appearance: none;
    appearance: none;
    background: #d0d0d0;
    outline: none;
    border-radius: 999px;
  }

  .slider::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: #6185ff;
    cursor: pointer;
    box-shadow:
      0 1px 1px 0 rgba(0, 0, 0, 0.14),
      0 0px 2px 1px rgba(0, 0, 0, 0.2);
  }

  .slider::-moz-range-thumb {
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: #6185ff;
    cursor: pointer;
    box-shadow:
      0 1px 1px 0 rgba(0, 0, 0, 0.14),
      0 0px 2px 1px rgba(0, 0, 0, 0.2);
  }

  .year-labels {
    display: flex;
    justify-content: space-between;
    margin-top: 0.5rem;
    color: #666;
  }

  .current-year {
    font-weight: bold;
    color: #6185ff;
  }
</style>
