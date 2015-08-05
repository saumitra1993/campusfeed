angular.module("campusfeed").controller("logoutController", function($scope,$location,$http,appfactory,$routeParams){

$scope.errorBox=false;

var data = appfactory.logout();
		
$location.path('/login');

});