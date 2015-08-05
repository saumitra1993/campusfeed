angular.module("campusfeed").controller("loginController", function($scope,$location,$http,appfactory,$routeParams){
$scope.statusText = "Login";
$scope.login = function(){
	$scope.errorBox=false;
	$scope.statusText = "Loading...";
	appfactory.login($scope.studentid, $scope.password).then(function(data){
			$location.path('/');
			$scope.statusText = "Login";
		},function(status){
			$scope.errorBox=true;
			$scope.statusText = "Login";
		},function(update){
			$scope.statusText = update;
		});
	
};

});