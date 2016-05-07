 angular.module('upmApp')
 .controller( 'profileCtrl', ['$scope', '$cookies', 'api', 'User', 'userModel', 'snackbar', '$upload', '$location', function($scope, $cookies, api, User, userModel, snackbar, $upload, $location){
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

 	$scope.updateAvatar = function ( avatar ) {
 		api.updateAvatar(avatar[0])
 		.success(function(data, status, headers, config) {
 			snackbar.message(data);
 			User.destroy();
 			User.get().then(function success(response){
				$scope.user = User.get();
			 	$scope.profilePic = api.getPic( $scope.user.profilePic );
			});

 		})
 		.error(function(data, status, headers, config) {
 			snackbar.error(data.error, 5000);
 		});  
 	};

 	$scope.upload = function ( profilePic ) {
 		if ( profilePic ) {
 			$scope.updateAvatar(profilePic);
 		}
 	};

 	$scope.$watch('newProfilePic', function () {
 		$scope.upload($scope.newProfilePic);
 	});


 	var updateUserSuccess = function (data) {
 		snackbar.message(data);
 		$scope.editMode = false;
 	};
 }]);  