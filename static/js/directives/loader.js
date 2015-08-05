angular.module('campusfeed').directive('loading',   ['$http' ,function ($http)
    {
        return {
            restrict: 'A',
            link: function (scope, elm, attrs)
            {
                scope.isLoading = function () {
                    return $http.pendingRequests.length > 0;
                };

                scope.$watch(scope.isLoading, function (v)
                {
                    if(v){
                        scope.loading=true;
                    }else{
                        scope.loading=false;
                    }
                });
            }
        };
  }]);
  