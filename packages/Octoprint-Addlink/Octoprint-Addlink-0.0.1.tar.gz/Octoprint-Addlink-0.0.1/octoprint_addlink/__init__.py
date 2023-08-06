# coding=utf-8
from __future__ import absolute_import

from flask import jsonify, request
from octoprint.server import admin_permission, VERSION

import octoprint.plugin

from tabulate import tabulate

appHost ="https://cloud.addnorth.com"
socketHost="wss://api.addnorth.com/v1"
hostSoftwareBase="Octoprint"

class AddlinkPlugin(octoprint.plugin.SettingsPlugin,
                    octoprint.plugin.AssetPlugin,
                    octoprint.plugin.TemplatePlugin,
                    octoprint.plugin.StartupPlugin,
                    octoprint.plugin.BlueprintPlugin,
                    octoprint.plugin.EventHandlerPlugin):

  def on_after_startup(self):
    self.logger("Addlink started", "info")
    self.logger("\n" + tabulate([
      ["Host software", self._settings.get(["hostSoftwareBase"])],
      ["Host software version", self._settings.get(["hostSoftwareVersion"])],
      ["Plugin version", self._plugin_version],
      ["Device ID", self._settings.get(["deviceId"])],
      ["Device linked", self._settings.get(["deviceLinked"])],
      ["Device connected", self._settings.get(["deviceConnected"])],
      ["App host", self._settings.get(["appHost"])],
      ["Socket host", self._settings.get(["socketHost"])]
    ], ["Setting", "Value"], tablefmt="psql"), "info")
  
  def logger(self, msg, level="info"):
    colors = dict(
      info = "\033[94m",
      warning = "\033[93m",
      error = "\033[91m"
    )
    func = getattr(self._logger,level)
    func(colors[level] + msg + "\033[0m")
  
  def settings_set(self, setting, value):
    self._settings.set([setting], value)
    self._settings.save()
    self._plugin_manager.send_plugin_message("addlink", {setting: value})

  def get_settings_defaults(self):
    return dict(
      appHost = appHost,
      socketHost = socketHost,
      hostSoftwareBase = hostSoftwareBase,
      hostSoftwareVersion = VERSION,
      deviceId = False,
      deviceToken = None,
      deviceLinked = False,
      deviceConnected = False
    )

  def get_template_configs(self):
    return dict(
      dict(type="navbar", custom_bindings=False)
    )

  def get_assets(self):
    return dict(
      js=["js/addlink.js"],
      css=["css/addlink.css"]
    )

  def get_update_information(self):
		return dict(
      addlink=dict(
        displayName="Addlink Plugin",
        displayVersion=self._plugin_version,
        type="github_release",
        user="hoffeman",
        repo="Octoprint-Addlink",
        current=self._plugin_version,
        pip="https://github.com/addnorth/Octoprint-Addlink/archive/{target_version}.zip"
      )
    )

  def on_event(self, event, payload):
    self.logger(str(event), "info")

  def is_blueprint_protected(self):
    return False

  @octoprint.plugin.BlueprintPlugin.route("/errorlogger", methods=["POST"])
  @admin_permission.require(403)
  def error_logger(self):
    self.logger(str(request.json['error']), "error")
    return jsonify({}), 200, {'ContentType':'application/json'}

  @octoprint.plugin.BlueprintPlugin.route("/savelink", methods=["POST"])
  @admin_permission.require(403)
  def save_link(self):
    self.settings_set('deviceToken', request.json['deviceToken'])
    self.settings_set('deviceId', request.json['deviceId'])
    self.settings_set('deviceLinked', True)
    self.logger("Device linked: " + str(request.json['deviceId']), "info")
    return jsonify({}), 200, {'ContentType':'application/json'}

def __plugin_load__():
  plugin = AddlinkPlugin()

  global __plugin_implementation__
  __plugin_implementation__ = plugin

  global __plugin_hooks__
  __plugin_hooks__ = {
    "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
  }
def __plugin_check__():
  try:
    from tabulate import tabulate
  except ImportError:
    return False
  return True

  