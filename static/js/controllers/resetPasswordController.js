angular.module("campusfeed").controller("resetPasswordController", function($scope,$location,$modal,$http,appfactory,$routeParams){
$scope.show=0;
$scope.errorBox = false;
$scope.errorBox2 = false;
$scope.statusText = "Set it!";
$scope.success=0;
$scope.forgotId = $routeParams.forgotId;
$scope.pending_request = 1;
appfactory.checkForgotId($scope.forgotId).then(function(data){
	$scope.show=1;
	$scope.pending_request = 0;
},function(status){
	$scope.errorBox = 1;
	$scope.pending_request = 0;
});
$scope.reset = function(password,confirmpassword){
	$scope.statusText = "Loading...";
	if(password == confirmpassword){
		appfactory.resetPassword($scope.forgotId,password).then(function(data){
			$scope.success=1;
			$scope.statusText = "Set it!";
		},function(status){
			$scope.errorBox2 = true;
			$scope.statusText = "Set it!";
		});
	}
	else{
		$scope.errorBox2 = true;
	}
};
});