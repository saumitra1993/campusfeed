angular.module("campusfeed").controller("createChannelController", function($scope,$location,SharedState,$http,appfactory,$routeParams){
$scope.errorBox=false;
$scope.picture='';
$scope.creating="channel";
$scope.statusText = "Create Channel";
$scope.picture="";
$scope.tag="course";
if(appfactory.loggedIn==false){
    $location.path('/login');
}
$scope.navigate = function(){
    $location.path('/');
};
$scope.submit = function(){
     var isAnonymous;
     $scope.statusText = "Loading...";
    var formData = new FormData();
    var name_arr = $scope.name.split(" ");
    for(var i=0;i<name_arr.length;i++){
        if(name_arr[i].toUpperCase() != name_arr[i]){
            name_arr[i] = toTitleCase(name_arr[i]);
        }
    }
    $scope.name = name_arr.join(' ');
    formData.append("channel_name", $scope.name);
    formData.append("description", $scope.descr);
    formData.append("tag", $scope.tag);
    if($scope.picture!=""){
        formData.append("channel_img", dataURItoBlob($scope.picture));
    }
    if($scope.isAnonymous==true){
        formData.append("isAnonymous", 'True');
        isAnonymous = 'True';
    }
    else{
        formData.append("isAnonymous", 'False');
        isAnonymous = 'False';
    }
    appfactory.createchannel(formData,$scope.name, $scope.descr, isAnonymous, $scope.picture).then(function(data){
        
            $scope.title="Welcome Feed Admin!";
            $scope.content="Your channel is currently under review. You can see your channel in 'Channels I own' panel. You will be able to post in your channel shortly.";
            $scope.statusText = "Create Channel";
            $('#channel_modal').modal({
              keyboard: true
            });
        },function(status){
            $scope.title="Oh shoot!";
            $scope.content="Something's wrong. Can't hurt to try again.";
            $scope.statusText = "Create Channel";
            $('#channel_modal').modal({
              keyboard: true
            });
        },function(update){
            $scope.statusText = update.text;
            $scope.progress = update.progress;
        });
};

function toTitleCase(str)
{
    return str.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
}
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