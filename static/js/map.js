/* =================================
	Map
==================================== */

// When the window has finished loading create our google map below
var address = document.getElementById('map');
var latitude, longitude;
var geocoder;

var IsClicked = false;
function init() {
    geocoder = new google.maps.Geocoder();
    geocoder.geocode({ 'address': $(address).attr('data-address') }, function (results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            latitude = results[0].geometry.location.lat();
            longitude = results[0].geometry.location.lng();
            var myLatlng = new google.maps.LatLng(latitude, longitude);
            //$('section.map').find('#googlemap').show();
            // Basic options for a simple Google Map
            // For more options see: https://developers.google.com/maps/documentation/javascript/reference#MapOptions
            var mapOptions = {
                // How zoomed in you want the map to start at (always required)
                zoom: 14,

                // The latitude and longitude to center the map (always required)
                center: myLatlng, // New York

                // How you would like to style the map. 
                // This is where you would paste any style found on Snazzy Maps.
                styles: [{ "featureType": "water", "elementType": "geometry.fill", "stylers": [{ "color": "#d3d3d3" }] }, { "featureType": "transit", "stylers": [{ "color": "#808080" }, { "visibility": "off" }] }, { "featureType": "road.highway", "elementType": "geometry.stroke", "stylers": [{ "visibility": "on" }, { "color": "#b3b3b3" }] }, { "featureType": "road.highway", "elementType": "geometry.fill", "stylers": [{ "color": "#ffffff" }] }, { "featureType": "road.local", "elementType": "geometry.fill", "stylers": [{ "visibility": "on" }, { "color": "#ffffff" }, { "weight": 1.8 }] }, { "featureType": "road.local", "elementType": "geometry.stroke", "stylers": [{ "color": "#d7d7d7" }] }, { "featureType": "poi", "elementType": "geometry.fill", "stylers": [{ "visibility": "on" }, { "color": "#ebebeb" }] }, { "featureType": "administrative", "elementType": "geometry", "stylers": [{ "color": "#a7a7a7" }] }, { "featureType": "road.arterial", "elementType": "geometry.fill", "stylers": [{ "color": "#ffffff" }] }, { "featureType": "road.arterial", "elementType": "geometry.fill", "stylers": [{ "color": "#ffffff" }] }, { "featureType": "landscape", "elementType": "geometry.fill", "stylers": [{ "visibility": "on" }, { "color": "#efefef" }] }, { "featureType": "road", "elementType": "labels.text.fill", "stylers": [{ "color": "#696969" }] }, { "featureType": "administrative", "elementType": "labels.text.fill", "stylers": [{ "visibility": "on" }, { "color": "#737373" }] }, { "featureType": "poi", "elementType": "labels.icon", "stylers": [{ "visibility": "off" }] }, { "featureType": "poi", "elementType": "labels", "stylers": [{ "visibility": "off" }] }, { "featureType": "road.arterial", "elementType": "geometry.stroke", "stylers": [{ "color": "#d6d6d6" }] }, { "featureType": "road", "elementType": "labels.icon", "stylers": [{ "visibility": "off" }] }, {}, { "featureType": "poi", "elementType": "geometry.fill", "stylers": [{ "color": "#dadada" }] }]
            };

            // Get the HTML DOM element that will contain your map 
            // We are using a div with id="map" seen below in the <body>
            var mapElement = document.getElementById('map');

            // Create the Google Map using out element and options defined above
            var map = new google.maps.Map(mapElement, mapOptions);

            var marker = new google.maps.Marker({
                position: myLatlng,
                map: map,
                title: ''
            });

            var contentString = $(mapElement).attr('data-text');

            if (contentString) {
                var infowindow = new google.maps.InfoWindow({
                    content: contentString
                });

                mapCenter = map.getCenter();

                google.maps.event.addListener(marker, 'click', function () {
                    infowindow.open(map, marker);
                });
            }
            setTimeout(function () {
                //$('section.map').find('#googlemap').hide();
            }, 1000);

            google.maps.event.addListener(map, 'center_changed', function () {
                //console.log(marker.getPosition());
                window.setTimeout(function () {
                    if (!IsClicked)
                        map.setCenter(marker.getPosition());
                }, 200);
            });
        }
    });
}

google.maps.event.addDomListener(window, 'load', init);

$('a[href=#tab1], a[href=#tg2]').on('click', function () {
    setTimeout(function () {
        google.maps.event.trigger(map, 'resize');
    }, 50);
});
$(".map-button").on("click", function () {
    //$("#googlemap").show("fast");
    $("#googlemap").addClass("openmap");
    $(this).parents('div.map-overlay').hide();

    google.maps.event.trigger(map, 'resize');
    window.setTimeout(function () {
        IsClicked = true;
    }, 500);

    google.maps.event.clearListeners(map, 'center_changed');
    /*$(this).text($(this).text() == "Locate Us on Map" ? "Locate Us on Map" : "Locate Us on Map");
    if($(this).text() == 'Locate Us on Map')
    {
            google.maps.event.trigger(map, 'resize');
    }*/
});
