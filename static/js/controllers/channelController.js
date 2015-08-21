angular.module("campusfeed").controller("channelController", function($scope,$location,$modal,$http,appfactory,$routeParams){
$scope.errorBox=false;
$scope.getNotifications = true;
$scope.channelDetails=[];
$scope.channelPosts=[];
$scope.limit=10;
$scope.offset=0;
$scope.moreAval=1;
$scope.channel_id = $routeParams.channelId;
$scope.type=$routeParams.type;
$scope.otherData = appfactory.active_channel;
$scope.channel_pending_bit = appfactory.active_channel.pending_bit;
$scope.is_admin = appfactory.active_channel.is_admin;
$scope.statusText = "Load more";
$scope.pending_request = 1;
$scope.approveText = "Approve";
$scope.followText = 'Follow';
$scope.showDetails=0;
$scope.anyAval=1;
appfactory.channelPosts($scope.channel_id, $scope.limit, $scope.offset).then(function(data){
	if(data.posts.length>0){
		$scope.channelPosts=data.posts;
	}
	else{
		$scope.anyAval=0;
	}
	$scope.pending_request = 0;
},function(status){
	$scope.errorBox=true;
	$scope.pending_request = 0;
});

if($scope.type == 'unrelated'){
	appfactory.channelDetails($scope.channel_id).then(function(data){
		$scope.channelDetails=data;
	},function(status){
		$scope.errorBox=true;
	});
}
$scope.getChannelDetails = function(){
	$scope.showDetails=1;
	appfactory.channelDetails($scope.channel_id).then(function(data){
		$scope.channelDetails=data;
	},function(status){
		$scope.errorBox=true;
	});
};

$scope.loadMore = function(){
	$scope.statusText = "Loading...";
	$scope.offset = $scope.limit;
	$scope.limit += 10;
	appfactory.channelPosts($scope.channel_id, $scope.limit, $scope.offset).then(function(data){
		if(data.posts.length>0){
			$scope.channelPosts = $scope.channelPosts.concat(data.posts);
		}
		else{
			$scope.moreAval=0;
		}
		$scope.statusText = "Load More";		
	},function(status){
		$scope.moreAval=0;
		$scope.errorBox=true;
	},function(update){
		$scope.statusText = update;
	});
};
$scope.open = function (imgUrl) {
     $scope.imgUrl = imgUrl; 
    var modalInstance = $modal.open({
      animation: $scope.animationsEnabled,
      controller: 'ModalInstanceCtrl',
      templateUrl: 'fullImage.html',
      size:'lg',
      resolve: {
        selectedImgUrl: function () {
          return $scope.imgUrl;
        }
      }
    });
  };
$scope.approve = function(post){
	post.approveText = "Loading...";
	appfactory.approvePost($scope.channel_id,post.post_id).then(function(data){
		post.pending_bit=0;
		post.approveText = "Approve";
	},function(status){
		$scope.errorBox=true;
		post.approveText = "Approve";
	},function(update){
		$scope.approveText = update;
	});
};
$scope.follow = function(){
	$scope.followText = "Loading...";
	appfactory.followChannel($scope.channel_id, $scope.getNotifications).then(function(data){
		
			$scope.type='related';
			$scope.otherData.num_followers++;
			$scope.followText = 'Follow';
		},
		function(status) {
			$scope.errorBox=true;
			$scope.followText = 'Follow';
		},function(update){
			$scope.followText = update;
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