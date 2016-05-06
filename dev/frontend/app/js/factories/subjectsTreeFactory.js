angular.module('upmApp').factory('SubjectsTree', ['$location', 'api', function($location, api){
	
	var returno = {
		model : undefined, 

	    get : function(){
	    	if( this.model===undefined )
	    		return api.subjectsTree()
				.then(
					function success(response) { 
						returno.model = response.data[0];
						return returno.model; 
					},
					function error(){
						return null; 
					}
				);
    		else	
    			return this.model;
	    },

	    set : function(model){
	    	this.model = model;
	    },

		destroy : function(){
			returno.model = undefined;
		},

		getLevel : function(id, node){
			var that = this;
			node = node || this.model;
			if(node.id == id)
				return node;
			else if(node.children){
				var returno = null;
				angular.forEach(node.children, function(children, index){
					if(!returno){
						candidateNode = that.getLevel(id, children);
						if( candidateNode )
							returno = candidateNode;
					}
				});
				return returno;
			} 
			return null;
		}
	};
	return returno;
}]);