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

angular.module('myApp').factory('AuthService',
  ['$q', '$timeout', '$http',
  function ($q, $timeout, $http) {

    // create user variable
    var user = null;
    var logindata = null;

    // return available functions for use in controllers
    return ({
      isLoggedIn: isLoggedIn,
      login: login,
      logout: logout,
      register: register,
      getUserStatus: getUserStatus,
      getLoginData: getLoginData
    });

    function getLoginData(){
      return logindata;
    }
    function isLoggedIn() {
      if(user) {
        return true;
      } else {
        return false;
      }
    }

    function login(email, password) {

      // create a new instance of deferred
      var deferred = $q.defer();

      // send a post request to the server
      $http.post('/api/user/login', {email: email, pwd: password})
        // handle success
        .success(function (data, status) {
          if(status === 200 && data.result){
            user = true;
            logindata=data;
            console.log(logindata);

            deferred.resolve();
          } else {
            user = false;
            logindata =data;
            console.log(logindata);

            deferred.reject();
          }
        })
        // handle error
        .error(function (data) {
          user = false;
          deferred.reject();
        });

      // return promise object
      return deferred.promise;

    }

    function logout() {

      // create a new instance of deferred
      var deferred = $q.defer();

      // send a get request to the server
      $http.get('/api/user/logout')
        // handle success
        .success(function (data) {
          user = false;
          logindata=null;

          deferred.resolve();
        })
        // handle error
        .error(function (data) {
          user = false;
          logindata=null;

          deferred.reject();
        });

      // return promise object
      return deferred.promise;

    }

    function register(name, email, password) {

      // create a new instance of deferred
      var deferred = $q.defer();

      // send a post request to the server
      $http.post('/api/user/register', {name: name, email: email, pwd: password})
        // handle success
        .success(function (data, status) {
          if(status === 200 && data.result){
            deferred.resolve();
          } else {
            deferred.reject();
          }
        })
        // handle error
        .error(function (data) {
          deferred.reject();
        });

      // return promise object
      return deferred.promise;

    }

    function getUserStatus() {
      return $http.get('/api/user/status')
      // handle success
      .success(function (data) {
        if(data.status){
          user = true;
        } else {
          user = false;
        }
      })
      // handle error
      .error(function (data) {
        user = false;
      });
    }

}]);

/*

angular.module('myApp').factory('DevicesDataService',
  ['$q', '$timeout', '$http',
  function ($q, $timeout, $http) {

    var devicelist=null;
    
    return ({
      getDeviceList : getDeviceList,
      fetchDeviceList : fetchDeviceList
    });

    function getDeviceList()
    {
      return devicelist;
    }

    function fetchDeviceList(owner_id) {
      return $http.get('/api/devices/'+owner_id)
      // handle success
      .success(function (data) {
        if(data.result){
          devicelist=data.devicelist;
          
        } 
        else {
          devicelist=data.msg;
          
        }
      })
      // handle error
      .error(function (data) {
        devicelist="Data Fetch Error!";
        
      });

      //return devicelist;
    }


}]);

*/