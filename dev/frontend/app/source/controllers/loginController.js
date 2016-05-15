
angular.module('upmApp').controller( 'loginController', ['$scope', '$cookies', 'api', 'User', '$location', 'snackbar', function($scope, $cookies, api, User, $location, snackbar){

	$scope.backgroundStyle = {background: '#000'};
	
	$scope.sendForm = function(user){
		var email = (user && user.email ) ? user.email : null;
		var password = (user && user.password ) ? user.password : null;
		api.auth.login( email, password )
			.success(function(data, status, headers, config) {
				snackbar.message(data.message);
				$location.path('/dashboard');
			})
			.error(function(data, status, headers, config) {
				snackbar.error(data);
			});
	};

	$scope.signIn = function(){
		$location.path('/signup');
	};

	$scope.recoverPassword = function(){
		$location.path('/recoverPassword');
	};
}]);