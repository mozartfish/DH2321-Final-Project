<script>
  // Simple props matching EUData pattern
  const {
    policyData = [],
    selectedCountry = null,
    year
  } = $props();

  // Log for debugging, similar to EUData
  $effect(() => {
    console.log('PolicyData - selectedCountry:', selectedCountry);
    console.log('PolicyData - year:', year);
  });
</script>

<section>
  <h1>POLICY DATA COMPONENT</h1>
  {#if selectedCountry && policyData.length > 0}
    <div class="policy-container">
      <h2>Policies for {selectedCountry} in {year}</h2>
      <ul>
        {#each policyData.filter(policy => 
          policy.country === selectedCountry && 
          parseInt(policy.year) === year
        ) as policy}
          <li>
            <strong>{policy.sector}:</strong> {policy.name}
          </li>
        {/each}
      </ul>
    </div>
  {/if}
</section>

<style>
  section {
    margin-top: 20px;
  }
  
  h1 {
    text-align: center;
  }
  
  .policy-container {
    border-radius: 10px;
    border: 3px solid rgba(0, 0, 0, 0.8);
    padding: 20px;
    background-color: antiquewhite;
    max-width: 800px;
    margin: 0 auto;
  }
  
  ul {
    list-style-type: none;
    padding-left: 0;
  }
  
  li {
    margin-bottom: 10px;
    padding: 10px;
    background-color: white;
    border-radius: 5px;
    border: 1px solid #ddd;
  }
</style>
