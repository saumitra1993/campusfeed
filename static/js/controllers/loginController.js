angular.module("campusfeed").controller("loginController", function($scope,$location,$uibModal, SharedState, $http,appfactory,$routeParams){
$scope.statusText = "Login";
$scope.errorBox2=false;
$scope.picture='';
$scope.creating="user";
$scope.statusText2 = "Sign Up";
$scope.signup_success = true;
var searchObject = $location.search();
$scope.branch = "Choose your department";
console.log(searchObject);
$scope.redirect_to = searchObject.redirect_to;
console.log($scope.redirect_to);
$scope.message = "There was some error. Please try again.";
$scope.login = function(){
	$scope.errorBox=false;
	$scope.statusText = "Loading...";
	appfactory.login($scope.studentid, $scope.pass).then(function(data){
            if($scope.redirect_to == undefined){
    			$location.path('/');	
            }
            else{
                $location.url('/'+$scope.redirect_to);
            }
            $scope.statusText = "Login";
		},function(data){
			$scope.errorBox=true;
            if(data.message!=""){
                $scope.message = data.message;
            }
			$scope.statusText = "Login";
		},function(update){
			$scope.statusText = update;
		});
	
};

$scope.close = function(){
    if($scope.signup_success == true){
        $scope.first_name="";
        $scope.last_name="";
        $scope.studentid=$scope.email;
        $scope.branch = "Choose your department";
        $scope.phone="";
        $scope.user_id="";
        $scope.email="";
        $scope.password="";
        $scope.picture="";
    }
    $('#user_modal').modal('toggle');
};

$scope.submit = function(){
     $scope.statusText2 = "Loading...";
     if($scope.branch != "Choose your department"){
        var formData = new FormData();
    
        $scope.first_name = toTitleCase($scope.first_name);
        $scope.last_name = toTitleCase($scope.last_name);
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
                $('#user_modal').modal({
                  keyboard: true
                });
                $scope.statusText2= "Sign Up";
            },function(data){
                $scope.signup_success = false;
                $scope.title="Oh shoot!";
                $scope.content="Something's wrong. Can't hurt to try again.";
                $('#user_modal').modal({
                  keyboard: true
                });
                $scope.statusText2 = "Sign Up";
                if(data.message!=""){
                    $scope.message = data.message;
                }
                
            },function(update){
                $scope.statusText2 = update.text;
                $scope.progress = update.progress;
            });
    }
    else{
        $scope.signup_success = false;
        $scope.title="Oh shoot!";
        $scope.content="Fill out your branch.";
        $('#user_modal').modal({
          keyboard: true
        });
        $scope.statusText2 = "Sign Up";
        
    }
    
};
$scope.open = function () {
    var modalInstance = $uibModal.open({
      animation: $scope.animationsEnabled,
      controller: 'ForgotPasswordCtrl',
      templateUrl: 'forgotpassword.html',
      resolve: {
        selectedImgUrl: function () {
          return $scope.imgUrl;
        }
      }
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