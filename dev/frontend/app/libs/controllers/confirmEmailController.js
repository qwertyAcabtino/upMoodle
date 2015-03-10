angular.module('upmApp').controller( 'confirmEmailCtrl', ['$scope', '$cookies', 'api', 'snackbar', '$routeParams', '$location', '$timeout', function($scope, $cookies, api, snackbar, $routeParams, $location, $timeout) {
	console.log('confirmEmailCtrl');
	console.log($routeParams.token);
	$scope.confirmed = false;
	api.confirmEmail($routeParams.token)
	.success(function(data, status, headers, config) {
		snackbar.message(data.message, 3000);
		$location.path('/login');
	})
	.error(function(data, status, headers, config) {
		snackbar.error(data, 3000);
		$location.path('/login');
	});
}]);