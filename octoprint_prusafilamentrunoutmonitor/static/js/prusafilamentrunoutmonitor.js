/*
 * View model for Prusa Filament Runour Monitor
 *
 * Author: jneilliii
 * License: AGPLv3
 */
$(function () {
    function PrusafilamentrunoutmonitorViewModel(parameters) {
        var self = this;
        self.settingsViewModel = parameters[0];
        self.popup = undefined;

        self.add_position = function() {
            const x_position = $("#pfrm_x_position input").val();
            const y_position = $("#pfrm_y_position input").val();
            const x_index = self.settingsViewModel.settings.plugins.prusafilamentrunoutmonitor.x_positions.indexOf(x_position);
            const y_index = self.settingsViewModel.settings.plugins.prusafilamentrunoutmonitor.y_positions.indexOf(y_position);
            if (x_position !== "" && y_position !== "") {
                // make sure position isn't already entered.
                if ((x_index !== y_index) || (x_index + y_index === -2)) {
                    self.settingsViewModel.settings.plugins.prusafilamentrunoutmonitor.x_positions.push(x_position);
                    self.settingsViewModel.settings.plugins.prusafilamentrunoutmonitor.y_positions.push(y_position);
                }
                $("#pfrm_x_position input, #pfrm_y_position input").val("");
                $("#pfrm_x_position, #pfrm_y_position").removeClass("error");
            } else {
                if (x_position === "") {
                    $("#pfrm_x_position").addClass("error");
                }
                if (y_position === "") {
                    $("#pfrm_y_position").addClass("error");
                }
            }
        };

        self.remove_position = function(idx) {
            self.settingsViewModel.settings.plugins.prusafilamentrunoutmonitor.x_positions.splice(idx, 1);
            self.settingsViewModel.settings.plugins.prusafilamentrunoutmonitor.y_positions.splice(idx, 1);
        };

        self.onDataUpdaterPluginMessage = function (plugin, data) {
            if (plugin !== "prusafilamentrunoutmonitor") {
                return;
            }

            if (data.filamentrunout) {
                self.popup = new PNotify({
                    title: 'Prusa Filament Runout',
                    text: gettext('Filament runout has occurred, please replace filament and resume printing when ready.'),
                    type: 'info',
                    hide: false
                });
            } else {
                if (typeof self.popup !== "undefined") {
                    self.popup.remove();
                    self.popup = undefined;
                }
            }
        };
    }

    OCTOPRINT_VIEWMODELS.push({
        construct: PrusafilamentrunoutmonitorViewModel,
        dependencies: ["settingsViewModel"],
        elements: ["#settings_plugin_prusafilamentrunoutmonitor"]
    });
});
