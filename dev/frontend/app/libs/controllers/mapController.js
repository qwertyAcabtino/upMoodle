var map;
//This point is the center of Madrid.
var center = new google.maps.LatLng(40.41, -3.69); 
var markers = [];

angular.module('upmApp').controller( 'mapController', ['$scope', '$http', 'api', function($scope, $http, api){
	
	$scope.actives = [];
	$scope.searchResults = [ ];

	$scope.searchKeyword = function(){
		if( $scope.keyword != "" && $scope.keyword != " " && $scope.keyword !== undefined  ){
			$scope.actives = [];
			_resetMarkers();
			var request = {
			    location : center,
			    radius: 2000,
			    keyword: $scope.keyword
			  };
			var service = new google.maps.places.PlacesService(map);
			service.nearbySearch(request, $scope.searchRequestCallback);
		}
	}
	
	$scope.searchRequestCallback = function(results, status) {
		$scope.updateList(results);
		$scope.updateMap(results);
	}	

	$scope.updateList = function(results){
		$scope.$apply(function(){
			$scope.searchResults = results;
			for( i=0; i< $scope.searchResults.length; i++ ){
				var id = $scope.searchResults[i].id;
				$scope.actives[ id ] = false;
			}			
		});
	}

	$scope.updateMap = function(results){
		for(i=0; i< results.length; i++){
			var marker = createGmapsMarker(results[i]);
			markers.push(marker);
		}
	}

	$scope.setListitemActive = function(id){
		$scope.setListitemActiveById(id);		
	}

	$scope.listitemClickEvent = function(id){
		$scope.setListitemActive(id);
		$scope.triggerMarkerEvent(id);
	}

	$scope.triggerMarkerEvent = function(id) {
		index = _getMarkerPosition(id);
		google.maps.event.trigger( markers[ index ], 'click');
	}

	$scope.setListitemActiveById = function (liId){
		$scope.$apply(function(){
			for( i=0; i< $scope.searchResults.length; i++ ){
				var id = $scope.searchResults[i].id;
				if( id == liId )
					$scope.actives[ id ] = true;
				else
					$scope.actives[ id ] = false;
			}
		});
	}

	function centerAtMarkerAndSetListitemActive (marker) {
	    map.setZoom(18);
	    map.setCenter(marker.getPosition());
	    $scope.setListitemActive(marker.id);	
	}

	function createGmapsMarker(data){
		var marker = new google.maps.Marker({
		    map: map,
		    icon: data.image,
		    title: data.name,
		    position: data.geometry.location,
		    id : data.id
		});
		google.maps.event.addListener(marker, 'click', function(){
			centerAtMarkerAndSetListitemActive(marker);
		});	
	return marker;
	}

	function _getMarkerPosition(id){
		for( i=0; i< markers.length; i++){
			if(markers[i].id == id)
				break;
		}
	return i;
	}

	function _resetMarkers () {
		for (var i = 0, marker; marker = markers[i]; i++){
		    marker.setMap(null);
	    }
	}

}]);

// function loadMap($scope){
// 	var mapOptions = {
// 	zoom: 5,
// 	center: center
// 	};
// 	map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
// }
// google.maps.event.addDomListener(window, 'load', loadMap);