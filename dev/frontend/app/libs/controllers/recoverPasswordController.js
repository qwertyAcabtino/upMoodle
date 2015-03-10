angular.module('upmApp').controller( 'recoverPasswordCtrl', ['$scope', '$cookies', 'api', 'snackbar', '$location', function($scope, $cookies, api, snackbar, $location) {
	$scope.sendForm = function(email){
		api.recoverPassword(email)
		.success(function(data, status, headers, config) {
			snackbar.message(data.message, 3000);
			$location.path('/login');
		})
		.error(function(data, status, headers, config) {
			snackbar.error(data, 3000);
		});
	}
}]);