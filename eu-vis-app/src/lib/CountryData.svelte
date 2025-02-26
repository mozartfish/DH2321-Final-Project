<script>
    let {data} = $props();
    console.log("you have entered the data prop;")
    console.log("this is the data: ", data);
    // export let data = [];
</script>
<section>
    This is the Country Data Component

   {#if data.length > 0}
        <table>
            <thead>
                <tr>
                    {#each Object.keys(data[0]) as key}
                        <th>{key}</th>
                    {/each}
                </tr>
            </thead>
            <tbody>
                {#each data as row}
                    <tr>
                        {#each Object.values(row) as value}
                            <td>{value}</td>
                        {/each}
                    </tr>
                {/each}
            </tbody>
        </table>
    {:else}
        <p>No data to show</p>
    {/if}
</section>
<style></style>