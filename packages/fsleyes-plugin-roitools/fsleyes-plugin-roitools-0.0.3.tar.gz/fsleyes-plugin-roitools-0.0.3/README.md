# fsleyes-plugin-roitool

A plugin which provides a easy way to find rois from Masks/Label-Images and get a fast information

## Usage

To pen the Plugin go to Settings->Ortho View->RoiTools. 

* all Overlays which are marked as ` mask image` or ` Label image` are listed in the Roi-Tools-Widget.
* You can drop down all Overlays to see the containing labels of each overlay
* DoubleClick on any label to jump to the center of mass of the label.

## Issues

* needs to inspect only changed overlays. Currently it might get verry cpu-consuming because every change on any overlay forces
  the plugin to reread all overlays of map or label-type

## TODO
	
	* Mean/Std of each label in all overlays

