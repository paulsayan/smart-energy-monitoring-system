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
  ['$scope', '$location', 'AuthService','$http', '$interval',
  function ($scope, $location, AuthService, $http, $interval) {

    $scope.logindata=AuthService.getLoginData();

    $scope.energyc_quota_exceeded=-1;

    var url='/api/updatebills?user='+$scope.logindata.id;
    $http.get(url).then( function(response) {
      if(response.data.result)
      {
        $scope.billstartdate=response.data.billstartdate;
        $scope.billenddate=response.data.billenddate;
        $scope.energyc_quota=response.data.energyc_quota;
        
        console.log(response.data);
      }
      else{
        
      }

    });

    $scope.viewRealtimeBill=function()
    {
        var url='/api/realtimebill/'+$scope.logindata.id;

        $http.get(url).then( function(response) {
        if(response.data.result)
        {
          $scope.devicelist=response.data.devicelist;
          $scope.totalenergyc=response.data.totalenergyc;
          $scope.totalenergyc_cs=response.data.totalenergyc_completedsessions;
          $scope.totalenergyc_os=response.data.totalenergyc_ongoingsessions;

          $scope.dataFound=true;
          console.log(response.data);
        }
        else{
          $scope.devicelist=null;
          $scope.dataFound=false;
          $scope.errormsg=response.data.msg;
        }

        if($scope.totalenergyc==0)
        {
          $scope.dataFound=false;
          $scope.errormsg=$scope.devicelist;
        }
    
        });

        if($scope.totalenergyc>$scope.energyc_quota)
        {
          $scope.energyc_quota_exceeded=1;
          var diff=($scope.totalenergyc-$scope.energyc_quota)/1000;
          $scope.energyc_quota_exceeded_msg=diff.toFixed(3)+" Units or kWh";
        }
        else
        {
          $scope.energyc_quota_exceeded=0;
          var percent=($scope.totalenergyc/$scope.energyc_quota)*100;
          $scope.energyc_quota_notexceeded_msg=percent.toFixed(2)+" %";
        }

    };

    //$scope.viewRealtimeBill();

    $scope.datafetch_timer=$interval(function(){$scope.viewRealtimeBill(); }, 2000);
    $scope.$on('$destroy',function(){$interval.cancel($scope.datafetch_timer);  });

}]);

angular.module('myApp').controller('billsController',
  ['$scope', '$location', 'AuthService','$http',
  function ($scope, $location, AuthService, $http) {

    $scope.logindata=AuthService.getLoginData();

    $scope.viewAnyBill=function()
    {
        var startdate=$scope.startdate.getFullYear()+"-"+($scope.startdate.getMonth()+1)+"-"+$scope.startdate.getDate();
        var enddate=$scope.enddate.getFullYear()+"-"+($scope.enddate.getMonth()+1)+"-"+$scope.enddate.getDate();

        //alert(startdate+" to "+enddate);

        var url='/api/anybill/'+$scope.logindata.id+'?startdate='+startdate+'&enddate='+enddate;
        $http.get(url).then( function(response) {
        if(response.data.result)
        {
          $scope.devicelist=response.data.devicelist;
          $scope.totalenergyc=response.data.totalenergyc;
          $scope.dataFound=true;
          console.log(response.data);
        }
        else{
          $scope.devicelist=null;
          $scope.dataFound=false;
          $scope.errorMessage=response.data.msg;
        }
    
        });

    };

}]);


angular.module('myApp').controller('profileController',
  ['$scope', '$location', 'AuthService',
  function ($scope, $location, AuthService) {

    $scope.logindata=AuthService.getLoginData();
    

}]);

angular.module('myApp').controller('settingsController',
  ['$scope', '$location', 'AuthService','$http',
  function ($scope, $location, AuthService, $http) {

    $scope.logindata=AuthService.getLoginData();
    
    var url='/api/user/'+$scope.logindata.id+"/settings";
    $http.get(url).then( function(response) {
      if(response.data.result)
      {
        $scope.settings=response.data.settings;
        $scope.settingsFound=true;
        console.log($scope.settings)
      }
      else{
        $scope.settings=null;
        $scope.settingsFound=false;
      }
    
    });

    $scope.SettingNametoLabel=function(settingname){
      if(settingname=="billingcycle"){
        return "Billing Cycle (in Days)"
      }
      else if(settingname=="lastbilldate"){
        return "Last Bill Date (YYYY-MM-DD)"
      }
      else if(settingname=="energyc_quota"){
        return "Energy Consumption Quota (in Wh)"
      }
      return null;
    };



}]);

angular.module('myApp').controller('notificationsController',
  ['$scope', '$location', 'AuthService', '$http',
  function ($scope, $location, AuthService, $http) {

    $scope.logindata=AuthService.getLoginData();
    
    var url='/api/notifications/'+$scope.logindata.id;
    $http.get(url).then( function(response) {
      if(response.data.result)
      {
        $scope.notifications=response.data.notifications;
        $scope.notificationsFound=true;
        console.log($scope.notifications)
      }
      else{
        $scope.notifications=null;
        $scope.notificationsFound=true;
      }
    
    });

    $scope.NotificationTypeToText=function(ntype)
    {
      if(ntype=="ENERGYC_QUOTA_EXCEEDED")
      {
        return "Energy Consumption Quota Exceeded!";
      }
      else
      {
        return "";
      }
    }

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

angular.module('myApp').controller('realtimeDataController',
  ['$scope', '$location', 'AuthService', '$http','$routeParams', '$interval',
  function ($scope, $location, AuthService, $http, $routeParams, $interval) {

    $scope.logindata=AuthService.getLoginData();

    $scope.device=null;
    $scope.deviceFound=false;

    $scope.dsession_starttime_found=false;

    var url='/api/device/'+$routeParams.device_id;
    $http.get(url).then( function(response) {
      if(response.data.result)
      {
        $scope.device=response.data;
        $scope.deviceFound=true;
        console.log(response.data);
      }
      else{
        $scope.device=null;
        $scope.deviceFound=false;
      }
    
    });
    
    $scope.getrealtimedata=function(){
    
      var url='/api/device/'+$routeParams.device_id+'/realtimedata';
      $http.get(url).then( function(response) {
        if(response.data.result)
        {
          $scope.dsession=response.data;
          //$scope.deviceON=true;
        
        }
        else{
          $scope.dsession=null;
          //$scope.deviceON=false;
        }
    
      });

      if($scope.dsession_starttime_found==false)
      {
        var url='/api/session/'+$scope.dsession.sid;
        $http.get(url).then( function(response) {
        if(response.data.result)
        {
          $scope.dsession_starttime=response.data.start_time;
          $scope.dsession_starttime_found=true;
          //$scope.deviceON=true;
        
        }
        else{
          $scope.dsession_starttime=null;
          //$scope.deviceON=false;
        }
    
        });


      }

      console.log("Interval Occurred.");
      console.log($scope.dsession);

    };

    $scope.datafetch_timer=$interval(function(){$scope.getrealtimedata(); }, 2000);
    $scope.$on('$destroy',function(){$interval.cancel($scope.datafetch_timer);  });

    /*
    if($scope.deviceFound){
      if($scope.device.state==true){
        
        console.log("testing..");
      }
    }
    */

}]);

angular.module('myApp').controller('deviceInfoController',
  ['$scope', '$location', 'AuthService', '$http','$routeParams',
  function ($scope, $location, AuthService, $http, $routeParams) {

    $scope.logindata=AuthService.getLoginData();

    $scope.device=null;
    $scope.deviceFound=false;

    var url='/api/device/'+$routeParams.device_id;
    $http.get(url).then( function(response) {
      if(response.data.result)
      {
        $scope.device=response.data;
        $scope.deviceFound=true;
        $scope.device.state=($scope.device.state==true)?"ON":"OFF";
      }
      else{
        $scope.device=null;
        $scope.deviceFound=false;
      }
    
    });

    $scope.getState=function(){
        return $scope.device.state?'ON':'OFF';
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

    $scope.selectdevice=function(device_id)
    {
      $scope.deviceselected=device_id;
    };


    /*
    $scope.gotoDeviceSettings=function(device_id){
      
      var url='#/device_settings/'+device_id;
      $location.path(url);

    };
    */

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

angular.module('myApp').controller('sessionsController',
  ['$scope', '$location', 'AuthService', '$http','$routeParams','$route',
  function ($scope, $location, AuthService, $http, $routeParams, $route) {

    $scope.logindata=AuthService.getLoginData();

    $scope.deletedallsessions=0;
    $scope.deletedsession=0;

    var url='/api/sessions/'+$routeParams.device_id;
    $http.get(url).then( function(response) {
      if(response.data.result)
      {
        $scope.sessionlist=response.data.sessionlist;
        $scope.sessionlistfound=response.data.result;
      }
      else{
        $scope.sessionlistlist=null;
        $scope.sessionlistfound=response.data.result;
        $scope.errorMessage=response.data.msg;
      }
      
      console.log(response.data);
    });

    console.log($scope.sessionlist);
    console.log($scope.sessionlistfound);

    $scope.deleteAllSessions=function()
    {
      
      var url='/api/sessions/'+$routeParams.device_id;
      $http.delete(url).then( function(response) {
        if(response.data.result)
        {
          $scope.deletedallsessions=1;
          $route.reload();
        }
        else{
          $scope.deletedallsessions=2;
          $scope.errormsg=response.data.msg;

        }
        
        
      });
    }

    $scope.deleteSessionById=function(session_id)
    {
      
      var url='/api/session/'+session_id;
      $http.delete(url).then( function(response) {
        if(response.data.result)
        {
          $scope.deletedsession=1;
          $route.reload();
        }
        else{
          $scope.deletedsession=2;
          $scope.errormsg=response.data.msg;

        }
        
        
      });


    }

    $scope.selectsession=function(session_id)
    {
      $scope.sessionselected=session_id;
    };

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