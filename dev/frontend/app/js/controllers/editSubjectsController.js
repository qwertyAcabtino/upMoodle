 angular.module('upmApp')
 .controller( 'editSubjectsCtrl', 
 	['$scope', '$cookies', 'api', 'User', 'userModel', 'snackbar', '$location', 'SubjectsTree',
 	function($scope, $cookies, api, User, userModel, snackbar, $location, SubjectsTree){

 		$scope.isAUserSubject = function (subject) {
 			subject.signedUp = User.isSignedInSubject(subject.id);
 			return User.isSignedInSubject(subject.id);
 		};

 		$scope.getSubjectsCheckedList = function(){
 			var subjectsCheck = [];
 			angular.forEach($scope.university.children, function(career, index){
 				angular.forEach(career.children, function(course, index){
 					angular.forEach(course.children, function(subject, index){
 						if(subject.signedUp)
 							subjectsCheck.push(subject.id); 
 					});
 				});
 			});
 			return subjectsCheck;
 		};

 		$scope.updateUserSubjects = function(){
 			var subjectsCheck = $scope.getSubjectsCheckedList();
 			api.updateUserSubjects(subjectsCheck)
 			.success(function(data, status, headers, config) {
 				$scope.updateUserSubjectsCallback(data);
 			})
 			.error(function(data, status, headers, config) {
 				snackbar.error(data.error);
 			});
 		};

 		$scope.updateUserSubjectsCallback = function(message){
 			snackbar.message(message);
 			api.getUser().
 			success(function(data, status, headers, config) {
 				User.set(data);
 				$location.path('/subjects');
 			});
 		};

 		$scope.init = function(){
	 		$scope.university = SubjectsTree.get();
 		};

 		$scope.init();

 	}]);  