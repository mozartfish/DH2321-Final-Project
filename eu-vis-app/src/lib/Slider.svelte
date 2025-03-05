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
    min={2000}
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

  :root {
    --range-slider: #df40a2; /* slider main background color */
    --range-handle-inactive: #9cc5f8; /* inactive handle color */
    --range-handle: #838de7; /* non-focussed handle color */
    --range-handle-focus: #4a40d4; /* focussed handle color */
    --range-handle-border: var(--range-handle); /* handle border color */
    --range-range-inactive: var(
      --range-handle-inactive
    ); /* inactive range bar background color */
    --range-range: var(
      --range-handle-focus
    ); /* active range background color */
    --range-limit: #b9c2c2; /* limit range background color */
    --range-float-inactive: var(
      --range-handle-inactive
    ); /* inactive floating label background color */
    --range-float: var(
      --range-handle-focus
    ); /* floating label background color */
    --range-float-text: white; /* text color on floating label */
  }
</style>
