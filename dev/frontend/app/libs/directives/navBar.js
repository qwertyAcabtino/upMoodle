angular.module('upmApp').directive('navbar', function(User){

	return {
		restrict: 'EA',
		templateUrl: 'views/navbar.html',
		controller: function($scope, api, $location) {
			$scope.user = User.model;
			$scope.logout = function() {
				api.logout().
				success(function(data, status, headers, config) {
					User.destroy();
					$location.path('/login'); 
				})	
				.error(function(data, status, headers, config) {
				}); 
			};
		} 
	}
}); 