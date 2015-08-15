angular.module("campusfeed").controller("homeController", function($scope,$location,appfactory,$q,$routeParams){
$scope.limit=10;
$scope.offset=0;
$scope.moreAval=1;
$scope.pending_request=1;
$scope.statusText = "Load more";
$scope.errorBox=false;
$scope.anyAval=1;
$scope.approveText = "Approve";
$scope.tags = ["course","club", "committee", "event"];
if(appfactory.loggedIn==false){
	$location.path('/login');
}
else{
	appfactory.feed($scope.limit, $scope.offset).then(function(data){
		$scope.pending_request=0;
		if(Object.keys(data.channel_posts).length>0){
			$scope.channelPosts=data.channel_posts;
		}
		else{
			$scope.anyAval=0;
		}
	},function(status){
		$scope.errorBox=true;
		$scope.pending_request=0;
	},function(update){
		$scope.statusText = update;
	});
}

$scope.loadMore = function(){
	$scope.offset = $scope.limit;
	$scope.limit += 10;
	$scope.statusText = "Loading...";
	appfactory.feed($scope.limit, $scope.offset).then(function(data){
		if(Object.keys(data.channel_posts).length>0){
			$scope.channelPosts = $scope.channelPosts.concat(data.channel_posts);
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
$scope.approve = function(channel_id,post){
	post.approveText = "Loading...";
	appfactory.approvePost(channel_id,post.post_id).then(function(data){
		post.pending_bit=0;
		post.approveText = "Approve";
	},
	function(status) {
		$scope.errorBox=true;
		post.approveText = "Approve";
	},function(update){
		$scope.approveText = update;
	});
};
function makeid()
{
    var text = "";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

    for( var i=0; i < 5; i++ )
        text += possible.charAt(Math.floor(Math.random() * possible.length));

    return text;
}
});