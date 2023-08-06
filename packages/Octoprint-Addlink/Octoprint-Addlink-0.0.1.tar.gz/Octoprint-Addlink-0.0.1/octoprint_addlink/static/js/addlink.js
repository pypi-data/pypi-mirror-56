/*
 * View model for Octoprint-Addlink
 *
 * Author: Carl-Fredrik Hårsmar
 * License: AGPLv3
 */
$(function() {
  function AddlinkViewModel(parameters) {
    var self = this;
    self.loginState = parameters[0];
    self.settings = parameters[1];
    self.deviceLinked = ko.observable(false);
    self.deviceConnected = ko.observable(false);
    self.appHost = ko.observable(null);
    self.linkWindow = null;
    self.linkListener = null;
    self.linkEvent = null;


    self.linkDevice = function() {
      var redirect_url = window.location.origin + window.location.pathname;
      var query = self.buildQuery({
        request_type: 'link'
      });

      if(self.linkWindow == null || self.linkWindow.closed) {
        self.linkWindow = window.open(
          self.appHost() + '/login?' + query,
          'Authorize with add:link',
          'toolbar=no, menubar=no, width=600, height=700, left= 600, top=200, centerscreen=true'
        );
        self.linkWindow.onbeforeunload = function(){
          self.linkWindow = null;
        };
      } else {
        self.linkWindow.location.href = self.appHost() + '/login?' + query;
        self.linkWindow.focus();
      }
    };

    var eventMethod = window.addEventListener ? "addEventListener" : "attachEvent";
    var messageEvent = eventMethod === "attachEvent"? "onmessage": "message";
    window[eventMethod](messageEvent, function(message) {
      try {
        if (message.origin != self.appHost()) {
          throw "Not trusted origin: " + message.origin;
        }
        
        var deviceInfo = JSON.parse(message.data);
        if(!deviceInfo['token'] || !deviceInfo['deviceId']) throw "Error getting authorization token and device id";
        self.linkWindow.close();
        self.saveLink(deviceInfo['deviceId'], deviceInfo['token']);
      } catch(e) {
        self.errorLogger(e)
      }
    });

    self.saveLink = function (deviceId, token) {
      console.log("Posting:");
      console.log({
        deviceId: deviceId, 
        deviceToken: token
      });
      $.ajax({
        type: "POST",
        contentType: "application/json; charset=utf-8",
        url: PLUGIN_BASEURL + "addlink/savelink",
        data: JSON.stringify({
          deviceId: deviceId, 
          deviceToken: token
        }),
        dataType: "json",
        error: self.errorLogger
      });
    }

    self.errorLogger = function(error) {
      console.log("Sending error: " + JSON.stringify(error));
      $.ajax({
        type: "POST",
        contentType: "application/json; charset=utf-8",
        url: PLUGIN_BASEURL + "addlink/errorlogger",
        data: JSON.stringify({error: JSON.stringify(error)}),
        dataType: "json"
      });
    }

    self.buildQuery = function(params) {
      if (typeof (params) === 'string') return encodeURIComponent(params);
      var query = [];
      for (var key in params) {
        if (params.hasOwnProperty(key)) {
          query.push(encodeURIComponent(key) + '=' + encodeURIComponent(params[key]));
        }
      }
      return query.join('&');
    }
    
    
    self.getQueryParams = function (params) {
      var pairs = params.substring(1).split("&"), obj = {}, pair, i;
      for ( i in pairs ) {
        if ( pairs[i] === "" ) continue;
        pair = pairs[i].split("=");
        obj[ decodeURIComponent( pair[0] ) ] = decodeURIComponent( pair[1] );
      }
      return obj;
    }
    
    self.onBeforeBinding = function() {
      self.deviceLinked(self.settings.settings.plugins.addlink.deviceLinked());
      self.deviceConnected(self.settings.settings.plugins.addlink.deviceConnected());
      self.appHost(self.settings.settings.plugins.addlink.appHost());
    }

    self.onDataUpdaterPluginMessage = function(plugin, messages) {
      if(plugin =="addlink") {
        for(var i in messages){
          if(self.hasOwnProperty(i)) {
            self[i](messages[i]);
          }
        }
      }
    }
  }
  
  OCTOPRINT_VIEWMODELS.push({
      construct: AddlinkViewModel,
      // ViewModels your plugin depends on, e.g. loginStateViewModel, settingsViewModel, ...
      dependencies: ["loginStateViewModel", "settingsViewModel"],
      // Elements to bind to, e.g. #settings_plugin_addlink, #tab_plugin_addlink, ...
      elements: ["#navbar_plugin_addlink","#tab_plugin_addlink"]
  });
});
