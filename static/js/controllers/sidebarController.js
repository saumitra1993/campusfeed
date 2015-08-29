angular.module("campusfeed").controller("navController", function($scope,$location,$http,appfactory,$routeParams,SharedState){
$scope.isSuperuser=appfactory.isSuperuser;
$scope.loggedIn = false;
if(appfactory.loggedIn == false){
	$scope.personalisedText = "You are not logged in.";
}
else{
	$scope.personalisedText = appfactory.first_name+"'s Campusfeed";
	$scope.loggedIn = true;
}
$scope.$on('login', function(e, data) {
  if (data.loggedIn === true) {
    $scope.personalisedText = appfactory.first_name+"'s Campusfeed";
    $scope.isSuperuser = appfactory.isSuperuser;
    $scope.loggedIn = true;
  } 
  else {
    $scope.personalisedText = "You are not logged in.";
    $scope.loggedIn = false;
  }
});

});