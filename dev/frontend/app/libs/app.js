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
		User.update(data);
	})	
	.error(function(data, status, headers, config) {
		$location.path('/login');
	});
});