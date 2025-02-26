<script>
  let { data, country } = $props();
  console.log('hello world, I am the EU Data Component');
  $inspect(country);
  $inspect(data);
  // preprocess all the data based on the country that came in
  // console.log('selected data: ', data);
  // console.log('selected country: ', country);
  // const countryData = data.find((item) => item.country === country);
  // const euData = data.find((item) => item.country === "EU");
  // console.log("countryData: ", countryData);
  // console.log("euData: ", euData);
</script>

<section>This is the EU Data Component</section>

<style></style>
