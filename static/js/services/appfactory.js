angular.module("campusfeed").factory('appfactory',function($q,$rootScope,SharedState){

var factory={};
var url = window.location.href;
console.log(url);
var n = url.search("www.");
if(n==-1){
  var ip='http://campusfeedapp-1097.appspot.com/';  
}
else{
    var ip='http://www.campusfeedapp-1097.appspot.com/';
}
var user_id= window.localStorage.getItem("user_id");
SharedState.initialize($rootScope, "loggedIn", false);
if(user_id){
    factory.user_id = user_id;
    factory.first_name = window.localStorage.getItem("first_name");
    factory.last_name = window.localStorage.getItem("last_name");
    factory.token = window.localStorage.getItem("token");
    factory.isSuperuser=window.localStorage.getItem("isSuperuser");
    
    factory.loggedIn = true;
    SharedState.setOne('loggedIn',true);
    /*cordovaHTTP.setHeader("token", factory.token).then(function() {
        console.log('success!');
    }, function() {
        console.log('error :(');
    });*/
}
else{
    factory.loggedIn = false;
}


factory.login=function(studentid, password){
	var defer1=$q.defer();
    
    $.ajax({
        type: "POST",
        url: ip+'login',
        data: JSON.stringify({"user_id":studentid,"password":password}),
        contentType: "application/json",
        dataType: "json",
        async:true,
        beforeSend: function(){
            defer1.notify('Loading...');
        },
        success: function(data, textStatus, xhr){
            factory.first_name = data.first_name;
            factory.last_name = data.last_name;
            factory.token = data.mAuthToken;
            factory.loggedIn = true;
            factory.user_id = data.user_id;
            console.log(data.type);
            if(data.type=="superuser"){
                factory.isSuperuser=1;
            }
            else{
                factory.isSuperuser=0;
            }
            $rootScope.$broadcast('login', {loggedIn:factory.loggedIn});
            window.localStorage.setItem("user_id", factory.user_id);
            window.localStorage.setItem("first_name", factory.first_name);
            window.localStorage.setItem("last_name", factory.last_name);
            window.localStorage.setItem("token", factory.token);
            window.localStorage.setItem("isSuperuser", factory.isSuperuser);
            /*cordovaHTTP.setHeader("token", factory.token).then(function() {
                console.log('success!');
            }, function() {
                console.log('error :(');
            });*/
            defer1.resolve(xhr.status);
        },
        error: function(data, textStatus, xhr){
            var tempObj = {};
            tempObj.status = xhr.status;
            console.log(data.statusText);
            tempObj.message = data.statusText;
            defer1.reject(tempObj);
        },
        timeout: 15000 
    });
    return defer1.promise;
};

factory.myChannels = function(limit,offset){
    var defer2=$q.defer();
    /*cordovaHTTP.get(ip+'users/'+factory.user_id+"/mychannels?limit="+limit+"&offset="+offset, {},{"Content-Type":"application/json"}).then(function(response){
        console.log(response.status);
        console.log(response.data);
        defer2.resolve(JSON.parse(response.data));
    }, function(response) {
        defer2.reject(response.status);
        console.error(response.error);
    });*/
    $.ajax({
            type: "GET",
            async:true,
            url: ip+'users/'+factory.user_id+"/mychannels?limit="+limit+"&offset="+offset,
            dataType: "json",
            beforeSend: function(){
                defer2.notify('Loading...');
            },
            success: function(data, textStatus, xhr){
                defer2.resolve(data);
                
            },
            error: function(data, textStatus, xhr){
                console.log(textStatus);
                defer2.reject(xhr.status);
                
            },
            timeout: 15000
        });  
    return defer2.promise;
};

factory.followedChannels = function(limit,offset){
    var defer3=$q.defer();
    /*cordovaHTTP.get(ip+'users/'+factory.user_id+"/channels?limit="+limit+"&offset="+offset, {},{"Content-Type":"application/json"}).then(function(response){
        console.log(response.status);
        console.log(response.data);
        defer3.resolve(JSON.parse(response.data));
    }, function(response) {
        defer3.reject(response.status);
        console.error(response.error);
    });*/
    $.ajax({
        type: "GET",
        url: ip+'users/'+factory.user_id+"/channels?limit="+limit+"&offset="+offset+"&tag=all",
        async:true,
        dataType: "json",
        beforeSend: function(){
            defer3.notify('Loading...');
        },
        success: function(data, textStatus, xhr){
            defer3.resolve(data);    
        },
        error: function(data, textStatus, xhr){
            defer3.reject(xhr.status);    
        },
        timeout: 15000
    }); 
    
    return defer3.promise;
};

factory.channelDetails = function(channel_id){
    var defer4=$q.defer();
    /*cordovaHTTP.get(ip+'channels/'+channel_id, {},{"Content-Type":"application/json"}).then(function(response){
        console.log(response.status);
        console.log(response.data);
        defer4.resolve(JSON.parse(response.data));
    }, function(response) {
        defer4.reject(response.status);
        console.error(response.error);
    });*/
    $.ajax({
        type: "GET",
        url: ip+'channels/'+channel_id,
        async:true,
        dataType: "json",
        beforeSend: function(){
            defer4.notify('Loading...');
        },
        success: function(data, textStatus, xhr){
            defer4.resolve(data);
            
        },
        error: function(data, textStatus, xhr){
            defer4.reject(xhr.status);
            
        },
        timeout: 15000
    }); 
    
    return defer4.promise;
};

factory.channelPosts=function(channel_id,limit,offset){
    var defer5=$q.defer();
    /*cordovaHTTP.get(ip+'channels/'+channel_id+"/posts?limit="+limit+"&offset="+offset, {},{"Content-Type":"application/json"}).then(function(response){
        console.log(response.status);
        console.log(response.data);
        defer5.resolve(JSON.parse(response.data));
    }, function(response) {
        defer5.reject(response.status);
        console.error(response.error);
    });*/
    $.ajax({
        type: "GET",
        url: ip+'channels/'+channel_id+"/posts?limit="+limit+"&offset="+offset,
        async:true,
        dataType: "json",
        beforeSend: function(){
            defer5.notify('Loading...');
        },
        success: function(data, textStatus, xhr){
            defer5.resolve(data);
            
        },
        error: function(data, textStatus, xhr){
            defer5.reject(xhr.status);
            
        },
        timeout: 15000
    });    
    return defer5.promise;
};

factory.createchannel = function(formData,name,descr,isAnonymous,image){
  var defer6=$q.defer();
  formData.append("user_id",factory.user_id);
  var update = {};
  update.text = "Loading...";
  update.progress=0;
  defer6.notify(update);
    /*if(image!=''){
        var options = new FileUploadOptions();
        options.fileKey="channel_img";
        options.fileName=image.substr(image.lastIndexOf('/')+1);
        options.mimeType="image/jpeg";

        var params = {};
        params.channel_name = name;
        params.description = descr;
        params.isAnonymous = isAnonymous;
        params.user_id = factory.user_id;
        options.params = params;
        var ft = new FileTransfer();
        ft.onprogress = function(progressEvent) {
            if (progressEvent.lengthComputable) {
                var perc = (progressEvent.loaded / progressEvent.total)*100;
                update.progress = perc;
                defer6.notify(update);
            } 
        };
        ft.upload(image, encodeURI(ip+"channels"), function(r){
            defer6.resolve(r.responseCode);
            
        }, function(r){
            defer6.reject(r.responseCode);
            
        }, options);
    }
    else{*/
      $.ajax({
        url: ip+"channels",
        data: formData,
        async:true,
        processData: false,
        contentType: false,
        type: 'POST',
        beforeSend: function(){
            defer6.notify('Loading...');
        },
        success: function(data, textStatus, xhr){
            defer6.resolve(xhr.status);     
        },
        error: function(data, textStatus, xhr){
            defer6.reject(xhr.status);
        },
        timeout: 15000
      });
    
  
   return defer6.promise;
};



factory.addPost = function(formData,channel_id,text,post_by,isAnonymous,image){
    var defer7=$q.defer();
    formData.append("user_id",factory.user_id);
    var update = {};
    update.text = "Loading...";
    update.progress=0;
    
    /*if(image!=''){
        var options = new FileUploadOptions();
        options.fileKey="post_img";
        options.fileName=image.substr(image.lastIndexOf('/')+1);
        options.mimeType="image/jpeg";

        var params = {};
        params.text = text;
        params.post_by = post_by;
        params.isAnonymous = isAnonymous;
        params.user_id = factory.user_id;
        options.params = params;
        var ft = new FileTransfer();
        ft.onprogress = function(progressEvent){
            if (progressEvent.lengthComputable) {
                var perc = (progressEvent.loaded / progressEvent.total)*100;
                update.progress = perc;
                defer7.notify(update);
            } 
        };
        ft.upload(image, encodeURI( ip+"channels/"+channel_id+"/posts"), function(r){
            defer7.resolve(r.responseCode);
           
        }, function(r){
            defer7.reject(r.responseCode);
            
        }, options);
    }
    else{*/
    $.ajax({
        type: "GET",
        url: ip+'uploadendpoint?channel_id='+channel_id,
        dataType:"json",
        success: function(data, textStatus, xhr){
            $.ajax({
                url: data.upload_url,
                data: formData,
                async:true,
                processData: false,
                contentType: false,
                type: 'POST',
                
                success: function(data, textStatus, xhr){
                    defer7.resolve(data);
                    
                },
                error: function(data, textStatus, xhr){
                    defer7.reject(data);
                    
                },
                timeout: 25000
              });
        },
        error: function(data, textStatus, xhr){
            defer7.reject(xhr.status);
            
        },
        timeout: 15000
    }); 
 
   return defer7.promise;
   
};

factory.approvePost = function(channel_id, post_id){
  var defer8=$q.defer();
  
  $.ajax({
        type: "PUT",
        async:true,
        url:  ip+"channels/"+channel_id+"/posts/"+post_id,
        data: {},
        beforeSend: function(){
            defer8.notify('Loading...');
        },
        success: function(data, textStatus, xhr){
           defer8.resolve(xhr.status);
           
        },
        error: function(data, textStatus, xhr){
            defer8.reject(xhr.status);
            
        },
        timeout: 15000
      });
  
  
   return defer8.promise;
};

factory.followChannel=function(channel_id, getNotifications){
    var defer9=$q.defer();
    if(getNotifications == true){
        getNotifications = 1;
    }else{
        getNotifications = 0;
    }
    $.ajax({
        type: "POST",
        async:true,
        url: ip+'users/'+factory.user_id+"/channels",
        data: JSON.stringify({"channel_id":channel_id,'get_notification':getNotifications}),
        contentType: "application/json; charset=utf-8",
        beforeSend: function(){
            defer9.notify('Loading...');
        },
        success: function(data, textStatus, xhr){
            defer9.resolve(xhr.status);
            
        },
        error: function(data, textStatus, xhr){
            defer9.reject(xhr.status);
           
        },
        timeout: 15000
    });
    return defer9.promise;
};

factory.allChannels = function(limit,offset){
    var defer10=$q.defer();
    /*cordovaHTTP.get(ip+"channels?limit="+limit+"&offset="+offset, {},{"Content-Type":"application/json"}).then(function(response){
        console.log(response.status);
        console.log(response.data);
        defer10.resolve(JSON.parse(response.data));
    }, function(response) {
        defer10.reject(response.status);
        console.error(response.error);
    });*/
    $.ajax({
        type: "GET",
        async:true,
        url:ip+"channels?limit="+limit+"&offset="+offset+"&tag=all",
        
        dataType: "json",
        beforeSend: function(){
            defer10.notify('Loading...');
        },
        success: function(data, textStatus, xhr){
            defer10.resolve(data);
            
        },
        error: function(data, textStatus, xhr){
            defer10.reject(xhr.status);
            
        },
        timeout: 15000
    });  
    return defer10.promise;
    
};

factory.searchUser= function(search_string){
  var defer11=$q.defer();
  /*cordovaHTTP.get(ip+"users/search"+search_string, {},{"Content-Type":"application/json"}).then(function(response){
        console.log(response.status);
        console.log(response.data);
        defer11.resolve(JSON.parse(response.data));
    }, function(response) {
        defer11.reject(response.status);
        console.error(response.error);
    });*/
    $.ajax({
        type: "GET",
        async:true,
        url:ip+"users/search"+search_string,
        
        dataType: "json",
        beforeSend: function(){
            defer11.notify('Loading...');
        },
        success: function(data, textStatus, xhr){
            defer11.resolve(data);
            
        },
        error: function(data, textStatus, xhr){
            defer11.reject(xhr.status);
            
        },
        timeout: 15000
    });  
    return defer11.promise;
};

factory.addAdmin=function(user,channel_id){
  var defer12=$q.defer();
  console.log(user.user_id+" "+user.isAnonymous);
  $.ajax({
        type: "POST",
        async:true,
        url: ip+"channels/"+channel_id+"/admins",
        data: JSON.stringify({"user_id":user.user_id,"isAnonymous":user.isAnonymous}),
        contentType: "application/json; charset=utf-8",
        beforeSend: function(){
            defer12.notify('Loading...');
        },
        success: function(data, textStatus, xhr){
            console.log("idhar");
            defer12.resolve(xhr.status);
            
        },
        error: function(data, textStatus, xhr){
            console.log(textStatus);
            defer12.reject(xhr.status);
            
        },
        timeout: 15000
    });
  
  return defer12.promise;
};
factory.feed = function(limit,offset){

    var defer13=$q.defer();
    /*cordovaHTTP.get(ip+"users/"+factory.user_id+"/feed?limit="+limit+"&offset="+offset, {},{"Content-Type":"application/json"}).then(function(response){
        console.log(response.status);
        defer13.resolve(JSON.parse(response.data));
    }, function(response){
        defer13.reject(response.status);
        console.error(response.error);
    });*/
    var defer13=$q.defer();
     $.ajax({
        type: "GET",
        async:true,
        url:ip+"users/"+factory.user_id+"/feed?limit="+limit+"&offset="+offset,
        
        dataType: "json",
        beforeSend: function(){
            defer13.notify('Loading...');
        },
        success: function(data, textStatus, xhr){
            defer13.resolve(data);
        },
        error: function(data, textStatus, xhr){
            defer13.reject(xhr.status);
        },
        timeout: 15000
    });
    return defer13.promise;
};

factory.createuser = function(formData,first_name, last_name, branch,email_id,user_id,phone,password,image){
  var defer14=$q.defer();
  var update = {};
  update.text = "Loading...";
  update.progress=0;
  defer14.notify(update);
  
  $.ajax({
    url: ip+"signup",
    data: formData,
    async:true,
    processData: false,
    contentType: false,
    type: 'POST',
    beforeSend: function(){
        defer14.notify('Loading...');
    },
    success: function(data, textStatus, xhr){
        var tempObj = {};
        tempObj.status = xhr.status;
        
        tempObj.message = xhr.statusText;
        defer14.resolve(tempObj);     
    },
    error: function(data, textStatus, xhr){
        var tempObj = {};
        tempObj.status = xhr.status;
        tempObj.message = data.statusText;
        defer14.reject(tempObj);
    },
    timeout: 15000
  });
      
   return defer14.promise;
};

factory.logout = function(){
    var defer15=$q.defer();
    $.ajax({
        url: ip+"logout",
        async:true,
        processData: false,
        contentType: false,
        type: 'GET',
        success: function(data, textStatus, xhr){
            window.localStorage.clear();
            factory.loggedIn=false;
            factory.user_id = -1;
            factory.first_name = "";
            factory.last_name = "";
            factory.token="";
            factory.isSuperuser=0;
            $rootScope.$broadcast('login', {loggedIn:factory.loggedIn});
            defer15.resolve(xhr.status);     
        },
        error: function(data, textStatus, xhr){
            defer15.reject(xhr.status);
        },
        timeout: 15000
    });
    return defer15.promise;
};

factory.forgotpassword = function(email_id){
    var defer16=$q.defer();
     $.ajax({
        type: "POST",
        url: ip+'forgotpassword',
        data: JSON.stringify({"email_id":email_id}),
        contentType: "application/json",
        dataType: "json",
        async:true,
        beforeSend: function(){
            defer16.notify('Loading...');
        },
        success: function(data, textStatus, xhr){
            defer16.resolve(data);
        },
        error: function(data, textStatus, xhr){
            defer16.reject(xhr.status);
        },
        timeout: 15000
    });
     return defer16.promise;
};

factory.checkForgotId = function(forgotId){
    var defer17=$q.defer();
     $.ajax({
        type: "GET",
        url: ip+'resetpassword?forgotId='+forgotId,
        contentType: "application/json",
        dataType: "json",
        async:true,
        success: function(data, textStatus, xhr){
            defer17.resolve(textStatus);
        },
        error: function(data, textStatus, xhr){
            defer17.reject(textStatus);
        },
        timeout: 15000
    });
     return defer17.promise;
};
factory.resetPassword = function(forgotId,password){
    var defer18=$q.defer();
     $.ajax({
        type: "POST",
        url: ip+'resetpassword',
        data: JSON.stringify({"forgotId":forgotId,"password":password}),
        contentType: "application/json",
        dataType: "json",
        async:true,
        
        success: function(data, textStatus, xhr){
            defer18.resolve(textStatus);
        },
        error: function(data, textStatus, xhr){
            defer18.reject(xhr.status);
        },
        timeout: 15000
    });
     return defer18.promise;
};

factory.unfollowChannel=function(channel_id){
    var defer19=$q.defer();
    
    $.ajax({
        type: "POST",
        async:true,
        url: ip+'users/'+factory.user_id+"/unfollowchannel",
        data: JSON.stringify({"channel_id":channel_id}),
        contentType: "application/json; charset=utf-8",
        
        success: function(data, textStatus, xhr){
            defer19.resolve(xhr.status);
            
        },
        error: function(data, textStatus, xhr){
            defer19.reject(xhr.status);
           
        },
        timeout: 15000
    });
    return defer19.promise;
};

factory.editchannel = function(formData){
    var defer20=$q.defer();
  
  
  $.ajax({
    url: ip+"editchannel",
    data: formData,
    async:true,
    processData: false,
    contentType: false,
    type: 'POST',
    
    success: function(data, textStatus, xhr){
        defer20.resolve(xhr.status);     
    },
    error: function(data, textStatus, xhr){
        defer20.reject(xhr.status);
    },
    timeout: 15000
  });
      
   return defer20.promise;
};

factory.getFollowers = function(channelId){
    var defer21=$q.defer();
     $.ajax({
        type: "GET",
        url: ip+'channels/'+channelId+"/followers",
        contentType: "application/json",
        dataType: "json",
        async:true,
        success: function(data, textStatus, xhr){
            defer21.resolve(data);
        },
        error: function(data, textStatus, xhr){
            defer21.reject(textStatus);
        },
        timeout: 15000
    });
     return defer21.promise;
};

factory.getChannelId = function(){
    var defer22=$q.defer();
     $.ajax({
        type: "GET",
        url: ip+'channelid?user_id='+factory.user_id,
        contentType: "application/json",
        dataType: "json",
        async:true,
        success: function(data, textStatus, xhr){
            defer22.resolve(data);
        },
        error: function(data, textStatus, xhr){
            defer22.reject(textStatus);
        },
        timeout: 15000
    });
     return defer22.promise;
};

factory.getThreads = function(channel_id,limit,offset){
    var defer23=$q.defer();
     $.ajax({
        type: "GET",
        url: ip+'channels/'+channel_id+"/threads?limit="+limit+"&offset="+offset,
        contentType: "application/json",
        dataType: "json",
        async:true,
        success: function(data, textStatus, xhr){
            defer23.resolve(data);
        },
        error: function(data, textStatus, xhr){
            defer23.reject(textStatus);
        },
        timeout: 15000
    });
     return defer23.promise;
};

factory.addThread = function(channel_id,topic){
    console.log(topic);
    var defer24=$q.defer();
    $.ajax({
        url: ip+"channels/"+channel_id+"/threads",
        data: JSON.stringify({"topic":topic}),
        contentType: "application/json",
        dataType: "json",
        type: 'POST',

        success: function(data, textStatus, xhr){
            defer24.resolve(data);     
        },
        error: function(data, textStatus, xhr){
            defer24.reject(xhr.status);
        },
        timeout: 15000
    });
      
   return defer24.promise;
};

factory.getComments = function(channel_id,thread_id,limit,offset){
    var defer25=$q.defer();
     $.ajax({
        type: "GET",
        url: ip+'channels/'+channel_id+"/threads/"+thread_id+"/discussions?limit="+limit+"&offset="+offset,
        contentType: "application/json",
        dataType: "json",
        async:true,
        success: function(data, textStatus, xhr){
            defer25.resolve(data);
        },
        error: function(data, textStatus, xhr){
            defer25.reject(textStatus);
        },
        timeout: 15000
    });
     return defer25.promise;
};

factory.addComment = function(channel_id,thread_id,comment){
    var defer25=$q.defer();
    $.ajax({
        url: ip+"channels/"+channel_id+"/threads/"+thread_id+"/discussions",
        data: JSON.stringify({"text":comment}),
        contentType: "application/json",
        dataType: "json",
        type: 'POST',

        success: function(data, textStatus, xhr){
            defer25.resolve(data);     
        },
        error: function(data, textStatus, xhr){
            defer25.reject(xhr.status);
        },
        timeout: 15000
    });
      
   return defer25.promise;
};

factory.deleteComment = function(channel_id,thread_id,comment_id){
    var defer26=$q.defer();
    $.ajax({
        url: ip+"channels/"+channel_id+"/threads/"+thread_id+"/deletecomment",
        data: JSON.stringify({"comment_id":comment_id}),
        contentType: "application/json",
        dataType: "json",
        type: 'POST',

        success: function(data, textStatus, xhr){
            defer26.resolve(data);     
        },
        error: function(data, textStatus, xhr){
            defer26.reject(xhr.status);
        },
        timeout: 15000
    });
      
   return defer26.promise;
};

factory.deleteThread = function(channel_id,thread_id){
    var defer27=$q.defer();
    $.ajax({
        url: ip+"channels/"+channel_id+"/deletethread",
        data: JSON.stringify({"thread_id":thread_id}),
        contentType: "application/json",
        dataType: "json",
        type: 'POST',

        success: function(data, textStatus, xhr){
            defer27.resolve(data);     
        },
        error: function(data, textStatus, xhr){
            defer27.reject(xhr.status);
        },
        timeout: 15000
    });
      
   return defer27.promise;
};

return factory;
});