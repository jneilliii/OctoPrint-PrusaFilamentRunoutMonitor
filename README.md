# Prusa Filament Runout Monitor

**This plugin exists thanks to generous funding by [Kaizen Smart Data Ltd.](https://kaizensmartdata.com/)**

Plugin monitors Prusa Buddy firmware's (MK4, Mini, XL, MK3.9) serial communications for specific conditions that indicate
a filament runout on the printer and fires a pause on the event bus of OctoPrint.

It was programmed to work with OctoText to send an alert to the user, typically an SMS or email, that the printer is
paused waiting for a filament change; however, it will work with any plugin that reacts to the pause event in OctoPrint.

![popup screenshot](screenshot_popup.png)

**NOTE:** If Prusa updates their Buddy firmware to work correctly with Octoprint, this plugin will no longer be needed.

## Settings

Configure the X and Y position for the parked position during filament runout in the plugin's settings. To determine what
the exact position is start a sacrificial print and cut the filament while looking at the terminal tab of
OctoPrint. You should see something reported from the printer like this:
```
echo:busy: processing
X:241.00 Y:-3.00 Z:38.90 E:89.28 Count X:24099 Y:-300 Z:15559
```
Use the values for X and Y as they appear in the second line of the above example, ie. `241.00` for X and `-3.00` for Y,
in the plugin's settings. This is how the plugin determines if the printer is in the parked position during filament
runout.

![settings screenshot](screenshot_settings.png)

## Get Help

If you experience issues with this plugin or need assistance please use the issue tracker by clicking issues above.

### Additional Plugins

Check out my other plugins [here](https://plugins.octoprint.org/by_author/#jneilliii)

### Sponsors
- Andreas Lindermayr
- [@TheTuxKeeper](https://github.com/thetuxkeeper)
- [@tideline3d](https://github.com/tideline3d/)
- [SimplyPrint](https://simplyprint.io/)
- [Andrew Beeman](https://github.com/Kiendeleo)
- [Calanish](https://github.com/calanish)
- [Lachlan Bell](https://lachy.io/)
- [Jonny Bergdahl](https://github.com/bergdahl)
## Support My Efforts
I, jneilliii, programmed this plugin for fun and do my best effort to support those that have issues with it, please return the favor and leave me a tip or become a Patron if you find this plugin helpful and want me to continue future development.

[![Patreon](patreon-with-text-new.png)](https://www.patreon.com/jneilliii) [![paypal](paypal-with-text.png)](https://paypal.me/jneilliii) [![GitHub](github.png)](https://github.com/sponsors/jneilliii)

<small>No paypal.me? Send funds via PayPal to jneilliii&#64;gmail&#46;com</small>
