angular.module('upmApp').factory('api', function($http, $cookies, $upload, $window){
	var base_url = 'http://127.0.0.1:8000/';
	var user_pics_url = base_url + "media/";

	return {

		getPic : function(url){
			return user_pics_url + url;			
		},

		getUser : function(){
			return $http({ 
				method: 'GET', 
				url:  base_url + 'user/'
			});
		},

		updateUserSubjects : function (subjects) {
			return $http({ 
				method: 'post', 
				url:  base_url + 'user/subjects/',
				headers: {'Content-Type': 'application/x-www-form-urlencoded'},
				transformRequest: function(obj) {
					var str = [];
					for(var p in obj)
						str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
					return str.join("&");
				},
				data : {ids: subjects || [] }
			});
		},

		updateUser : function(user){
			return $http({ 
				method: 'POST', 
				url:  base_url + 'user/',
				headers: {'Content-Type': 'application/x-www-form-urlencoded'},
				transformRequest: function(obj) {
					var str = [];
					for(var p in obj)
						str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
					return str.join("&");
				},
				data: user.password ? 
				{email: user.email, name: user.name, nick: user.nick, password: user.password} :
				{email: user.email, name: user.name, nick: user.nick}
			});
		},

		login : function(userEmail, userPassword){
			return $http({ 
				method: 'post', 
				url:  base_url + 'login/',
				headers: {'Content-Type': 'application/x-www-form-urlencoded'},
				transformRequest: function(obj) {
					var str = [];
					for(var p in obj)
						str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
					return str.join("&");
				},
				data : {email: userEmail, password: userPassword}
			});
		},

		signup : function(email, password, nick){
			return $http({ 
				method: 'post', 
				url:  base_url + 'signup/',
				headers: {'Content-Type': 'application/x-www-form-urlencoded'},
				transformRequest: function(obj) {
					var str = [];
					for(var p in obj)
						str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
					return str.join("&");
				},
				data : {email: email, password: password, nick: nick}
			});
		},

		logout : function(){
			return $http({ 
				method: 'POST', 
				url:  base_url + 'logout/'
			});	
		},

		recoverPassword : function(email){
			return $http({ 
				method: 'POST', 
				url:  base_url + 'recover_password/',
				headers: {'Content-Type': 'application/x-www-form-urlencoded'},
				transformRequest: function(obj) {
					var str = [];
					for(var p in obj)
						str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
					return str.join("&");
				},
				data: {email: email}
			});	
		},

		confirmEmail : function(token){  
			return $http({     
				method: 'GET',      
				url:  base_url + 'confirm_email/' + token +"/"
			});
		},

		subjectsTree : function(){
			return $http({
				method: 'GET',
				url: base_url + 'subjectsTree/'
			});
		},

		notesByLevelId : function(level, recursive){
			var recuriveIn = recursive || false;
			return $http({
				method: 'GET',
				url: base_url + 'note/level/' + level +"/" + "?recursive="+recursive
			});
		},

		notePost : function(note){
			return $http({
				method: 'post', 
				url:  base_url + 'note/',
				headers: {'Content-Type': 'application/x-www-form-urlencoded'},
				transformRequest: function(obj) {
					var str = [];
					for(var p in obj)
						str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
					return str.join("&");
				},
				data : {text: note.text, topic: note.topic, level_id: note.level_id}
			});
		},

		subjectFiles : function(subjectId){
			return $http({
				method: 'GET',
				url: base_url + 'files/subject/' + subjectId +"/"
			});
		},

		fileTypesGet : function(){
			return $http({
				method: 'GET',
				url: base_url + 'fileTypes/'
			});
		},

		uploadFile : function(file, data){
			return $http({
				method: 'POST',
				url: base_url + 'file/f/',
				headers: {
					'Content-Type': 'multipart/form-data'
				},
				data: {
					subject_id: data.subjectId,
					uploader_id : data.userId,
					file: file
				},
				transformRequest: function (data, headersGetter) {
					var formData = new FormData();
					angular.forEach(data, function (value, key) {
						formData.append(key, value);
					});

					var headers = headersGetter();
					delete headers['Content-Type'];

					return formData;
				}
			});
		},

		filePost : function(file){
			return $http({
				method: 'post', 
				url:  base_url + 'file/' + file.id +'/',
				headers: {'Content-Type': 'application/x-www-form-urlencoded'},
				transformRequest: function(obj) {
					var str = [];
					for(var p in obj)
						str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
					return str.join("&");
				},
				data : {
					text: file.text, 
					name: file.name,
					fileType_id : file.fileType.id
				}
			});
		},

		fileGet : function(fileId){
			return $http({
				method: 'GET',
				url: base_url + 'file/' + fileId +'/',
			});
		},

		fileDownload : function(id){
			var url = base_url + 'file/f/' + id +"/";
			$window.open( url );
		},

		fileDelete : function(fileId){
			return $http.delete(base_url + 'file/' + fileId +'/');
		},
	}
});  