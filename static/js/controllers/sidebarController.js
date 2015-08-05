angular.module("campusfeed").controller("sidebarController", function($scope,$location,$http,appfactory,$routeParams,SharedState){
if(appfactory.loggedIn==false){
	$scope.personalisedText = "You are not logged in.";
}
else{
	$scope.personalisedText = appfactory.first_name+"'s Campusfeed";
}
$scope.$on('mobile-angular-ui.state.changed.loggedIn', function(e, newVal, oldVal) {
  if (newVal === true) {
    $scope.personalisedText = appfactory.first_name+"'s Campusfeed";
  } else {
    $scope.personalisedText = "You are not logged in.";
  }
});

});