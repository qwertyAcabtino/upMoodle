
angular.module('upmApp').controller( 'loginController', ['$scope', '$cookies', 'api', 'User', '$location', 'snackbar', function($scope, $cookies, api, User, $location, snackbar){

	$scope.sendForm = function(user){
		var email = (user && user.email ) ? user.email : null;
		var password = (user && user.password ) ? user.password : null;
		api.login( email, password )
			.success(function(data, status, headers, config) {
				snackbar.message(data.message);
				$scope.getUser();
			})
			.error(function(data, status, headers, config) {
				snackbar.error(data.error);
			});
	};

	$scope.signIn = function(){
		$location.path('/signup');
	};

	$scope.recoverPassword = function(){
		$location.path('/recoverPassword');
	};

	$scope.getUser = function(){
		api.getUser()
			.success(function(data, status, headers, config){
				// User.update(data);
				$location.path('/dashboard');
			})
			.error(function(data, status, headers, config) {
				snackbar.error(data.error);
			});
	};
}]);