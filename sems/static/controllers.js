
angular.module('myApp').controller('loginController',
  ['$scope', '$location', 'AuthService',
  function ($scope, $location, AuthService) {

    $scope.login = function () {

      // initial values
      $scope.error = false;
      $scope.disabled = true;

      // call login from service
      AuthService.login($scope.loginForm.email, $scope.loginForm.password)
        // handle success
        .then(function () {
          $location.path('/');
          $scope.disabled = false;
          $scope.loginForm = {};
        })
        // handle error
        .catch(function () {
          $scope.error = true;
          //$scope.errorMessage = "Invalid username and/or password";
          $scope.errorMessage = AuthService.getLoginData().msg;
          $scope.disabled = false;
          $scope.loginForm = {};
        });

    };

}]);

angular.module('myApp').controller('logoutController',
  ['$scope', '$location', 'AuthService',
  function ($scope, $location, AuthService) {

    $scope.logout = function () {

      // call logout from service
      AuthService.logout()
        .then(function () {
          $location.path('/login');
        });

    };

}]);

angular.module('myApp').controller('homeController',
  ['$scope', '$location', 'AuthService',
  function ($scope, $location, AuthService) {

    $scope.logindata=AuthService.getLoginData();

}]);

angular.module('myApp').controller('profileController',
  ['$scope', '$location', 'AuthService',
  function ($scope, $location, AuthService) {

    $scope.logindata=AuthService.getLoginData();
    

}]);

angular.module('myApp').controller('addDeviceController',
  ['$scope', '$location', 'AuthService', '$http',
  function ($scope, $location, AuthService, $http) {

    $scope.logindata=AuthService.getLoginData();

    $scope.device_name="";
    $scope.deviceaddedsuccessfully=0;
    $scope.msg="";
    
    $scope.addDevice=function(){
      
      var url='api/devices/'+$scope.logindata.id;
      $http.post(url, {name:$scope.device_name})
      .success(function(data){
          if(data.result){
          $scope.deviceaddedsuccessfully=1;
          $scope.msg=data.msg;
          }
          else{
          $scope.deviceaddedsuccessfully=2;
          $scope.msg=data.msg;
          }
      })
      .error(function(data){
        $scope.deviceaddedsuccessfully=2;
        $scope.msg="Data Upload Error!!!";
      });
    };

}]);


angular.module('myApp').controller('devicesController',
  ['$scope', '$location', 'AuthService', '$http', '$route',
  function ($scope, $location, AuthService, $http, $route) {

    $scope.logindata=AuthService.getLoginData();
    
    var devicelist;

    var url='/api/devices/'+$scope.logindata.id;
    $http.get(url).then( function(response) {
      if(response.data.result)
      {
        $scope.devicelist=response.data.devicelist;
        $scope.devicelistfound=response.data.result;
      }
      else{
        $scope.devicelist=null;
        $scope.devicelistfound=response.data.result;
        $scope.errorMessage=response.data.msg;
      }
      
      console.log(response.data);
    });

    console.log($scope.devicelist);
    console.log($scope.devicelistfound);

    $scope.updateDeviceState=function(device_id,device_state)
    {
      var url='api/device/'+device_id+'/state';
      $http.post(url, {state:device_state})
      .success(function(data){
        if(!data.result){
          $scope.deviceStateUpdateError="Failed to update Device state."
        }
      })
      .error(function(data){
          $scope.errorMessage="Data Update Error!!!"
      });  
    };

    $scope.deleteDevice=function(device_id)
    {
      //alert("Dummy Delete Function!!!");
      
      var url='api/device/'+device_id;
      $http.delete(url)
      .success(function(data){
        if(data.result){
          $route.reload();
        }
        else{
          $scope.errorMessage=data.msg;
        }
      })
      .error(function(data){
          $scope.errorMessage="Data Update Error!!!"
      }); 
      
    };


    /*
    DevicesDataService.fetchDeviceList($scope.logindata.id)
    .then(function()
    {
      $scope.devicelist=DevicesDataService.getDeviceList();
    });

    console.log(String($scope.devicelist));

    if($scope.devicelist instanceof String){
      $scope.devicelistfound=false;
    }
    else{
      $scope.devicelistfound=true;
    }
    
    console.log(String($scope.devicelistfound));
    */


}]);

angular.module('myApp').controller('registerController',
  ['$scope', '$location', 'AuthService',
  function ($scope, $location, AuthService) {

    $scope.register = function () {

      // initial values
      $scope.error = false;
      $scope.disabled = true;

      // call register from service
      AuthService.register($scope.registerForm.name,
                           $scope.registerForm.email,
                           $scope.registerForm.password)
                           
        // handle success
        .then(function () {
          $location.path('/login');
          $scope.disabled = false;
          $scope.registerForm = {};
        })
        // handle error
        .catch(function () {
          $scope.error = true;
          $scope.errorMessage = "Something went wrong!";
          $scope.disabled = false;
          $scope.registerForm = {};
        });

    };

}]);