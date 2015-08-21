angular.module('campusfeed', ['ngRoute','ngSanitize','mobile-angular-ui','mobile-angular-ui.gestures','ImageCropper','ui.bootstrap'])
.config(function($routeProvider){
  $routeProvider
   .when('/',                                      
    {controller:'homeController',
    templateUrl:'html/home.html'})
   .when('/login',                                      
    {controller:'loginController',
    templateUrl:'html/login.html'})
   .when('/signup',                                      
    {controller:'signupController',
    templateUrl:'html/signup.html'})
   .when('/createchannel',                                      
    {controller:'createChannelController',
    templateUrl:'html/createchannel.html'})
   .when('/channels/:channelId/addpost',                                      
    {controller:'addPostController',
    templateUrl:'html/addpost.html'})
   .when('/channels/:channelId/addadmin',                                      
    {controller:'addAdminController',
    templateUrl:'html/addadmin.html'})
   .when('/mychannels',                                      
    {controller:'myChannelsController',
    templateUrl:'html/channel_listing.html'})
   .when('/followedchannels/:action',                                      
    {controller:'followedChannelsController',
    templateUrl:'html/channel_listing.html'})
   .when('/discoverchannels',                                      
    {controller:'allChannelsController',
    templateUrl:'html/home.html'})
   .when('/logout',                                      
    {controller:'logoutController',
    templateUrl:'html/logout.html'})
   .when('/channels/:type/:channelId',                                      
    {controller:'channelController',
    templateUrl:'html/channel_home.html'})
   .when('/resetpassword/:forgotId',                                      
    {controller:'resetPasswordController',
    templateUrl:'html/resetpassword.html'})
   .otherwise({redirectTo: '/' });

});


