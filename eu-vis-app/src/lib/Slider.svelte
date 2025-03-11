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
  <div class="container">
    <RangeSlider
      id="rangeSlider"
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
    color: #094c93;
    margin-bottom: -10px;
  }
  #slider {
    width: 100%;
    height: 100%;
    margin: 0;
    border-radius: 10px;
    border: 3px solid rgba(0, 0, 0, 0.8);
    background-color: white;
  }
  .container {
    scale: 0.9;
  }

  :root {
    --range-slider: #094c93; /* slider main background color */
    --range-handle-inactive: #ffc459; /* inactive handle color */
    --range-handle: #ffc459; /* non-focussed handle color */
    --range-handle-focus: #ffc459; /* focussed handle color */
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

  /* Custom style to turn the slider handle into a star */
  .rangeSlider > .rangeHandle > .rangeNub {
    width: 1000px;
    /* width: 30px;
    height: 30px;
    background-c olor: var(--range-handle);
    clip-path: polygon(
      50% 0%,
      61% 35%,
      98% 35%,
      68% 57%,
      79% 91%,
      50% 70%,
      21% 91%,
      32% 57%,
      2% 35%,
      39% 35%
    );
    border: 2px solid var(--range-handle-border);
    */
  }
</style>
