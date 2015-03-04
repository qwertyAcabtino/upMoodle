
angular.module('upmApp').controller( 'loginController', ['$scope', '$cookies', 'api', 'User', '$location', 'snackbar', function($scope, $cookies, api, User, $location, snackbar){

	$scope.text = "Hola mundo";

	$scope.sendForm = function(user){
		api.login( user.email, user.password )
			.success(function(data, status, headers, config) {
				snackbar.message(data.message);
				$scope.getUser();
			})
			.error(function(data, status, headers, config) {
				snackbar.error(data.error);
			});
	}

	$scope.signIn = function(){
		$location.path('/signin');
	}

	$scope.getUser = function(){
		api.getUser()
			.success(function(data, status, headers, config){
				User.update(data);
				$location.path('/dashboard');
			})
			.error(function(data, status, headers, config) {
				console.log('error');
			});
	}
}]);