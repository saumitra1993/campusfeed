angular.module("campusfeed").controller("logoutController", function($scope,$location,$http,appfactory,$routeParams){

$scope.errorBox=false;

var data = appfactory.logout().then(function(data){
	$location.path('/login');
},function(data){
	$scope.errorBox=true;
});
});