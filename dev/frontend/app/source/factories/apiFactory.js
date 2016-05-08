angular.module('upmApp').factory('api', function($http, $cookies, $upload, $window){
	var base_url = 'http://127.0.0.1:8000/';
	var user_pics_url = base_url;

	return {

		auth : {

			login : function(userEmail, userPassword){
				return $http({ 
					method: 'POST', 
					url:  base_url + 'auth/login/',
					headers: {'Content-Type': 'application/json'},
					data : {
						email: userEmail, 
						password: userPassword
					}
				});
			},

			logout : function(){
				return $http({ 
					method: 'POST', 
					url:  base_url + 'auth/logout/'
				});	
			},

			signup : function(user){
				return $http({ 
					method: 'post', 
					url:  base_url + 'auth/signup/',
					headers: {'Content-Type': 'application/json'},
					data : {
						email: user.email, 
						password: user.password, 
						nick: user.nick, name: 
						user.name
					}
				});
			},

			confirmEmail : function(token){  
				return $http({     
					method: 'POST',      
					url:  base_url + 'confirm_email/',
					headers: {'Content-Type': 'application/json'},
					data: {
						token: token
					}
				});
			},

			recoverPassword : function(email){
				return $http({ 
					method: 'POST', 
					url:  base_url + 'auth/recover_password/',
					headers: {'Content-Type': 'application/json'},
					data: {
						email: email
					}
				});	
			}
		},

		userMe : {
			get : function(){
				return $http({ 
					method: 'GET', 
					url:  base_url + 'user/'
				});
			},

			update : function(user){
				var userData = {
					email: user.email, 
					name: user.name, 
					nick: user.nick, 
					password: user.password
				};

				if(user.password){
					userData.password = user.password;
				}
				return $http({ 
					method: 'POST', 
					url:  base_url + 'user/',
					headers: {'Content-Type': 'application/json'},
					data: userData
				});
			},

			updateSubjects : function (subjects) {
				return $http({ 
					method: 'post', 
					url:  base_url + 'user/subjects/',
					headers: {'Content-Type': 'application/json'},
					data : {
						ids: subjects || [] 
					}
				});
			},

			updateAvatar : function( avatar ){
				console.log( avatar );
				return $http({
					method: 'POST',
					url: base_url + 'user/avatar/',
					headers: {
						'Content-Type': 'multipart/form-data'
					},
					data: {
						avatar: avatar
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
				url: base_url + 'level/' + level +"/notes" + "?recursive="+recursive
			});
		},

		notePut : function(note){
			return $http({
				method: 'PUT', 
				url:  base_url + 'note/' + note.id +'/',
				headers: {'Content-Type': 'application/json'},
				data : {text: note.text, topic: note.topic, level_id: note.level.id}
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

		noteDelete : function(noteId){
			return $http.delete(base_url + 'note/' + noteId +'/');
		},

		subjectFiles : function(subjectId){
			return $http({
				method: 'GET',
				url: base_url + 'subject/' + subjectId +"/files"
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
				url: base_url + 'file/',
				headers: {
					'Content-Type': 'multipart/form-data'
				},
				data: {
					subject_id: data.subjectId,
					uploader_id : data.userId,
					name : data.fileInfo.name,
					text : data.fileInfo.text,
					fileType_id : data.fileType.id,
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
				method: 'PUT', 
				url:  base_url + 'file/' + file.hash,
				headers: {'Content-Type': 'application/json'},
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

		fileGet : function(hash){
			return $http.get(
				base_url + 'file/' + hash,
				{
					headers: {'Accept': 'application/json'}
				}
			);
		},

		fileDownload : function(hash){
			var url = base_url + 'file/' + hash;
			$window.open( url );
		},

		fileDelete : function(hash){
			return $http.delete(base_url + 'file/' + hash);
		},
	};
});  