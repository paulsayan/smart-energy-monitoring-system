/*

    Smart Energy Monitoring System
    Copyright (C) 2018 - Sayan Paul

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

*/

var myApp = angular.module('myApp', ['ngRoute']);

myApp.config(function ($routeProvider) {
  $routeProvider
    .when('/', {
      templateUrl: 'static/partials/home.html',
      controller: 'homeController',
      access: {restricted: true}
    })
    .when('/login', {
      templateUrl: 'static/partials/login.html',
      controller: 'loginController',
      access: {restricted: false}
    })
    .when('/logout', {
      controller: 'logoutController',
      access: {restricted: true}
    })
    .when('/register', {
      templateUrl: 'static/partials/register.html',
      controller: 'registerController',
      access: {restricted: false}
    })
    .when('/one', {
      template: '<h1>This is page one!</h1>',
      access: {restricted: true}
    })
    .when('/two', {
      template: '<h1>This is page two!</h1>',
      access: {restricted: false}
    })
    .when('/profile', {
      templateUrl: 'static/partials/profile.html',
      controller: 'profileController',
      access: {restricted: true}
    })
    .when('/devices', {
      templateUrl: 'static/partials/devices.html',
      controller: 'devicesController',
      access: {restricted: true}
    })
    .when('/add_device', {
      templateUrl: 'static/partials/add_device.html',
      controller: 'addDeviceController',
      access: {restricted: true}
    })
    .when('/device/:device_id/info', {
      templateUrl: 'static/partials/device_info.html',
      controller: 'deviceInfoController',
      access: {restricted: true}
    })
    .when('/device/:device_id/sessions', {
      templateUrl: 'static/partials/sessions.html',
      controller: 'sessionsController',
      access: {restricted: true}
    })
    .when('/device/:device_id/realtimedata', {
      templateUrl: 'static/partials/realtimedata.html',
      controller: 'realtimeDataController',
      access: {restricted: true}
    })
    .when('/bills', {
      templateUrl: 'static/partials/bills.html',
      controller: 'billsController',
      access: {restricted: true}
    })
    .when('/settings', {
      templateUrl: 'static/partials/settings.html',
      controller: 'settingsController',
      access: {restricted: true}
    })
    .when('/notifications', {
      templateUrl: 'static/partials/notifications.html',
      controller: 'notificationsController',
      access: {restricted: true}
    })
    .otherwise({
      redirectTo: '/'
    });
});

myApp.run(function ($rootScope, $location, $route, AuthService) {
  $rootScope.$on('$routeChangeStart',
    function (event, next, current) {
      AuthService.getUserStatus()
      .then(function(){
        if (next.access.restricted && !AuthService.isLoggedIn()){
          $location.path('/login');
          $route.reload();
        }
      });
  });
});