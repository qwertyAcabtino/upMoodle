angular.module('upmApp').controller( 'calendarController', ['$scope', '$cookies', 'api', 'snackbar', '$location', 'uiCalendarConfig', '$compile',
	function($scope, $cookies, api, snackbar, $location, uiCalendarConfig, $compile) {

    var date = new Date();
    var d = date.getDate();
    var m = date.getMonth();
    var y = date.getFullYear();
    
    $scope.changeTo = 'Hungarian';
    /* event source that contains custom events on the scope */
    // $scope.events = [
    // {title: 'All Day Event',start: new Date(y, m, 1)},
    // {title: 'Long Event',start: new Date(y, m, d - 5),end: new Date(y, m, d - 2)},
    // {id: 999,title: 'Repeating Event',start: new Date(y, m, d - 3, 16, 0),allDay: false},
    // {id: 999,title: 'Repeating Event',start: new Date(y, m, d + 4, 16, 0),allDay: false},
    // {title: 'Birthday Party',start: new Date(y, m, d + 1, 19, 0),end: new Date(y, m, d + 1, 22, 30),allDay: false},
    // {title: 'Click for Google',start: new Date(y, m, 28),end: new Date(y, m, 29),url: 'http://google.com/'}
    // ];

     /* alert on eventClick */
     $scope.alertOnEventClick = function( date, jsEvent, view){
      console.log(date.title + ' was clicked ');
    };
    /* alert on Drop */
    $scope.alertOnDrop = function(event, delta, revertFunc, jsEvent, ui, view){
     $scope.alertMessage = ('Event Droped to make dayDelta ' + delta);
   };
   /* alert on Resize */
   $scope.alertOnResize = function(event, delta, revertFunc, jsEvent, ui, view ){
     $scope.alertMessage = ('Event Resized to make dayDelta ' + delta);
   };
   /* add and removes an event source of choice */
   $scope.addRemoveEventSource = function(sources,source) {
    var canAdd = 0;
    angular.forEach(sources,function(value, key){
      if(sources[key] === source){
        sources.splice(key,1);
        canAdd = 1;
      }
    });
    if(canAdd === 0){
      sources.push(source);
    }
  };
  /* add custom event*/
  $scope.addEvent = function() {
    $scope.events.push({
      title: 'Open Sesame',
      start: new Date(y, m, 28),
      end: new Date(y, m, 29),
      className: ['openSesame']
    });
  };
  /* remove event */
  $scope.remove = function(index) {
    $scope.events.splice(index,1);
  };
  /* Change View */
  $scope.changeView = function(view,calendar) {
    uiCalendarConfig.calendars[calendar].fullCalendar('changeView',view);
  };
  /* Change View */
  $scope.renderCalender = function(calendar) {
    if(uiCalendarConfig.calendars[calendar]){
      uiCalendarConfig.calendars[calendar].fullCalendar('render');
    }
  };
  /* Render Tooltip */
  $scope.eventRender = function( event, element, view ) { 
    element.attr({'tooltip': event.title,
     'tooltip-append-to-body': true});
    $compile(element)($scope);
  };
  /* config object */
  $scope.uiConfig = {
    calendar:{
      height: 600,
      editable: false,
      header:{
        left: 'title',
        center: '',
        right: 'month, agendaWeek, agendaDay, today, prev,next'
      },
      eventClick: $scope.alertOnEventClick,
      eventDrop: $scope.alertOnDrop,
      eventResize: $scope.alertOnResize,
      eventRender: $scope.eventRender,
      viewRender: function(view, element) {
        $scope.addMonthEvents(view.intervalStart.month());
      }
    }
  };

  $scope.addMonthEvents = function(month){
    api.calendar.month(month+1, true)
    .success(function(data, status, headers, config){
      var finalCalendarEvents = [];
      var calendarEvents = data.data; 
      angular.forEach(calendarEvents, function (calendar, key) {
        calendarDates = calendar.dates;
        angular.forEach(calendarDates, function (value, key) {
          date = new Date(value);
          dateEnd = new Date(date);
          date.setHours(parseInt(calendar.hourStart.split(":")[0]));
          dateEnd.setHours(parseInt(calendar.hourEnd.split(":")[0]));
          if( date.getFullYear() == y && date.getMonth() == month){
            finalCalendarEvents.push({
              id : calendar.id,
              title : calendar.title,
              start : date,
              end : dateEnd,
              allDay : calendar.allDay               
            });
          }
        });
      });

      $scope.eventSources[0] = finalCalendarEvents;
    })
    .error(function(data, status, headers, config) {
      console.log(data);
    });       
  };

  $scope.eventSources = [];
}]);