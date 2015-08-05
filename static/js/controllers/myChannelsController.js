angular.module("campusfeed").controller("myChannelsController", function($scope,$location,$http,appfactory,$routeParams){
$scope.title = "Channels you own";
$scope.errorBox=false;
$scope.limit=10;
$scope.offset=0;
$scope.channels=[];
$scope.moreAval=1;
$scope.following=1;
$scope.anyAval=1;
$scope.pending_request = 1;
$scope.statusText = 'Load more';
$scope.type = 'mine';
if(appfactory.loggedIn==false){
	$location.path('/login');
}
else{
	appfactory.myChannels($scope.limit,$scope.offset).then(function(data){
		if(data.my_channels.length>0){
			$scope.channels=data.my_channels;
		}
		else{
			$scope.anyAval=0;
		}
		$scope.pending_request = 0;
	},function(status){
		$scope.errorBox=true;
		$scope.pending_request = 0;
	},function(update){
	});
}

$scope.goToChannel=function(channel){
	appfactory.active_channel=channel;
	$location.path('/channels/'+$scope.type+'/'+channel.channel_id);
};

$scope.loadMore = function(){
	$scope.offset = $scope.limit;
	$scope.limit += 10;
	$scope.statusText = 'Loading...';
	appfactory.myChannels($scope.limit,$scope.offset).then(function(data){
		if(data.my_channels.length>0){
			$scope.channels = $scope.channels.concat(data.my_channels);
		}
		else{
			$scope.moreAval=0;
		}
		$scope.statusText = 'Load more';		
	},function(status){
		$scope.moreAval=0;
		$scope.errorBox=true;
		$scope.statusText = 'Load more';
	},function(update){
		$scope.statusText = update;
	});
};

});