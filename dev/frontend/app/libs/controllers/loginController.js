
angular.module('upmApp').controller( 'loginController', ['$scope', '$cookies', 'api', function($scope, $cookies, api){

	$scope.text = "Hola mundo";
	api.login('viperey@eui.upm.es', 'qwerqwer')
		.success(function(data, status, headers, config) {
					//TODO. Set user at some place.
			console.log('ok');
			console.log(data);
		})
		.error(function(data, status, headers, config) {
			console.log('error');
		});
}]);