angular.module('upmApp').directive('navbar', function(){

	return {
		restrict: 'EA',
		templateUrl: 'views/navbar.html',
		controller: function($scope, api, $location, User) {
			$scope.user = User.model;
			$scope.profilePic = api.getPic( $scope.user.profilePic );
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
	};
}); 