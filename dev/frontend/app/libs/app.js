var app = angular.module("upmApp", ['ngRoute', 'ngCookies', 'angular.snackbar', 'ui.bootstrap']);

app
.config(['$routeProvider', '$locationProvider', '$httpProvider',
	function($routeProvider, $locationProvider, $httpProvider) {

		userPromise = ['User', function(User){ return User.get(); }];

		$httpProvider.defaults.withCredentials = true;
		$routeProvider
		.when('/login', {
			templateUrl: 'views/login.html',
			controller: 'loginController'
		})
		.when('/signup', {
			templateUrl: 'views/signup.html',
			controller: 'signUpCtrl',
		})
		.when('/recoverPassword', {
			templateUrl: 'views/recoverPassword.html',
			controller: 'recoverPasswordCtrl',
		})
		.when('/confirm_email/:token', {
			templateUrl: 'views/confirm_email.html',
			controller: 'confirmEmailCtrl',
		})
		.when('/dashboard', {
			templateUrl: 'views/dashboard.html',
			controller: 'dashboardCtrl',
			resolve : {
				userModel : userPromise
			}
		})
		.otherwise({
			redirectTo: '/login'
		});
	}])
.run(function($location, $http, $cookies, api, User){
	api.getUser().
	success(function(data, status, headers, config) {
		User.set(data);
	})	
	.error(function(data, status, headers, config) {
		if( 
			$location.path().indexOf("recoverPassword")!=-1 &&
			$location.path().indexOf("confirm_email")!=-1 &&
			$location.path().indexOf("signup")!=-1 
		)
			$location.path('/login');
	});
});