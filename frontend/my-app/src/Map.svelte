<script>
  import { onMount } from "svelte";
  import "leaflet/dist/leaflet.css";
  import L from "leaflet"

  onMount(() => {
    const map = L.map("map").setView([51.505, -0.09], 13);
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png").addTo(map);
  });
</script>

<style>
  #map {
    height: 400px;
    width: 100%;
  }
</style>

<div id="map"></div>

