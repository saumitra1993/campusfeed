angular.module("campusfeed").controller("addAdminController", function($scope,$location,$http,appfactory,$routeParams){
$scope.errorBox=false;
$scope.otherData = appfactory.active_channel;
$scope.users=[];
$scope.addAdminText = "Add as admin";
$scope.searchText = "Search";
$scope.search=function(){
    $scope.searchText = "Loading...";
	var name_arr = $scope.search_string.split(" ");
    for(var i=0;i<name_arr.length;i++){
        name_arr[i] = toTitleCase(name_arr[i]);
    }
    if(name_arr.length>0){
    	var search_string="?first_name="+name_arr[0];
    	if(name_arr.length==2){
    		search_string+="&last_name="+name_arr[1];
    	}
    	else{
    		search_string+="&last_name=";
    	}
    }
    appfactory.searchUser(search_string).then(function(data){
    	$scope.users=data.results;
        $scope.searchText = "Search";
    },function(status){
        $scope.errorBox=true;
        $scope.searchText = "Search";
    },function(update){
        $scope.searchText = update;
    });
};

$scope.addAdmin=function(user){
    $scope.addAdminText = "Loading...";
	appfactory.addAdmin(user,$scope.otherData.channel_id).then(function(data){
		    $scope.addAdminText = "Add as admin";
			user.is_admin=1;
		},
		function(status){
			$scope.errorBox=true;
		    $scope.addAdminText = "Add as admin";
	   },function(update){
            $scope.addAdminText = update;
       });
};

function toTitleCase(str)
{
    return str.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
}
});