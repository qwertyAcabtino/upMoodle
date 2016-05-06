 angular.module('upmApp')
.controller( 'subjectsCtrl', ['$scope', '$cookies', 'api', 'User', 'userModel', '$location', function($scope, $cookies, api, User, userModel, $location){
 	
 	$scope.navigateTo = function (id) {
		var candidate = $scope.getNodeAndStack($scope.subjectsTree, id);
		var node = candidate.node;
		if( node.type==="subject" )
			$location.path('/subject/'+id);
		else{
			$scope.showingSubjectsTree = node;
			$scope.pushStack( candidate.stack );
		}
 	};

 	$scope.getNodeAndStack = function (node, id, candidateStack) {
 		var stack = candidateStack || [];
 		if(node.id === id){
 			composedReturn = {};
 			composedReturn.node = node;
 			composedReturn.stack = stack;
 			return composedReturn;
 		}
 		else if(node.children){
 			var returno = null;
 			angular.forEach(node.children, function(children, index){
 				if(!returno){
					candidateNode = $scope.getNodeAndStack(children, id, stack);
					if( candidateNode ){
			 			stack.push( node );
						returno = candidateNode;
					}
				}
 			});
 			return returno;
		} 
	return null;
 	};

 	$scope.getRootStackNode = function () {
		var rootStackNode = {};
 		rootStackNode.name = "..";
 		rootStackNode.id = null;
		var stackArray = [];
		stackArray.push(rootStackNode);
		return stackArray;
 	};

 	$scope.pushStack = function (stack) {
		$scope.returnStack = stack;
		$scope.returnStack.unshift($scope.showingSubjectsTree);
		$scope.returnStack.reverse();
 	};

	$scope.showingSubjectsTree = {};
	$scope.subjectsTree = {};
	$scope.returnStack = {};

 	api.subjectsTree()
 	.success(function(data, status, headers, config){
		$scope.subjectsTree = data[0];
		$scope.navigateTo($scope.subjectsTree.id);
 	})
 	.error(function(data, status, headers, config) {
 		$location.path('/dashboard/');
 	});
}]);  