angular.module("campusfeed").controller("allChannelsController", function($scope,$location,$http,appfactory,$routeParams){
$scope.title = "Discover channels";
$scope.errorBox=false;
$scope.limit=10;
$scope.offset=0;
$scope.channels=[];
$scope.moreAval=1;
$scope.anyAval=1;
$scope.statusText = "Load more";
$scope.tags = ["course","club", "committee", "event"];
$scope.pending_request = 1;
$scope.type = 'unrelated';
if(appfactory.loggedIn==false){
	$location.path('/login');
}
else{
	appfactory.allChannels($scope.limit,$scope.offset).then(function(data){
		
		$scope.channels=data.all_channels;
		$scope.pending_request = 0;
	},function(status){
		$scope.errorBox=true;
		$scope.pending_request = 0;
	},function(update){
		$scope.statusText = update;
	});
}

$scope.goToChannel=function(channel){
	appfactory.active_channel=channel;
	$location.path('/channels/'+$scope.type+'/'+channel.channel_id);
};

$scope.loadMore = function(){
	$scope.offset = $scope.limit;
	$scope.limit += 10;
	appfactory.allChannels($scope.limit,$scope.offset).then(function(data){
		if(data.all_channels.length>0){
			$scope.channels = $scope.channels.concat(data.all_channels);
		}
		else{
			$scope.moreAval=0;
		}
		$scope.statusText = "Load More";		
	},function(status){
		$scope.moreAval=0;
		$scope.errorBox=true;
		$scope.statusText = "Load More";
	},function(update){
		$scope.statusText = update;
	});
};
$scope.filterTag = function(tag) {
	for (var key in $scope.channels) {
	   if ($scope.channels.hasOwnProperty(key)) {
	        if(key == tag){
	        	return $scope.channels[key];
	        	break;
	        }
	    }
	}
};
});