<script>
  const { policyData = [], selectedCountry = null, year } = $props();
  console.log('This is the country data component');
  $effect(() => {
    console.log('policyData : ', policyData);
    console.log('policy selected country: ', selectedCountry);
    console.log('policy year: ', year);
  });
</script>

<!-- <section>
  <h2>Policy data component</h2>
  <h3>Policies Data for {country}</h3>
  <ul>
    {#each policyData.filter((policy) => !selectedCountry || policy.country === selectedCountry) as policy, i}
      <li>
        {policy.country} ({policy.year}) - {policy.sector}
      </li>
    {/each}
  </ul>
</section> -->