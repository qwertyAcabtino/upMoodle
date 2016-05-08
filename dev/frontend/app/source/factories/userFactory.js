angular.module('upmApp').factory('User', ['$location', 'api', function($location, api){
	var returno = {
		model : undefined, 

	    destroy : function(){
	    	this.model = undefined;
	    },

	    get : function(){
	    	if( this.model===undefined )
	    		return api.userMe.get()
				.then(
					function success(response) { 
						returno.model = response.data;
						returno.model.profilePic = 'http://127.0.0.1:8000/' + returno.model.profilePic;
						return returno.model; 
					},
					function error(){
						$location.path('/login');
						return false; 
					}
				);
    		else	
    			return this.model;
	    },

	    set : function(model){
	    	this.model = model;
	    },

	    isSignedInSubject : function(id){
    		returno = false;
			angular.forEach(this.model.subjects, function(value,index){
                if( value.id === id ){
                	returno = true;
                }
            });
	    	return returno;
	    }
	};

	return returno;
}]);