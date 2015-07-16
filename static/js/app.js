angular.module("campusfeed",['ngRoute','ngCookies','ui.bootstrap']);

angular.module("campusfeed").config(function($routeProvider){
  $routeProvider
   .when('/',                                      //add to cart button
    {controller:'homeController',
    templateUrl:'views/home.html'})
  .when('/product/:productId',                                      //add to cart button
    {controller:'productController',
    templateUrl:'views/product-detail.html'})
  .when('/checkout',
    {controller:'checkoutController',
    templateUrl:'views/checkout.html'})
  .when('/paymentsuccess',
    {controller:'paymentController',
    templateUrl:'views/paymentsuccess.html'})
  .when('/login',
      {controller:'loginController',
      templateUrl:'views/login.html'})
  .when('/register',
      {controller:'regController',
      templateUrl:'views/register.html'})
  .when('/productlisting',
      {controller:'PLController',
      templateUrl:'views/productlisting.html'})
  .when('/searchresults',
      {controller:'srController',
      templateUrl:'views/searchresults.html'})
  .when('/myorder',
      {controller:'myoController',
      templateUrl:'views/myorder.html'})
  .when('/checkout',
      {controller:'checkController',
      templateUrl:'views/checkout.html'})    
  .otherwise({redirectTo: '/' });

});
