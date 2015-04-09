 angular.module('upmApp')
.controller( 'profileCtrl', ['$scope', '$cookies', 'api', 'User', 'userModel', 'snackbar', function($scope, $cookies, api, User, userModel, snackbar){
	$scope.editMode = false;
	$scope.user = User.model;
	$scope.profilePic = api.getPic( $scope.user.profilePic );

	$scope.update = function (userModel) {
		api.updateUser(userModel)
			.success(function(data, status, headers, config){
				snackbar.message(data);
				$scope.editMode = false;
				delete $scope.user.password;
 			})
			.error(function(data, status, headers, config) {
				snackbar.error(data.error);
				delete $scope.user.password;
				User.destroy();
				User.get().then(function success(response){
					$scope.user = User.get(); //Data gets reseted.			
				});
			});
	};

	var updateUserSuccess = function (data) {
		snackbar.message(data);
		$scope.editMode = false;
	};
}]);  