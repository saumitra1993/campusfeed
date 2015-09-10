angular.module('campusfeed').controller('EditChannelCtrl', function ($scope, $location, $modalInstance, appfactory, channel_id) {
$scope.channel_id = channel_id;
$scope.errorBox = false;
$scope.statusText = "Submit";
$scope.img = "";
$scope.okText = "Ok";
$scope.cancelmodal = function () {
    $modalInstance.dismiss('cancel');
};


appfactory.channelDetails($scope.channel_id).then(function(data){
	$scope.descr = data.description;
	$scope.img_url = data.channel_img_url;
	$scope.name = data.channel_name;
	
},function(status){
	$scope.errorBox=true;
});

$scope.$on("cropme:done", function(ev, result, canvasEl) { 
	console.log("Cropping done!");
	$scope.img = result.croppedImage;
});

$scope.ok = function(){
	$scope.okText = "Image Selected";
	 $scope.$broadcast("cropme:ok");
};
$scope.cancel = function(){
	$scope.okText = "Ok";
	$scope.$broadcast("cropme:cancel");
};

$scope.submit = function(){
	$scope.statusText = "Loading...";
    var formData = new FormData();
    formData.append("channel_id", channel_id);
    formData.append("channel_name", $scope.name);
    formData.append("description", $scope.descr);
    formData.append('channel_img',$scope.img);
    appfactory.editchannel(formData).then(function(status){
    	$scope.statusText = "Submit";
    	$modalInstance.dismiss('cancel');
    	$location.path('/');
    },function(status){
    	$scope.statusText = "Submit";
    	$scope.errorBox = true;
    });
};

});