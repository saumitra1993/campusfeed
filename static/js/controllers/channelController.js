angular.module("campusfeed").controller("channelController", function($scope,$location,$uibModal,$http,appfactory,$routeParams){
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
$scope.threads = [];
$scope.loggedIn = appfactory.loggedIn;
$scope.statusText = "Load more";
$scope.pending_request = 1;
$scope.approveText = "Approve";
$scope.followText = 'Follow';
$scope.showDetails=0;
$scope.anyAval=1;
$scope.followers = {};
$scope.sidebar = 0;
$scope.discussionText = "Discussions";
$scope.statusText2 = "Load more";
$scope.threadTopicBox = 0;
$scope.addThreadText = "Add";
$scope.addCommentText = "Add";
$scope.errorBox2 = false;
$scope.threadInSidebar = 1;
$scope.thread_id = -1;	//used when sending a comment 
$scope.comments = [];
$scope.thread_topic = "";
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
	$scope.sidebarHead = $scope.channelDetails.channel_name+" discussion threads";
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
    var modalInstance = $uibModal.open({
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

$scope.loadMorePosts = function(){
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
    var modalInstance = $uibModal.open({
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

$scope.addThread = function(topic){
	$scope.addThreadText = "Loading...";
	appfactory.addThread($scope.channel_id, topic).then(function(data){
		$scope.addThreadText = "Add";
		$scope.topic = "";
		$scope.threadTopicBox = 0;
		$scope.threads.unshift(data.thread);
	},
	function(status) {
		$scope.addThreadText = "Add";
		$scope.errorBox2=true;
	});
};

$scope.getThreads = function(){
	if($scope.sidebar == 0){
		$scope.sidebar = 1;
		$scope.discussionsText = "Click to collapse";
		appfactory.getThreads($scope.channel_id,$scope.limit,$scope.offset).then(function(data){
			$scope.threads = data.threads;
			$scope.discussionText = "Discussions";
		},function(status){
			$scope.errorBox2=true;
			$scope.discussionText = "Discussions";
		});
	}
	else{
		$scope.sidebar = 0;
	}
};

$scope.gotoThread = function(thread){
	$scope.sidebarHead = thread.topic;
	$scope.threadInSidebar = 0;
	$scope.thread_id = thread.thread_id;
	$scope.limit = 10;
	$scope.offset=0;
	appfactory.getComments($scope.channel_id,thread.thread_id,$scope.limit,$scope.offset).then(function(data){
		$scope.comments = data.threadDiscussions;
		$scope.comments.reverse();
		$scope.threadInSidebar = 0;
	},function(status){
		$scope.errorBox2=true;
	});
};

$scope.loadMoreThreads = function(){
	$scope.statusText2 = "Loading...";
	$scope.offset = $scope.limit;
	$scope.limit += 10;
	appfactory.getThreads($scope.channel_id,$scope.limit,$scope.offset).then(function(data){
		var threads = data.threads;
		for(var j=0;j<threads.length;j++){
			$scope.threads.push(threads[j]);
		}
		$scope.statusText2 = "Load more";
	},function(status){
		$scope.errorBox2=true;
		$scope.statusText2 = "Load more";
	});
};

$scope.loadMoreThreadComments = function(){
	$scope.statusText2 = "Loading...";
	$scope.offset = $scope.limit;
	$scope.limit += 10;
	appfactory.getComments($scope.channel_id,$scope.thread_id,$scope.limit,$scope.offset).then(function(data){
		var comments = data.threadDiscussions;
		for(var j=0;j<comments.length;j++){
			$scope.comments.unshift(comments[j]);
		}
		$scope.statusText2 = "Load more";
	},function(status){
		$scope.errorBox2=true;
		$scope.statusText2 = "Load more";
	});
};

$scope.backToThreads = function(){
	$scope.comments = [];
	$scope.threadInSidebar = 1;
	$scope.sidebarHead = $scope.channelDetails.channel_name+" discussion threads";
	$scope.limit = 10;
	$scope.offset=0;
};

$scope.addComment = function(comment){
	$scope.addCommentText = "Loading...";
	appfactory.addComment($scope.channel_id, $scope.thread_id, comment).then(function(data){
		$scope.addCommentText = "Add";
		$scope.comment = "";
		$scope.comments.push(data.comment);
	},
	function(status) {
		$scope.addThreadText = "Add";
		$scope.errorBox2=true;
	});
};

$scope.deleteThread = function(thread){
	appfactory.deleteThread($scope.channel_id, thread.thread_id).then(function(data){
		var index = $scope.threads.indexOf(thread);
		$scope.threads.splice(index, 1);
	},function(status){
		$scope.errorBox2=true;
	});
};

$scope.deleteComment = function(comment){
	appfactory.deleteComment($scope.channel_id,$scope.thread_id,comment.comment_id).then(function(data){
		var index = $scope.comments.indexOf(comment);
		$scope.comments.splice(index, 1);
	},function(status){
		$scope.errorBox2=true;
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