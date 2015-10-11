angular.module("campusfeed").controller("addPostController", function($scope,$location, SharedState,appfactory,$routeParams){
$scope.errorBox=false;
$scope.username = appfactory.first_name+" "+appfactory.last_name;
$scope.channelname = appfactory.active_channel.channel_name;
$scope.channel_id = $routeParams.channelId;
$scope.picture='';
$scope.creating="post";
$scope.statusText = "Add Post";
$scope.is_admin = appfactory.active_channel.is_admin;
$scope.isAnonymous = false;
if($scope.is_admin==1){
    $scope.post_by = 'channel';
}
else{
    $location.path('/');
}
SharedState.initialize($scope, "resultpost", false);
$scope.navigate = function(){
    $location.path('/');
};

$scope.submit = function(){
    $scope.statusText = "Loading...";
	var formData = new FormData($("#addPostForm")[0]);
    var isAnonymous;
	formData.append("text", $scope.text);
	formData.append("post_by", $scope.post_by);
    var files = $('#files')[0].files; 
    var arr;
    var fileTypes = ['jpg', 'jpeg', 'png', 'gif', 'bmp'];
    for (var i = 0, f; f = files[i]; i++) {

        var reader = new FileReader();
        reader.file = f;
        
            
        reader.onload = function (e) {
            file = this.file;
            fname = file.name;
            console.log(fname);
            var extens = fname.split('.').pop().toLowerCase();
            isSuccess = fileTypes.indexOf(extens) > -1;
            if(isSuccess){
                
                image = new Image();
                image.src = e.target.result;
                var quality =  80;
                output_format = 'jpg'; 
                arr = jic.compress(image,quality,output_format).src;
               formData.append("file", dataURItoBlob(arr), fname);
            }
            else{
                formData.append("file", dataURItoBlob(e.target.result), fname); 
            }    
        };
       
        
        reader.readAsDataURL(f);

    }
    /*if($scope.picture!=""){
        console.log($scope.picture);
        image = new Image();
        image.src = $scope.picture;
        var quality =  60;
        output_format = 'jpg'; 
        $scope.picture = jic.compress(image,quality,output_format).src;
        formData.append("post_img", dataURItoBlob($scope.picture));
    }*/
    if($scope.isAnonymous==true){
    	formData.append("isAnonymous", 'True');
        isAnonymous = 'True';
    }
    else{
    	formData.append("isAnonymous", 'False');
        isAnonymous = 'False';
    }
    appfactory.addPost(formData,$scope.channel_id,$scope.text,$scope.post_by, isAnonymous,$scope.picture).then(function(data){
        $scope.title="Post added!";
        $scope.content="You own the floor. Your post is live and can be seen under "+$scope.channelname+" in Channels I own panel.";
        
        $('#post_modal').modal({
              keyboard: true
            });
        $scope.statusText = "Add Post";
    },function(status){
        $scope.title="Oh snap!";
        $scope.content="Either the channel under which you are posting or you are malicious. Daya will have to break the door to find out.";
        SharedState.setOne('resultpost',true);
        $('#post_modal').modal({
              keyboard: true
            });
        $scope.statusText = "Add Post";
    },function(update){
        $scope.statusText = update.text;
        $scope.progress = update.progress;
    });
};
function dataURItoBlob(dataURI) {
    // convert base64/URLEncoded data component to raw binary data held in a string
    var byteString;
    if (dataURI.split(',')[0].indexOf('base64') >= 0)
        byteString = atob(dataURI.split(',')[1]);
    else
        byteString = unescape(dataURI.split(',')[1]);

    // separate out the mime component
    var mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0];

    // write the bytes of the string to a typed array
    var ia = new Uint8Array(byteString.length);
    for (var i = 0; i < byteString.length; i++) {
        ia[i] = byteString.charCodeAt(i);
    }

    return new Blob([ia], {type:mimeString});
}

});