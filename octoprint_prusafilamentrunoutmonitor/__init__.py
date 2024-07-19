# coding=utf-8
import time

import octoprint.plugin
from octoprint.events import Events

class PrusafilamentrunoutmonitorPlugin(octoprint.plugin.SettingsPlugin,
    octoprint.plugin.AssetPlugin,
    octoprint.plugin.TemplatePlugin,
    octoprint.plugin.EventHandlerPlugin
):
    def __init__(self):
        super().__init__()
        self._processing = False

    # ~~ SettingsPlugin mixin

    def get_settings_defaults(self):
        return {
            "x_position": "241.00",
            "y_position": "-3.00"
        }

    # ~~ AssetPlugin mixin

    def get_assets(self):
        return {
            "js": ["js/prusafilamentrunoutmonitor.js"]
        }

    # ~~ TemplatePlugin mixin

    def get_template_vars(self):
        return {"plugin_version": self._plugin_version}

    # ~~ Event Handler Plugin

    def on_event(self, event, payload):
        if event in [Events.PRINT_STARTED, Events.PRINT_DONE, Events.PRINT_CANCELLED, Events.PRINT_RESUMED]:
            self._plugin_manager.send_plugin_message(self._identifier, {'filamentrunout': False})
            self._processing = False

    # ~~ GCode received hook
    def process_gcode(self, comm, line, *args, **kwargs):
        # handle starting position monitoring
        if line.strip() == "echo:busy: processing" and self._printer.is_printing() and not self._processing:
            self._logger.debug("Enabling position monitor")
            self._processing = True
        # handle stopping position monitoring
        elif self._processing and line.strip() == "ok":
            self._logger.debug("Received ok while monitoring, disabling position monitor.")
            self._processing = False
            self._plugin_manager.send_plugin_message(self._identifier, {'filamentrunout': False})
        # check for position report match
        elif self._processing and line.strip().startswith(f"X:{self._settings.get(['x_position'])} Y:{self._settings.get(['y_position'])}"):
            self._logger.debug("Parked position matched")

            fileposition = comm.getFilePosition() if comm else None
            progress = comm.getPrintProgress() if comm else None
            job_data = self._printer.get_current_job()

            payload = job_data.get("file")
            payload["owner"] = ""
            payload["user"] = job_data.get("user")
            payload["fileposition"] = fileposition
            payload["progress"] = progress
            self._logger.debug("Firing pause on event bus.")
            self._event_bus.fire(Events.PRINT_PAUSED, payload)

            self._plugin_manager.send_plugin_message(self._identifier, {'filamentrunout': True})
            self._processing = False

        return line

    # ~~ Softwareupdate hook

    def get_update_information(self):
        return {
            "prusafilamentrunoutmonitor": {
                "displayName": "Prusa Filament Runout",
                "displayVersion": self._plugin_version,

                # version check: github repository
                "type": "github_release",
                "user": "jneilliii",
                "repo": "OctoPrint-PrusaFilamentRunoutMonitor",
                "current": self._plugin_version,

                # update method: pip
                "pip": "https://github.com/jneilliii/OctoPrint-PrusaFilamentRunoutMonitor/archive/{target_version}.zip",
            }
        }


__plugin_name__ = "Prusa Filament Runout"
__plugin_pythoncompat__ = ">=3,<4"  # Only Python 3

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = PrusafilamentrunoutmonitorPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.comm.protocol.gcode.received": (__plugin_implementation__.process_gcode, 1),
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
