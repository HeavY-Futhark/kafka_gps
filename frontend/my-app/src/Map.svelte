<script>
  import { onMount } from "svelte";
  import "leaflet/dist/leaflet.css";
  import L from "leaflet"

  onMount(() => {
    const map = L.map("map").setView([51.505, -0.09], 13);
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png").addTo(map);

    var marker_icon = L.icon({
      iconUrl: 'assets/marker.png',
      iconSize:     [48, 48], // size of the icon
      iconAnchor: [24, 48],
      popupAnchor:  [0, -32] // point from which the popup should open relative to the iconAnchor
    });
    var marker = L.marker([51.5, -0.09], {icon: marker_icon}).addTo(map);
    marker.bindPopup("I'm a marker").openPopup();
  });
</script>

<style>
  #map {
    width: 100%;
    height: 80vh;
  }
</style>

<div id="map"></div>

