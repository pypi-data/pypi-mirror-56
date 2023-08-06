#!/usr/bin/env python

import wx
import numpy as np
import nibabel as nib
import fsl.data.image as fslimage
import fsleyes.actions as actions
import fsleyes.controls.controlpanel as ctrlpanel
import fsleyes.displaycontext.labelopts as labelopts
from scipy.ndimage import label as ndlabel
from scipy.ndimage.measurements import center_of_mass


def fetch_labels(image):
    """
    Get a list of labels for a given Image

    Parameters
    ----------
    image: nibabel object
        Image to get Informations from

    Returns
    --------
    list: all labels except 0

    """

    data = image.get_data()
    labels = np.unique(data[data != 0])

    return list(labels)


def get_label_size(image, label):
    """
    Returns the size of the given label for an image


    Parameters
    ----------
    image: nibabel object
        Image with the label
    label: int or float
        label to query size of

    Returns
    --------

    [int: size in voxels, volume in mm³]

    """

    img = image.get_data()
    masked_img = np.zeros(img.shape)
    masked_img[img == label] = 1

    voxelcount = int(masked_img.sum())
    voxelvolume = np.prod(nib.affines.voxel_sizes(image.affine)) * voxelcount

    return [voxelcount, voxelvolume]


def get_position(image, label):
    """
    Returns the Center of mass for a given label

    Parameters
    ----------
    image: nibabel object

    label: int

    Returns
    -------

    tuple of coordinates (x,y, z)
    """

    img = image.get_data()
    masked_img = np.zeros(img.shape)
    masked_img[img == label] = 1
    coords = center_of_mass(masked_img)

    return coords


class RoiList(ctrlpanel.ControlPanel):
    def __init__(self, parent, overlay_list, display_ctx, frame):
        ctrlpanel.ControlPanel.__init__(self, parent, overlay_list, display_ctx, frame, name='ROI Tool')

        self.overlay_list = overlay_list
        self.display_ctx = display_ctx
        sizer = wx.BoxSizer(wx.VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        # Add TreeCtrl to display labels
        self.label_list = wx.TreeCtrl(self, wx.ID_ANY,
                                      wx.DefaultPosition,
                                      wx.DefaultSize,
                                      wx.TR_HAS_BUTTONS | wx.TR_HAS_VARIABLE_ROW_HEIGHT | wx.TR_HIDE_ROOT)
        self.label_list.AddRoot("Overlays")
        sizer.Add(self.label_list, flag=wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, proportion=1)
        sizer.Add(hsizer, 0, wx.ALIGN_BOTTOM | wx.EXPAND)
        self.btn_labelize = wx.Button(self, -1, 'Labelize')
        self.lbl_labelize = wx.StaticText(self, label='')
        hsizer.Add(self.btn_labelize, 0, wx.ALL | wx.EXPAND)
        hsizer.Add(self.lbl_labelize, 0, wx.ALL | wx.EXPAND)
        # Register Events
        self.label_list.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.__jump_to_label)
        self.label_list.Bind(wx.EVT_TREE_SEL_CHANGED, self.selection_changed)
        self.btn_labelize.Bind(wx.EVT_BUTTON, self.__labelize)

        self.update_labels()
        self.Layout()
        self.SetSizer(sizer)

        display_ctx.addListener('selectedOverlay',
                                self.name,
                                self.__overlays_changed)
        overlay_list.addListener('overlays',
                                 self.name,
                                 self.__overlays_changed)

    @staticmethod
    def defaultLayout():
        return {'location': wx.LEFT}

    @staticmethod
    def supportedViews():
        from fsleyes.views.orthopanel import OrthoPanel
        return [OrthoPanel]

    def selection_changed(self, event):
        """
        This function is called when selection in the TreeCtrl is changed. It
        reads the label of the currently selected file.
        """

        item = event.GetItem()

        try:
            overlay = self.label_list.GetItemData(item)[0]
        except Exception:
            pass
            return

        self.selected_overlay = overlay
        self.lbl_labelize.SetLabel(overlay.name)

    def update_labels(self):
        """
        Fetch all labels and update label_list.

        """
        root_item = self.label_list.GetRootItem()
        self.label_list.DeleteChildren(root_item)

        for overlay in self.overlay_list:
            display = self.display_ctx.getDisplay(overlay)

            try:
                # add a listener for each Overlay to get
                # updates when DataType is changed
                display.addListener('overlayType',
                                    self.name,
                                    self.__overlays_changed)
            except Exception:
                pass

            if display.overlayType in ["mask", "label"]:
                overlay_item = self.label_list.AppendItem(root_item,
                                                          str(overlay.name),
                                                          data=[overlay]
                                                          )
                labels = fetch_labels(overlay.nibImage)

                # get lookuptable for this overlay
                opts = self.display_ctx.getOpts(overlay)
                try:
                    if display.overlayType == 'label':
                        opts.addListener('lut',
                                         self.name,
                                         self.__overlays_changed
                                         )
                    if display.overlayType == 'mask':
                        opts.addListener('colour',
                                         self.name,
                                         self.__overlays_changed
                                         )
                except Exception:
                    pass
                for label in labels:
                    # now calculate volume for each label:
                    volume = get_label_size(overlay.nibImage, label)

                    # Add colours for all labels

                    col = (1, 1, 1, 1)
                    name = ''
                    if display.overlayType == 'mask':
                        col = opts.colour
                    if display.overlayType == 'label':
                        try:
                            col = opts.lut.get(label).colour
                            name = opts.lut.get(label).name
                            name = '' if name == str(label) else name + " | "
                        except Exception:
                            pass
                    itm = self.label_list.AppendItem(overlay_item,
                                                     "%i | %s %fmm³ " % (label, name, volume[1]),
                                                     data=[overlay, label]
                                                     )
                    self.label_list.SetItemBackgroundColour(itm,
                                                            wx.Colour(tuple(np.array(np.array(col) * 255).astype(int)))
                                                            )
        self.label_list.Refresh()
        self.Layout()

    def __overlays_changed(self, *a):
        """
            Called when the :class:`.OverlayList` changes.

        """

        self.update_labels()

    def __jump_to_label(self, e):
        """
            Called by event
        """

        selection = self.label_list.GetFocusedItem()
        data = self.label_list.GetItemData(selection)
        if type(data) is list and len(data) == 2:
            pos = get_position(data[0].nibImage, data[1])
            opts = self.display_ctx.getOpts(data[0])
            xform = opts.transformCoords(pos, 'id', 'display')
            self.display_ctx.location = xform

    def __labelize(self, e):
        """
        Create labels from selected overlay
        """

        selection = self.label_list.GetFocusedItem()
        data = self.label_list.GetItemData(selection)

        # Read original image and create a new overlay
        orig_image = data[0].nibImage
        labeled_image = ndlabel(orig_image.get_data())[0]
        img = nib.Nifti2Image(labeled_image, orig_image.affine)
        fslimg = fslimage.Image(img, name='%s Labeled' % data[0].name)
        self.overlay_list.append(fslimg, overlayType='label')


class PluginTool(actions.Action):
    def __init__(self, overlayList, displayCtx, frame):
        actions.Action.__init__(self, overlayList, displayCtx, self.run)

    def run(self):
        print('Running plugin tool')
