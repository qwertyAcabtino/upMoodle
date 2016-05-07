angular.module('upmApp').controller( 'signUpCtrl', ['$scope', '$cookies', 'api', 'snackbar', function($scope, $cookies, api, snackbar) {
	$scope.signedup = false;
	$scope.signUp = function(user){
		api.auth.signup( user )
			.success(function(data, status, headers, config) {
				$scope.signedup = true;
			})
			.error(function(data, status, headers, config) {
				snackbar.error(data.error, 5000); 
			});
	};
}]);