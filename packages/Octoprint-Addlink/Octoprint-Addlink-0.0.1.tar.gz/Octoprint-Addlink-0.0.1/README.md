# Octoprint-Addlink

Plugin to hook up your existing Octoprint device with add:link.

## Prerequisites

1. OctoPrint 1.3.12 (not tested on older versions)
2. add:link account (create one for free at [add:link](https://cloud.addnorth.com))
3. Internet connection
 Optional: Raspberry Pi Camera for streaming

## Setup

**1.** Install via the bundled [Plugin Manager](https://github.com/foosel/OctoPrint/wiki/Plugin:-Plugin-Manager)
or manually using this URL:

    https://github.com/hoffeman/Octoprint-Addlink/archive/master.zip

**2.** After plugin is installed, go to:

    Settings -> API and enable CORS

**3.** Restart OctoPrint

**4.** After OctoPrint has restarted go to the Dashboard and you will find a new tab called "OctoPrint-Addlink":

    Click the button "Link to account" and follow the instructions.

**5.** If successful the icon in the top navbar is now green and you are ready to go!

**6.** Now you can go to [add:link](https://cloud.addnorth.com) and manage your printer!

## Optimization

OctoPrint runs several features and plugins that are not needed for add:link to function and can be disabled to improve performance.

### Standard configuration
This is the default case.

To optimize performance go to the Dashboard -> OctoPrint-Addlink Tab and then press the "Optimize Octoprint" button

### Custom config.yaml
Follow these steps if you are using a custom config.yaml.

Insert the following in your config.yaml to disable unnecessary plugins.

    plugins:
      asd:
