# This file is generated by wxPython's SIP generator.  Do not edit by hand.
#
# Copyright: (c) 2018 by Total Control Software
# License:   wxWindows License

"""
This module contains a widget class and supporting classes for a generic HTML
renderer.  It supports only a subset of the HTML standards, and no Javascript
or CSS, but it is relatively lightweight and has no platform dependencies.  It
is suitable for displaying simple HTML documents, such as the application's
documentation or built-in help pages.

.. note:: Due to some internal dynamic initialization in wxWidgets, this
          module should be imported **before** the :class:`wx.App` object is
          created.
"""

from ._html import *

import wx

EVT_HTML_CELL_CLICKED = wx.PyEventBinder( wxEVT_HTML_CELL_CLICKED, 1 )
EVT_HTML_CELL_HOVER   = wx.PyEventBinder( wxEVT_HTML_CELL_HOVER, 1 )
EVT_HTML_LINK_CLICKED = wx.PyEventBinder( wxEVT_HTML_LINK_CLICKED, 1 )

# deprecated wxEVT aliases
wxEVT_COMMAND_HTML_CELL_CLICKED  = wxEVT_HTML_CELL_CLICKED
wxEVT_COMMAND_HTML_CELL_HOVER    = wxEVT_HTML_CELL_HOVER
wxEVT_COMMAND_HTML_LINK_CLICKED  = wxEVT_HTML_LINK_CLICKED

def _HtmlBookRecArray___repr__(self):
    return "HtmlBookRecArray: " + repr(list(self))
HtmlBookRecArray.__repr__ = _HtmlBookRecArray___repr__
del _HtmlBookRecArray___repr__
def _HtmlHelpDataItems___repr__(self):
    return "HtmlHelpDataItems: " + repr(list(self))
HtmlHelpDataItems.__repr__ = _HtmlHelpDataItems___repr__
del _HtmlHelpDataItems___repr__
