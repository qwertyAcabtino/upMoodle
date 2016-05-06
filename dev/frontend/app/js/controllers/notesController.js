 angular.module('upmApp')
 .controller( 'notesCtrl', 
    ['$scope', '$cookies', 'api', 'User', 'userModel', '$location', 'SubjectsTree', '$modal', 'snackbar', 
    function($scope, $cookies, api, User, userModel, $location, SubjectsTree, $modal, snackbar){

 	$scope.getNotesByLevelId = function ( levelId, recursive ) {
 		api.notesByLevelId(levelId, recursive || false)
 		.success(function(data, status, headers, config){
       $scope.notes = data;	
     })
 		.error(function(data, status, headers, config) {
       console.log(data.error);
     });
 	};


  $scope.openLevelModal = function () {

    var modalInstance = $modal.open({
      templateUrl: 'views/_modalSubjectsList.html',
      controller: 'ModalLevelsLists',
      size: 'lg',
      resolve: {
        levels: function () {
          return SubjectsTree.get();
        }
      }
    });

    modalInstance.result.then(function (selectedItem) {
      $scope.subjectsTree = selectedItem || SubjectsTree.get();
      $scope.getNotesByLevelId($scope.subjectsTree.id, true);
    }, function () {
    });
  };

  $scope.openNewNoteModal = function(){
    var modalInstance = $modal.open({
      templateUrl: 'views/_modalNewNote.html',
      controller: 'ModalNewNote',
      size: 'lg',
      resolve: {
        levels: function () {
          return SubjectsTree.get();
        }
      }
    });

    modalInstance.result.then(function (message) {
      snackbar.message(message, 5000);
      $scope.getNotesByLevelId($scope.subjectsTree.id, true);
    }, function () {
    });
  };

  $scope.openEditNoteModal = function(note){
    var modalInstance = $modal.open({
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
      snackbar.message(message, 5000);
      $scope.getNotesByLevelId($scope.subjectsTree.id, true);
    }, function () {
    });
  };

  $scope.init = function(){
    $scope.subjectsTree = SubjectsTree.get();
    $scope.getNotesByLevelId( $scope.subjectsTree.id, true );
  };

 $scope.subjectsTree = {};
 $scope.notes = [];
 $scope.init();
}]);  

angular.module('upmApp').controller('ModalLevelsLists', function ($scope, $modalInstance, levels) {
  $scope.root = levels;
  $scope.filterByLevel = function(level) {
    $modalInstance.close(level);
  };
}); 

angular.module('upmApp').controller('ModalEditNote', function ($scope, $modalInstance, levels, api, snackbar, note, SubjectsTree, levelsUnested) {

  $scope.getLevelsDropdown = function(node, depthParam){
    var depth = depthParam || 0; 
    node.depth = depth;
    var returningNode = {};
    returningNode.name = repeat(' · ', depth) + node.name;
    returningNode.depth = depth;
    returningNode.id = node.id;
    returningNode.parent = node.parent;
    if( !node.children ){
      return returningNode;
    }

    var levelsUnested = [returningNode];
    for(var i=0; i<node.children.length; i++){
      var returno = $scope.getLevelsDropdown(node.children[i], depth+1);
      if( Array.isArray(returno) )
        levelsUnested = levelsUnested.concat( returno ); 
      else 
        levelsUnested.push( returno );  
    }
    return levelsUnested;

    function repeat (string, num) {
      for(var i=1; i<num; i++){
        string += string;
      }
      return string;
    }
  };

  $scope.getLevelIndex = function () {
    for(var i=0; i<$scope.levelsUnested.length; i++){
      if( $scope.levelsUnested[i].id===$scope.note.level.id)
        return i;
    }
  return 0;
  };

  $scope.saveNewNote = function (newNote) {
    api.notePut( newNote )
    .success(function (data) {
      $modalInstance.close(data);
    })
    .error(function(data, status, headers, config) {
         snackbar.error(data.error);
         $scope.newNote = angular.copy($scope.note);
      });
  };

  $scope.deleteNote = function(){
    api.noteDelete($scope.note.id)
    .success(function (data) {
      $modalInstance.close(data.message);  
    })
    .error(function(data, status, headers, config) {
         snackbar.error(data.error);
      });
  };

  $scope.init = function ( newNote ) {
      $scope.note = newNote || note;
      $scope.newNote = angular.copy( $scope.note );
      $scope.levels = levels;
      $scope.editMode = false;
      $scope.levelsUnested = $scope.getLevelsDropdown($scope.levels);
      $scope.levelIndex = $scope.getLevelIndex();
  };

  $scope.init();
});

angular.module('upmApp').controller('ModalNewNote', function ($scope, $modalInstance, levels, api, snackbar) {

  $scope.post = function(note) {
    note = note || {};
    note.topic = note.topic || "";
    note.text = note.text || "";
    note.level = note.level || {};
    note.level_id = note.level.id || -1;
    api.notePost(note)
    .success(function(data, status, headers, config) {
      $modalInstance.close(data.message);   
    })
    .error(function(data, status, headers, config) {
      snackbar.error(data.error, 5000);
    });  
  };

  $scope.getLevelsDropdown = function(node, depthParam){
    var depth = depthParam || 0; 
    node.depth = depth;
    var returningNode = {};
    returningNode.name = repeat(' · ', depth) + node.name;
    returningNode.depth = depth;
    returningNode.id = node.id;
    returningNode.parent = node.parent;
    if( !node.children ){
      return returningNode;
    }

    var levelsUnested = [returningNode];
    for(var i=0; i<node.children.length; i++){
      var returno = $scope.getLevelsDropdown(node.children[i], depth+1);
      if( Array.isArray(returno) )
        levelsUnested = levelsUnested.concat( returno ); 
      else 
        levelsUnested.push( returno );  
    }
    return levelsUnested;

    function repeat (string, num) {
      for(var i=1; i<num; i++){
        string += string;
      }
      return string;
    }
  };

  $scope.levelsUnested = $scope.getLevelsDropdown(levels);
});
