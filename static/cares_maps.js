function initMap() {



{%for object in object_list %}
    var mapCoords_{{object.id}} = { lat: {{object.lat}}, lng: {{object.lng}} };

    var map_{{object.id}} = new google.maps.Map(document.getElementById('gmap_canvas_{{object.id}}'), {
      zoom:14,
      scrollwheel:false,
      draggable: false,
      center: mapCoords_{{object.id}},
      mapTypeId: google.maps.MapTypeId.ROADMAP
    });

    var marker = new google.maps.Marker({
      clickable: false,
      position: mapCoords_{{object.id}},
      map: map_{{object.id}}
    });
    {% endfor %}

}
