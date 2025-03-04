<script>
  import RangeSlider from 'svelte-range-slider-pips';

  let { year = $bindable() } = $props();

  let values = $state([year]);

  $effect(() => {
    values = [year];
  });

  $effect(() => {
    if (values[0] !== year) {
      year = values[0];
    }
  });
</script>

<div id="slider">
  <h2>{year}</h2>
  <RangeSlider
    pips
    first="label"
    last="label"
    min={1990}
    max={2024}
    bind:values
  />
</div>

<style>
  h2 {
    margin-top: 20px;
    text-align: center;
    font-size: 42px;
  }
  #slider {
    width: 50%;
    margin: 0 auto;
  }
</style>
