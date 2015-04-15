 angular.module('upmApp')
 .controller( 'subjectCtrl', 
 	['$scope', '$cookies', 'api', 'User', 'userModel', '$location', 'SubjectsTree', '$modal', 'snackbar', '$routeParams', '$upload',
 	function($scope, $cookies, api, User, userModel, $location, SubjectsTree, $modal, snackbar, $routeParams, $upload){

 		$scope.getSubjectFiles = function(){
 			api.subjectFiles( $scope.subject.id )
 			.success(function(data, status, headers, config){
 				$scope.subject.files = data;	
 			})
 			.error(function(data, status, headers, config) {
 				console.log(data.error);
 			}); 			
 		}

 		$scope.init = function(){
 			$scope.subjectId = $routeParams.id;
 			$scope.subject = SubjectsTree.getLevel( $scope.subjectId ); 
 			$scope.getSubjectFiles();
 		}

 		$scope.openEditFileModal = function(file){
 			var modalInstance = $modal.open({
 				templateUrl: 'views/_modalEditFileInfo.html',
 				controller: 'ModalEditFileInfo',
 				size: 'lg',
 				resolve: {
 					file: function(){ return file },
					}
 			});

 			modalInstance.result.then(function (message) {
 				snackbar.message(message, 5000);
 				$scope.getSubjectFiles();
 			}, function () {
 				$scope.getSubjectFiles();
 			});
 		};

 		$scope.upload = function (files) {
 			console.log("$scope.upload($scope.files);");
 			if (files && files.length) {
 				for (var i = 0; i < files.length; i++) {
 					var file = files[i];
 					console.log(file);
 					api.uploadFile(file, {userId : User.get().id, subjectId : $scope.subject.id})
					.success(function (data) {
						$scope.getSubjectFiles();
		 				snackbar.message(data);
 					})
			 		.error(function(data, status, headers, config) {
				       snackbar.error(data.error);
				    });
 				}
 			}
 		};

 		$scope.$watch('files', function () {
 			$scope.upload($scope.files);
 		});

 		$scope.init();
 	}]);  

angular.module('upmApp').controller('ModalEditFileInfo', function ($scope, $modalInstance, file, api, snackbar) {

	$scope.file = file;
	$scope.editMode = false;
	$scope.newFileInfo = angular.copy($scope.file);

	$scope.downloadFile = function(file){
		api.fileDownload(file.id);
	}

	$scope.deleteFile = function(file){
		api.fileDelete(file.id)
		.success(function (data) {
			$modalInstance.close(data.message);  
		})
 		.error(function(data, status, headers, config) {
	       snackbar.error(data.error);
	    });
	}

	$scope.saveFileInfo = function(newFileInfo){
		api.filePost(newFileInfo)
		.success(function (data) {
			$scope.saveFileInfoCallback(data.message);
		})
 		.error(function(data, status, headers, config) {
	       snackbar.error(data.error);
	       $scope.newFileInfo = angular.copy($scope.file);
	    });
	}

	$scope.saveFileInfoCallback = function(message){
		$scope.getFileInfo(file.id, message);
		$scope.editMode = false;
	}

	$scope.getFileInfo = function (fileId, previousMessage) {
		api.fileGet(fileId)
		.success(function (data) {
			if( previousMessage )
				snackbar.message( previousMessage, 5000);
			$scope.init( data[0] );
			//TODO. Update main view.
		})
 		.error(function(data, status, headers, config) {
	       snackbar.error(data.error);
	       $scope.newFileInfo = angular.copy($scope.file);
	    });
	}

	$scope.init = function ( newFile ) {
		$scope.file = newFile || file;
		$scope.editMode = false;
		$scope.newFileInfo = angular.copy($scope.file);
	}
});