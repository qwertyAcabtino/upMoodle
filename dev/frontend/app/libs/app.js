var app = angular.module("upmApp", ['ngRoute', 'ngCookies']);

app
.config(['$routeProvider', '$locationProvider', '$httpProvider',
	function($routeProvider, $locationProvider, $httpProvider) {
		$httpProvider.defaults.withCredentials = true;
		$routeProvider
		.when('/login', {
			templateUrl: 'views/login.html',
			controller: 'loginController'
		})
		.when('/map', {
			templateUrl: 'views/map.html',
			controller: 'mapController'
		})
		.otherwise({
			redirectTo: '/login'
		});
	}])
.run(function($location, $http, $cookies, api){
	api.getUser().
	success(function(data, status, headers, config) {
				//TODO. Set user at some place.
			})
	.error(function(data, status, headers, config) {
		$location.path('/login');
	});
});