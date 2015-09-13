angular.module("campusfeed").controller("channelController", function($scope,$location,$modal,$http,appfactory,$routeParams){
$scope.errorBox=false;
$scope.getNotifications = true;
$scope.channelDetails=[];
$scope.channelPosts=[];
$scope.limit=10;
$scope.offset=0;
$scope.is_admin = 0;
$scope.channel_pending_bit = 0;
$scope.moreAval=1;
$scope.channel_id = $routeParams.channelId;
$scope.type=$routeParams.type;

$scope.loggedIn = appfactory.loggedIn;
$scope.statusText = "Load more";
$scope.pending_request = 1;
$scope.approveText = "Approve";
$scope.followText = 'Follow';
$scope.showDetails=0;
$scope.anyAval=1;
$scope.followers = {};
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


appfactory.channelDetails($scope.channel_id).then(function(data){
	$scope.channelDetails=data;
	$scope.channel_pending_bit = data.pending_bit;
	$scope.is_admin = data.is_admin;
	if($scope.channelDetails.is_following != 1){
		$location.path('/channels/unrelated/'+$scope.channel_id);
	}
	else{
		$location.path('/channels/related/'+$scope.channel_id);
	}
},function(status){
	$scope.errorBox=true;
});



$scope.getChannelDetails = function(){
	$scope.showDetails=1;
	
};

$scope.followerDetails = function(){
	appfactory.getFollowers($scope.channel_id).then(function(data){
		$scope.followers = data.channel_followers;
	},function(data){
		$scope.errorBox = true;
	});
};

$scope.openedit = function () {
    var modalInstance = $modal.open({
      animation: $scope.animationsEnabled,
      controller: 'EditChannelCtrl',
      templateUrl: 'editchannel.html',
      resolve: {
        channel_id: function () {
          return $scope.channel_id;
        }
      }
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
	if(appfactory.loggedIn == true){
		appfactory.followChannel($scope.channel_id, $scope.getNotifications).then(function(data){
		
			$scope.type='related';
			$scope.channelDetails.num_followers++;
			$scope.followText = 'Follow';
		},
		function(status) {
			$scope.errorBox=true;
			$scope.followText = 'Follow';
		},function(update){
			$scope.followText = update;
		});
	}
	else{
		console.log("Here");
		$location.path('/login').search('redirect_to', 'channels/unrelated/'+$scope.channel_id)
	}
	
};
$scope.unfollow = function(){
	appfactory.unfollowChannel($scope.channel_id).then(function(data){
		
			$scope.type='unrelated';
			$scope.channelDetails.num_followers--;
			appfactory.channelDetails($scope.channel_id).then(function(data){
				$scope.channelDetails=data;
			},function(status){
				$scope.errorBox=true;
			});
		},
		function(status) {
			$scope.errorBox=true;
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