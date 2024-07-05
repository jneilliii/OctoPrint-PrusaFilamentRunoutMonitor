# coding=utf-8
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
            self._processing = False

    # ~~ GCode received hook
    def process_gcode(self, comm, line, *args, **kwargs):
        if line == "echo:busy: processing" or self._processing and self._printer.is_printing():
            if line == "echo:busy: processing":
                self._logger.debug("Enabling position monitor")
                self._processing = True
            elif self._processing:
                x_position = self._settings.get(["x_position"])
                y_position = self._settings.get(["y_position"])
                if line.startswith(f"X:{x_position} Y:{y_position}"):
                    self._logger.debug("Pausing print")
                    self._printer.pause_print()
                    self._plugin_manager.send_plugin_message(self._identifier, {'filamentrunout': True})
                    self._processing = False
                else:
                    self._logger.debug(f"unmatched: \"X:{x_position} Y:{y_position}\" to \"{line}\"")

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
        "octoprint.comm.protocol.gcode.received": __plugin_implementation__.process_gcode,
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
