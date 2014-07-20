(function(){

    var app = angular.module('todo', [
        'ngCookies',
        'ui.date',
        'ui-rangeSlider',
        'restangular',
        'ngRoute']);

    app.config(['$routeProvider', function($routeProvider) {

        $routeProvider.
            when('/', {
                controller: 'ListController',
                templateUrl:'list.html'
            }).
            when('/edit/:entryId', {
                controller: 'EditController',
                templateUrl:'/add_entry',
                resolve: {
                    entry: function(EntryRestangular, $route){
                        return EntryRestangular.one('entries', $route.current.params.entryId).get();
                    }
                }
            }).
            when('/new', {
                controller: 'AddController',
                templateUrl:'/add_entry'
            }).
            otherwise({redirectTo:'/'});
    }]);

    app.run(function run($http, $cookies) {
        $http.defaults.headers.post['X-CSRFToken'] = $cookies['csrftoken'];
        $http.defaults.headers.common['X-CSRFToken'] = $cookies['csrftoken'];
    });

    app.controller('ListController', ['$scope', 'EntryRestangular', function($scope, EntryRestangular) {
        $scope.entries = [];

        $scope.dateOptions1 = {
            maxDate: 0
        };

        $scope.dateOptions2 = {
            maxDate: 0
        };

        $scope.$watch('date_start', function() {
            $scope.dateOptions2.minDate = $scope.date_start;
        });

        $scope.$watch('date_finish', function(){
            if ($scope.date_finish <= new Date()) {
                $scope.dateOptions1.maxDate = $scope.date_finish;
            }
        });

        $scope.totalKm = function() {
            var distance = 0;
            if ($scope.filteredEntries) {
                $scope.filteredEntries.forEach(function(el) {
                    distance += el['distance'];
                });
            }
            return distance;
        };

        $scope.totalTime = function() {
            var result = "";
            var time = 0;
            if ($scope.filteredEntries) {
                $scope.filteredEntries.forEach(function(el){
                    time += el['duration_minutes'];
                });
                var hours = parseInt(time / 60);
                var minutes = parseInt(time % 60);
                result = hours + " hr " + minutes + " min";
            }
            $scope.totalMinutes = time;
            return result;
        };

        $scope.totalSpeed = function() {
            var speed = 0;
            var distance = $scope.totalKm();
            var time = $scope.totalMinutes;
            if (time > 0) {
                speed = distance / (time/60);
            }
            return speed;
        };

        EntryRestangular.all('entries').getList().then(function(entries) {
            $scope.entries = entries;
        });

    }]);

    app.filter('dateFilter', function() {
        return function(arr, start_date, end_date) {
            var result = [];

		    var start_date = start_date ? start_date : 0;
		    var end_date = end_date ? new Date(end_date).setHours(23,59,59,999) : new Date().getTime();

		    if (arr && arr.length > 0) {
			    $.each(arr, function (index, el) {
                    var dt = new Date(el['date']);
				    if (dt >= start_date && dt <= end_date)
				    {
					    result.push(el);
				    }
			    });
            }
            return result;
        };
    });

    app.filter('minutes2hours', function () {
    return function (value, max) {
        if (value == max) { return 'All'; }

        var h = parseInt(value / 60);
        var m = parseInt(value % 60);

        var hStr = (h > 0) ? h + 'hr'  : '';
        var mStr = (m > 0) ? m + 'min' : '';
        var glue = (hStr && mStr) ? ' ' : '';

        return hStr + glue + mStr;
    };
});


    app.controller('AddController', ['$scope', '$location', 'EntryRestangular', function($scope, $location, EntryRestangular) {
        $scope.dateOptions = {
            changeYear: true,
            changeMonth: true,
            dateFormat: 'yy-mm-dd',
            maxDate: 0
        };

        $scope.sliderOptions = {
            min: 0,
            max: 1440,
            step: 1,
            disabled: false
        };

        $scope.entry = {
            duration_minutes: 1
        };

        $scope.saveEntry = function() {
            EntryRestangular.all('entries').post($scope.entry).then(function(entry) {
                $location.path('/');
            });
        }

    }]);

    app.controller('EditController', ['$scope', '$location', 'EntryRestangular', 'entry', function($scope, $location, EntryRestangular, entry) {

        var original = entry;
        $scope.entry = EntryRestangular.copy(original);

        $scope.isClean = function() {
            return angular.equals(original, $scope.entry);
        }

        $scope.sliderOptions = {
            min: 0,
            max: 1440,
            step: 1,
            disabled: false
        };

        $scope.dateOptions = {
            changeYear: true,
            changeMonth: true,
            dateFormat: 'yy-mm-dd',
            maxDate: 0
        };

        $scope.saveEntry = function() {
            $scope.entry.put().then(function() {
                $location.path('/');
            });
        };

        $scope.removeEntry = function() {
            $scope.entry.remove().then(function() {
                $location.path('/');
            });
        }

    }]);


    app.factory('EntryRestangular', function (Restangular) {
    return Restangular.withConfig(function (RestangularConfigurer) {
        RestangularConfigurer.setBaseUrl('/api/v1');
        RestangularConfigurer.addResponseInterceptor(function(response, operation, what, url) {
            var newResponse;
            // Tastypie returns object, but we need only list part
            if (operation === "getList") {
                newResponse = response.objects;
                newResponse.metadata = response.meta;
            } else {
                newResponse = response;
            }
            return newResponse;
        });
        RestangularConfigurer.setRequestSuffix('/?format=json');
    });
});

})();