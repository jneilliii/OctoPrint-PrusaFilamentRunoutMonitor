/*
 * View model for Prusa Filament Runour Monitor
 *
 * Author: jneilliii
 * License: AGPLv3
 */
$(function() {
    function PrusafilamentrunoutmonitorViewModel(parameters) {
        var self = this;
        self.settingsViewModel = parameters[0];

        self.onDataUpdaterPluginMessage = function (plugin, data) {
			if (plugin !== "prusafilamentrunoutmonitor") {
				return;
			}

            if (data.filamentrunout) {
                new PNotify({
					title: 'Prusa Filament Runout',
					text: gettext('Filament runout has occurred, please replace filament and resume printing when ready.'),
                    type: 'info',
					hide: false
				});
            }
        }
    }

    OCTOPRINT_VIEWMODELS.push({
        construct: PrusafilamentrunoutmonitorViewModel,
        dependencies: ["settingsViewModel"],
        elements: ["#settings_plugin_prusafilamentrunoutmonitor"]
    });
});
