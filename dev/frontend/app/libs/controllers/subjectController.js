 angular.module('upmApp')
 .controller( 'subjectCtrl', 
 	['$scope', '$cookies', 'api', 'User', 'userModel', '$location', 'SubjectsTree', '$modal', 'snackbar', '$routeParams', '$upload',
 	function($scope, $cookies, api, User, userModel, $location, SubjectsTree, $modal, snackbar, $routeParams, $upload){

 		$scope.getFileTypes = function(){
 			api.fileTypesGet()
 			.success(function(data, status, headers, config){
 				$scope.fileTypes = data;	
 			})
 			.error(function(data, status, headers, config) {
 				console.log(data.error);
 			}); 			
 		}

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
			$scope.getFileTypes();
 			$scope.getSubjectFiles();
 			$scope.filetTypeFilter = {
 			};
 		}

 		$scope.openEditFileModal = function(file){
 			var modalInstance = $modal.open({
 				templateUrl: 'views/_modalEditFileInfo.html',
 				controller: 'ModalEditFileInfo',
 				size: 'lg',
 				resolve: {
 					file: function(){ 
 						return file 
 					},
					fileTypes : function(){ 
						return $scope.fileTypes; 
					}
				}
 			});

 			modalInstance.result.then(function (message) {
 				snackbar.message(message, 5000);
 				$scope.getSubjectFiles();
 			}, function () {
 				$scope.getSubjectFiles();
 			});
 		};

 		$scope.openNewFileModal = function(file){
 			var modalInstance = $modal.open({
 				templateUrl: 'views/_modalNewFile.html',
 				controller: 'ModalNewFileInfo',
 				size: 'lg',
 				resolve: {
 					file: function(){ 
 						return file 
 					},
					fileTypes : function(){ 
						return $scope.fileTypes; 
					},
					subject : function(){
						return $scope.subject;
					}
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
 			if (files && files.length) {
 				for (var i = 0; i < files.length; i++) {
 					var file = files[i];
 					$scope.openNewFileModal(file);
 				}
 			}
 		};

 		$scope.$watch('files', function () {
 			$scope.upload($scope.files);
 		});

 		$scope.init();
 	}]);  


angular.module('upmApp').controller('ModalNewFileInfo', function ($scope, $modalInstance, file, fileTypes, api, snackbar, User, subject) {

	$scope.getFilesFileTypeIndex = function(){
		for(var i=0; i<$scope.fileTypes.length; i++){
			if( $scope.fileTypes[i].id===$scope.file.fileType.id)
				return i;
		}
	return 0;
	}

	$scope.uploadNewFile = function (newFileInfo) {
		api.uploadFile( $scope.newFile, {userId : User.get().id, subjectId : $scope.subject.id, fileInfo: newFileInfo, fileType: $scope.fileTypeSelected})
		.success(function (data) {
			$modalInstance.close(data);
		})
 		.error(function(data, status, headers, config) {
	       snackbar.error(data.error);
	    });
	}

	$scope.init = function(){
		$scope.newFile = file;
		$scope.newFileInfo = {};
		$scope.newFileInfo.name = file.name;
		$scope.newFileInfo.text = "";
		$scope.fileTypes = fileTypes;
		$scope.filesFileTypeIndex = 0;
		$scope.subject = subject;
	}

	$scope.init();
});


angular.module('upmApp').controller('ModalEditFileInfo', function ($scope, $modalInstance, file, fileTypes, api, snackbar) {

	$scope.getFilesFileTypeIndex = function(){
		for(var i=0; i<$scope.fileTypes.length; i++){
			if( $scope.fileTypes[i].id===$scope.file.fileType.id)
				return i;
		}
	return 0;
	}

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
		newFileInfo.fileType = $scope.fileTypeSelected;
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
		$scope.fileTypes = fileTypes;
		$scope.filesFileTypeIndex = $scope.getFilesFileTypeIndex();
	}

	$scope.init();
});