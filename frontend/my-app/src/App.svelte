<script>
  import Map from "./Map.svelte";
  export let name;
</script>

<main>
  <h1>{name}</h1>
  <Map />
</main>

<style>
  main {
    text-align: center;
    margin: 1em;
  }
</style>

