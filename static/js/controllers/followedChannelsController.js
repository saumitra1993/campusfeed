angular.module("campusfeed").controller("followedChannelsController", function($scope,$location,$http,appfactory,$routeParams){

$scope.errorBox=false;
$scope.limit=10;
$scope.offset=0;
$scope.channels=[];
$scope.moreAval=1;
$scope.statusText = "Load more";
$scope.type = 'related';
$scope.pending_request = 1;
$scope.anyAval=1;

$scope.title = "Channels you follow";

if(appfactory.loggedIn==false){
	$location.path('/login');
}
else{
	appfactory.followedChannels($scope.limit,$scope.offset).then(function(data){
		if(data.followed_channels.length>0){
			$scope.channels = data.followed_channels;
		}
		else{
			$scope.anyAval=0;
		}
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
	if($scope.action == 'addpost'){
		$location.path('/channels/'+channel.channel_id+'/addpost');
	}
	else{
		$location.path('/channels/'+$scope.type+'/'+channel.channel_id);
	}
};

$scope.loadMore = function(){
	$scope.offset = $scope.limit;
	$scope.limit += 10;
	$scope.statusText = "Loading...";
	appfactory.followedChannels($scope.limit,$scope.offset).then(function(data){
		if(data.followed_channels.length>0){
			$scope.channels = $scope.channels.concat(data.followed_channels);
		}
		else{
			$scope.moreAval=0;
		}
		$scope.statusText = "Load more";		
	},function(status){
		$scope.moreAval=0;
		$scope.errorBox=true;
		$scope.statusText = "Load more";
	},function(update){
		$scope.statusText = update;
	});
};

});