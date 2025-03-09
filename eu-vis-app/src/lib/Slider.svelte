<script>
  import RangeSlider from 'svelte-range-slider-pips';

  let { year = $bindable(), dataMin } = $props();

  let values = $state([year]);

  $effect(() => {
    values = [year];
    console.log('SLIDER DATA MIN', dataMin);
  });

  $effect(() => {
    if (values[0] !== year) {
      year = values[0];
    }
  });
</script>

<div id="slider">
  <h2>{year}</h2>
  <!-- <RangeSlider
    pips
    first="label"
    last="label"
    min={2000}
    max={2022}
    bind:values
  /> -->
  <div class="container">
    <RangeSlider
      pips
      first="label"
      last="label"
      min={dataMin}
      max={2022}
      bind:values
    />
  </div>
</div>

<style>
  h2 {
    text-align: center;
    font-size: 35px;
    color: #5E01A7;
    margin-bottom: -12px;
  }
  #slider {
    width: 50%;
    margin: 10px;
    border-radius: 10px;
    border: 3px solid rgba(0, 0, 0, 0.8);
    background-color: white;
  }
  .container {
    scale: 0.9;
  }

  :root {
    --range-slider: #5E01A7; /* slider main background color */
    --range-handle-inactive: #fa963e; /* inactive handle color */
    --range-handle: #fa963e; /* non-focussed handle color */
    --range-handle-focus: #fa963e; /* focussed handle color */
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
