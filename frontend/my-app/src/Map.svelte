<script>
  import { onMount } from "svelte";
  import "leaflet/dist/leaflet.css";
  import L from "leaflet"

  var api_address = '127.0.0.1:80';

  function updateLatestCoordinate(marker, api_address) { 
    fetch(api_address+'/latest_coordinates')
      .then((response) => response.json())
      .then((data) => {
        marker.setLatLng([data.latitude, data.longitude]);
        marker.bindPopup("I'm a marker").openPopup();
      }).catch(error => {
        console.error("Error fetching latest coordinates: ", error)
      });
  }

  onMount(() => {
    const map = L.map("map").setView([51.505, -0.09], 13);
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png").addTo(map);

    var marker_icon = L.icon({
      iconUrl: 'assets/marker.png',
      iconSize:     [48, 48],
      iconAnchor: [24, 48],
      popupAnchor:  [0, -32]
    });
    var marker = L.marker([51.5, -0.09], {icon: marker_icon}).addTo(map);

    const updateInterval = setInterval(() => {
      updateLatestCoordinate(marker, api_address);
    }, 5000);
    onDestroy(() => clearInterval(updateInterval));

  });
</script>

<style>
  #map {
    width: 100%;
    height: 80vh;
  }
</style>

<div id="map"></div>

