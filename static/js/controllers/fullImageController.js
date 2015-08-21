angular.module('campusfeed').controller('ModalInstanceCtrl', function ($scope, $modalInstance, selectedImgUrl) {

  $scope.selectedImgUrl = selectedImgUrl;

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };

});