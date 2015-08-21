angular.module('campusfeed').controller('ForgotPasswordCtrl', function ($scope, $modalInstance, appfactory) {
$scope.success = false;
$scope.errorBox = false;
$scope.submitText = "Submit";
$scope.sendforlink = function(){
	$scope.submitText = "Loading...";
	appfactory.forgotpassword($scope.email_id).then(function(data){
		$scope.success = true;
		$scope.email_id = "";
		$scope.submitText = "Submit";
	},function(status){
		$scope.errorBox = true;
		$scope.submitText = "Submit";
	},function(update){
		$scope.submitText = "Loading...";
	});
};
  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };

});