<script>
  const { policyData = [], country = '' } = $props();
  console.log('This is the country data component');
  $effect(() => {
    console.log('policyData : ', policyData);
    console.log('country : ', country);
  });
</script>

<section>
  <h3>Policies Data for {country}</h3>
  <ul>
    {#each policyData.filter((policy) => !country || policy.country === country) as policy, i}
      <li>
        {policy.country} ({policy.year}) - {policy.sector}
      </li>
    {/each}
  </ul>
</section>
