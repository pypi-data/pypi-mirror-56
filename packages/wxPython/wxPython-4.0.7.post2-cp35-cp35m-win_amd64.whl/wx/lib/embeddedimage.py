#----------------------------------------------------------------------
# Name:        wx.lib.embeddedimage
# Purpose:     Defines a class used for embedding PNG images in Python
#              code. The primary method of using this module is via
#              the code generator in wx.tools.img2py.
#
# Author:      Anthony Tuininga
#
# Created:     26-Nov-2007
# Copyright:   (c) 2007 by Anthony Tuininga
# Licence:     wxWindows license
# Tags:        phoenix-port
#----------------------------------------------------------------------

import base64

import wx
from six import BytesIO

try:
    b64decode = base64.b64decode
except AttributeError:
    b64decode = base64.decodestring


class PyEmbeddedImage(object):
    """
    PyEmbeddedImage is primarily intended to be used by code generated
    by img2py as a means of embedding image data in a python module so
    the image can be used at runtime without needing to access the
    image from an image file.  This makes distributing icons and such
    that an application uses simpler since tools like py2exe will
    automatically bundle modules that are imported, and the
    application doesn't have to worry about how to locate the image
    files on the user's filesystem.

    The class can also be used for image data that may be acquired
    from some other source at runtime, such as over the network or
    from a database.  In this case pass False for isBase64 (unless the
    data actually is base64 encoded.)  Any image type that
    wx.Image can handle should be okay.
    """

    def __init__(self, data, isBase64=True):
        self.data = data
        self.isBase64 = isBase64

    def GetBitmap(self):
        return wx.Bitmap(self.GetImage())

    def GetData(self):
        data = self.data
        if self.isBase64:
            data = b64decode(self.data)
        return data

    def GetIcon(self):
        icon = wx.Icon()
        icon.CopyFromBitmap(self.GetBitmap())
        return icon

    def GetImage(self):
        stream = BytesIO(self.GetData())
        return wx.Image(stream)

    # added for backwards compatibility
    getBitmap = wx.deprecated(GetBitmap)
    getData = wx.deprecated(GetData)
    getIcon = wx.deprecated(GetIcon)
    getImage = wx.deprecated(GetImage)

    # define properties, for convenience
    Bitmap = property(GetBitmap)
    Data = property(GetData)
    Icon = property(GetIcon)
    Image = property(GetImage)
