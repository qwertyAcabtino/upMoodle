 angular.module('upmApp')
.controller( 'profileCtrl', ['$scope', '$cookies', 'api', 'User', 'userModel', function($scope, $cookies, api, User, userModel){
	$scope.user = User.model;
	$scope.profilePic = api.getPic( $scope.user.profilePic );
	console.log( "$scope.profilePic" );
	console.log( $scope.profilePic );
}]);  