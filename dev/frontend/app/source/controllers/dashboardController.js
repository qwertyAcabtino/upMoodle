 angular.module('upmApp')
 .controller( 'dashboardCtrl', 
 	['$scope', '$cookies', 'api', 'User', 'userModel', '$uibModal', 'snackbar', 'SubjectsTree',
 	function($scope, $cookies, api, User, userModel, $uibModal, snackbar, SubjectsTree){

 		$scope.getLastestNotes = function(){
 			api.notes.latest()
 			.success(function(data, status, headers, config){
 				$scope.latestNotes = data.data;
 			});
 		};

 		$scope.getLastestFiles = function(){
 			api.files.latest()
 			.success(function(data, status, headers, config){
 				$scope.latestFiles = data.data;
 			});
 		};

 		$scope.getFileTypes = function(){
 			api.filetype.getAll()
 			.success(function(data, status, headers, config){
 				$scope.fileTypes = data.data;	
 			})
 			.error(function(data, status, headers, config) {
 				console.log(data);
 			}); 			
 		};


 		$scope.init = function(){
 			$scope.getFileTypes();
 			$scope.getLastestNotes();
 			$scope.getLastestFiles();
 		};

 		$scope.openEditNoteModal = function(note){
 			var modalInstance = $uibModal.open({
 				templateUrl: 'views/_modalEditNote.html',
 				controller: 'ModalEditNote',
 				size: 'lg',
 				resolve: {
 					levels: function () {
 						return SubjectsTree.get();
 					},
 					note : function(){
 						return note;
 					},
 					levelsUnested: function () {
 						return $scope.levelsUnested; 
 					}
 				}
 			});

 			modalInstance.result.then(function (message) {
 			});
 		};

 		$scope.openEditFileModal = function(file){
 			var modalInstance = $uibModal.open({
 				templateUrl: 'views/_modalEditFileInfo.html',
 				controller: 'ModalEditFileInfo',
 				size: 'lg',
 				resolve: {
 					file: function(){ 
 						return file;
 					},
 					fileTypes : function(){ 
 						return $scope.fileTypes; 
 					}
 				}
 			});

 			modalInstance.result.then(function (message) {
 				snackbar.message(message.message, 3000);
 				$scope.getSubjectFiles();
 			}, function () {
 				$scope.getSubjectFiles();
 			});
 		};

 		$scope.init();
 	}]);