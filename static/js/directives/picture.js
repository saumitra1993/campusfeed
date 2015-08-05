angular.module('campusfeed').directive('camera', function() {
   return {
      restrict: 'A',
      require: 'ngModel',
      link: function(scope, elm, attrs, ctrl) {

         elm.on('click', function() {
           if(scope.creating == "channel" || scope.creating == "user"){
              navigator.camera.getPicture(function (imageURI) {
                 scope.$apply(function() {
                    ctrl.$setViewValue(imageURI);
                 });
              }, function (err) {
                 ctrl.$setValidity('error', false);
              }, { 
                  quality : 75,
                  destinationType : Camera.DestinationType.FILE_URI,
                  sourceType : Camera.PictureSourceType.PHOTOLIBRARY,
                  allowEdit : true,
                  encodingType: Camera.EncodingType.JPEG,
                  targetWidth: 400,
                  targetHeight: 400,
                  popoverOptions: CameraPopoverOptions,
                  saveToPhotoAlbum: false 
              });
            }
            else
            {
                navigator.camera.getPicture(function (imageURI) {
                 scope.$apply(function() {
                    ctrl.$setViewValue(imageURI);
                 });
                }, function (err) {
                 ctrl.$setValidity('error', false);
                 }, { 
                  quality : 100,
                  destinationType : Camera.DestinationType.FILE_URI,
                  sourceType : Camera.PictureSourceType.PHOTOLIBRARY,
                  encodingType: Camera.EncodingType.JPEG,
                  popoverOptions: CameraPopoverOptions,
                  saveToPhotoAlbum: false 
              });
            }
         });  
      }
   };
});