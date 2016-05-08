 angular.module('upmApp')
 .controller( 'profileCtrl', ['$scope', '$cookies', 'api', 'User', 'userModel', 'snackbar', '$upload', '$location', function($scope, $cookies, api, User, userModel, snackbar, $upload, $location){
 	$scope.editMode = false;
 	$scope.user = User.model;
 	$scope.avatar = $scope.user.profilePic;

 	$scope.update = function (userModel) {
 		api.userMe.update(userModel)
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
 		api.userMe.updateAvatar(avatar[0])
 		.success(function(data, status, headers, config) {
 			snackbar.message(data);
 			User.destroy();
 			User.get().then(function success(response){
				$scope.user = User.get();
			 	$scope.avatar = $scope.user.profilePic;
			});

 		})
 		.error(function(data, status, headers, config) {
 			snackbar.error(data.error, 5000);
 		});  
 	};

 	$scope.upload = function ( avatar ) {
 		if ( avatar ) {
 			$scope.updateAvatar(avatar);
 		}
 	};

 	$scope.$watch('newAvatar', function () {
 		$scope.upload($scope.newAvatar);
 	});


 	var updateUserSuccess = function (data) {
 		snackbar.message(data);
 		$scope.editMode = false;
 	};
 }]);  