angular.module("campusfeed").controller("signupController", function($scope,$location,$http,appfactory,$routeParams,SharedState){
$scope.errorBox=false;
$scope.picture='';
SharedState.initialize($scope, "resultuser", false);
$scope.creating="user";
$scope.statusText = "Sign Up";
$scope.picture="";
$scope.navigate = function(){
    $location.path('/login');
};
$scope.submit = function(){
     $scope.statusText = "Loading...";
    var formData = new FormData();
    
    $scope.first_name = toTitleCase($scope.first_name);
    $scope.last_name = toTitleCase($scope.last_name);
    $scope.branch = $scope.branch.toUpperCase();
    formData.append("first_name", $scope.first_name);
    formData.append("last_name", $scope.last_name);
    formData.append("branch", $scope.branch);
    formData.append("email_id", $scope.email);
    formData.append("user_id", $scope.user_id);
    formData.append("phone", $scope.phone);
    formData.append("password", $scope.password);
    if($scope.picture!=""){
        formData.append("user_img", dataURItoBlob($scope.picture));
    }
    appfactory.createuser(formData,$scope.first_name,$scope.last_name,$scope.branch,$scope.email,$scope.user_id,$scope.phone,$scope.password,$scope.picture).then(function(data){
        
            $scope.title="Welcome!";
            $scope.content="Hi "+$scope.first_name+"! Login to start with Campusfeed.";
            SharedState.setOne('resultuser',true);
            $scope.statusText = "Sign Up";
        },function(status){
            $scope.title="Oh shoot!";
            $scope.content="Something's wrong. Can't hurt to try again.";
            SharedState.setOne('resultuser',true);    
            $scope.statusText = "Sign Up";
        },function(update){
            $scope.statusText = update.text;
            $scope.progress = update.progress;
        });
};
$scope.seed = 0;
$scope.generateUniqueName = function()
{
    $scope.seed++;
    return $scope.seed;
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