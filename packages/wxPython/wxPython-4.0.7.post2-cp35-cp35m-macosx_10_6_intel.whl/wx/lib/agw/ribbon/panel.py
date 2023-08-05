# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Name:         panel.py
# Purpose:
#
# Author:       Andrea Gavana <andrea.gavana@gmail.com>
#
# Created:
# Version:
# Date:
# Licence:      wxWindows license
# Tags:         phoenix-port, unittest, documented, py3-port
#----------------------------------------------------------------------------
"""
Serves as a container for a group of (ribbon) controls.


Description
===========

A :class:`RibbonPanel` will typically have panels for children, with the controls for that
page placed on the panels. A panel adds a border and label to a group of controls,
and can be minimised (either automatically to conserve space, or manually by the user).


Window Styles
=============

This class supports the following window styles:

================================= =========== =================================
Window Styles                     Hex Value   Description
================================= =========== =================================
``RIBBON_PANEL_DEFAULT_STYLE``            0x0 Defined as no other flags set.
``RIBBON_PANEL_NO_AUTO_MINIMISE``         0x1 Prevents the panel from automatically minimising to conserve screen space.
``RIBBON_PANEL_EXT_BUTTON``               0x8 Causes an extension button to be shown in the panel's chrome (if the bar in which it is contained has ``RIBBON_BAR_SHOW_PANEL_EXT_BUTTONS`` set). The behaviour of this button is application controlled, but typically will show an extended drop-down menu relating to the panel.
``RIBBON_PANEL_MINIMISE_BUTTON``         0x10 Causes a (de)minimise button to be shown in the panel's chrome (if the bar in which it is contained has the ``RIBBON_BAR_SHOW_PANEL_MINIMISE_BUTTONS`` style set). This flag is typically combined with ``RIBBON_PANEL_NO_AUTO_MINIMISE`` to make a panel which the user always has manual control over when it minimises.
``RIBBON_PANEL_STRETCH``                 0x20 Allows a single panel to stretch to fill the parent page.
``RIBBON_PANEL_FLEXIBLE``                0x40 Allows toolbars to wrap, taking up the optimum amount of space when used in a vertical palette.
================================= =========== =================================


Events Processing
=================

This class processes the following events:

======================================= ===================================
Event Name                              Description
======================================= ===================================
``EVT_RIBBONPANEL_EXTBUTTON_ACTIVATED`` Triggered when the user activate the panel extension button.
======================================= ===================================

See Also
========

:class:`~wx.lib.agw.ribbon.page.RibbonPage`

"""

import wx

from .control import RibbonControl

from .art import *


wxEVT_COMMAND_RIBBONPANEL_EXTBUTTON_ACTIVATED = wx.NewEventType()
EVT_RIBBONPANEL_EXTBUTTON_ACTIVATED = wx.PyEventBinder(wxEVT_COMMAND_RIBBONPANEL_EXTBUTTON_ACTIVATED, 1)


def IsAncestorOf(ancestor, window):

    while window is not None:
        parent = window.GetParent()
        if parent == ancestor:
            return True
        else:
            window = parent

    return False


class RibbonPanelEvent(wx.PyCommandEvent):
    """ Handles events related to :class:`RibbonPanel`. """

    def __init__(self, command_type=None, win_id=0, panel=None):
        """
        Default class constructor.

        :param integer `command_type`: the event type;
        :param integer `win_id`: the event identifier;
        :param `panel`: an instance of :class:`RibbonPanel`;
        """

        wx.PyCommandEvent.__init__(self, command_type, win_id)

        self._panel = panel


    def GetPanel(self):
        """ Returns the panel which the event relates to. """

        return self._panel


    def SetPanel(self, panel):
        """
        Sets the panel relating to this event.

        :param `panel`: an instance of :class:`RibbonPanel`.
        """

        self._panel = panel


class RibbonPanel(RibbonControl):
    """ This is the main implementation of :class:`RibbonPanel`. """

    def __init__(self, parent, id=wx.ID_ANY, label="", minimised_icon=wx.NullBitmap,
                 pos=wx.DefaultPosition, size=wx.DefaultSize, agwStyle=RIBBON_PANEL_DEFAULT_STYLE,
                 name="RibbonPanel"):
        """
        Default class constructor.

        :param `parent`: pointer to a parent window, typically a :class:`~wx.lib.agw.ribbon.page.RibbonPage`, though
         it can be any window;
        :param `id`: window identifier. If ``wx.ID_ANY``, will automatically create
         an identifier;
        :param `label`: label of the new button;
        :param `minimised_icon`: the bitmap to be used in place of the panel children
         when it is minimised;
        :param `pos`: window position. ``wx.DefaultPosition`` indicates that wxPython
         should generate a default position for the window;
        :param `size`: window size. ``wx.DefaultSize`` indicates that wxPython should
         generate a default size for the window. If no suitable size can be found, the
         window will be sized to 20x20 pixels so that the window is visible but obviously
         not correctly sized;
        :param `agwStyle`: the AGW-specific window style. This can be one of the following
         bits:

         ================================= =========== =================================
         Window Styles                     Hex Value   Description
         ================================= =========== =================================
         ``RIBBON_PANEL_DEFAULT_STYLE``            0x0 Defined as no other flags set.
         ``RIBBON_PANEL_NO_AUTO_MINIMISE``         0x1 Prevents the panel from automatically minimising to conserve screen space.
         ``RIBBON_PANEL_EXT_BUTTON``               0x8 Causes an extension button to be shown in the panel's chrome (if the bar in which it is contained has ``RIBBON_BAR_SHOW_PANEL_EXT_BUTTONS`` set). The behaviour of this button is application controlled, but typically will show an extended drop-down menu relating to the panel.
         ``RIBBON_PANEL_MINIMISE_BUTTON``         0x10 Causes a (de)minimise button to be shown in the panel's chrome (if the bar in which it is contained has the ``RIBBON_BAR_SHOW_PANEL_MINIMISE_BUTTONS`` style set). This flag is typically combined with ``RIBBON_PANEL_NO_AUTO_MINIMISE`` to make a panel which the user always has manual control over when it minimises.
         ``RIBBON_PANEL_STRETCH``                 0x20 Allows a single panel to stretch to fill the parent page.
         ``RIBBON_PANEL_FLEXIBLE``                0x40 Allows toolbars to wrap, taking up the optimum amount of space when used in a vertical palette.
         ================================= =========== =================================

        :param `name`: the window name.
        """

        RibbonControl.__init__(self, parent, id, pos, size, wx.BORDER_NONE, name=name)
        self.CommonInit(label, minimised_icon, agwStyle)

        self.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseClick)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_MOTION, self.OnMotion)


    def __del__(self):

        if self._expanded_panel:
            self._expanded_panel._expanded_dummy = None
            self._expanded_panel.GetParent().Destroy()


    def IsExtButtonHovered(self):

        return self._ext_button_hovered


    def SetArtProvider(self, art):
        """
        Set the art provider to be used.

        Normally called automatically by :class:`~wx.lib.agw.ribbon.page.RibbonPage` when the panel is created, or the
        art provider changed on the page. The new art provider will be propagated to the
        children of the panel.

        Reimplemented from :class:`~wx.lib.agw.ribbon.control.RibbonControl`.

        :param `art`: an art provider.

        """

        self._art = art
        for child in self.GetChildren():
            if isinstance(child, RibbonControl):
                child.SetArtProvider(art)

        if self._expanded_panel:
            self._expanded_panel.SetArtProvider(art)


    def CommonInit(self, label, icon, agwStyle):

        self.SetName(label)
        self.SetLabel(label)

        self._minimised_size = wx.Size(-1, -1) # Unknown / none
        self._smallest_unminimised_size = wx.Size(-1, -1) # Unknown / none
        self._preferred_expand_direction = wx.SOUTH
        self._expanded_dummy = None
        self._expanded_panel = None
        self._flags = agwStyle
        self._minimised_icon = icon
        self._minimised = False
        self._hovered = False
        self._ext_button_hovered = False
        self._ext_button_rect = wx.Rect()

        if self._art == None:
            parent = self.GetParent()
            if isinstance(parent, RibbonControl):
                self._art = parent.GetArtProvider()

        self.SetAutoLayout(True)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.SetMinSize(wx.Size(20, 20))


    def IsMinimised(self, at_size=None):
        """
        Query if the panel would be minimised at a given size.

        :param `at_size`: an instance of :class:`wx.Size`, giving the size at which the
         panel should be tested for minimisation.
        """

        if at_size is None:
            return self.IsMinimised1()

        return self.IsMinimised2(wx.Size(*at_size))


    def IsMinimised1(self):
        """ Query if the panel is currently minimised. """

        return self._minimised


    def IsHovered(self):
        """
        Query is the mouse is currently hovered over the panel.

        :returns: ``True`` if the cursor is within the bounds of the panel (i.e.
         hovered over the panel or one of its children), ``False`` otherwise.
        """

        return self._hovered


    def OnMouseEnter(self, event):
        """
        Handles the ``wx.EVT_ENTER_WINDOW`` event for :class:`RibbonPanel`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        self.TestPositionForHover(event.GetPosition())


    def OnMouseEnterChild(self, event):
        """
        Handles the ``wx.EVT_ENTER_WINDOW`` event for children of :class:`RibbonPanel`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        pos = event.GetPosition()
        child = event.GetEventObject()

        if child:
            pos += child.GetPosition()
            self.TestPositionForHover(pos)

        event.Skip()


    def OnMouseLeave(self, event):
        """
        Handles the ``wx.EVT_LEAVE_WINDOW`` event for :class:`RibbonPanel`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        self.TestPositionForHover(event.GetPosition())


    def OnMouseLeaveChild(self, event):
        """
        Handles the ``wx.EVT_LEAVE_WINDOW`` event for children of :class:`RibbonPanel`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        pos = event.GetPosition()
        child = event.GetEventObject()

        if child:
            pos += child.GetPosition()
            self.TestPositionForHover(pos)

        event.Skip()


    def TestPositionForHover(self, pos):

        hovered = ext_button_hovered = False

        if pos.x >= 0 and pos.y >= 0:
            size = self.GetSize()
            if pos.x < size.GetWidth() and pos.y < size.GetHeight():
                hovered = True

        if hovered:
            if self.HasExtButton():
                ext_button_hovered = self._ext_button_rect.Contains(pos)

        if hovered != self._hovered or ext_button_hovered != self._ext_button_hovered:
            self._hovered = hovered
            self._ext_button_hovered = ext_button_hovered
            self.Refresh(False)


    def HasExtButton(self):

        bar = self.GetGrandParent()
        return (self._flags & RIBBON_PANEL_EXT_BUTTON) and (bar.GetAGWWindowStyleFlag() & RIBBON_BAR_SHOW_PANEL_EXT_BUTTONS)


    def AddChild(self, child):

        RibbonControl.AddChild(self, child)

        # Window enter / leave events count for only the window in question, not
        # for children of the window. The panel wants to be in the hovered state
        # whenever the mouse cursor is within its boundary, so the events need to
        # be attached to children too.
        child.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnterChild)
        child.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeaveChild)


    def RemoveChild(self, child):

        child.Unbind(wx.EVT_ENTER_WINDOW)
        child.Unbind(wx.EVT_LEAVE_WINDOW)

        RibbonControl.RemoveChild(self, child)


    def OnMotion(self, event):
        """
        Handles the ``wx.EVT_MOTION`` event for :class:`RibbonPanel`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        self.TestPositionForHover(event.GetPosition())


    def OnSize(self, event):
        """
        Handles the ``wx.EVT_SIZE`` event for :class:`RibbonPanel`.

        :param `event`: a :class:`wx.SizeEvent` event to be processed.
        """

        if self.GetAutoLayout():
            self.Layout()

        event.Skip()


    def DoSetSize(self, x, y, width, height, sizeFlags=wx.SIZE_AUTO):
        """
        Sets the size of the window in pixels.

        :param integer `x`: required `x` position in pixels, or ``wx.DefaultCoord`` to
         indicate that the existing value should be used;
        :param integer `y`: required `y` position in pixels, or ``wx.DefaultCoord`` to
         indicate that the existing value should be used;
        :param integer `width`: required width in pixels, or ``wx.DefaultCoord`` to
         indicate that the existing value should be used;
        :param integer `height`: required height in pixels, or ``wx.DefaultCoord`` to
         indicate that the existing value should be used;
        :param integer `sizeFlags`: indicates the interpretation of other parameters.
         It is a bit list of the following:

         * ``wx.SIZE_AUTO_WIDTH``: a ``wx.DefaultCoord`` width value is taken to indicate a
           wxPython-supplied default width.
         * ``wx.SIZE_AUTO_HEIGHT``: a ``wx.DefaultCoord`` height value is taken to indicate a
           wxPython-supplied default height.
         * ``wx.SIZE_AUTO``: ``wx.DefaultCoord`` size values are taken to indicate a wxPython-supplied
           default size.
         * ``wx.SIZE_USE_EXISTING``: existing dimensions should be used if ``wx.DefaultCoord`` values are supplied.
         * ``wx.SIZE_ALLOW_MINUS_ONE``: allow negative dimensions (i.e. value of ``wx.DefaultCoord``)
           to be interpreted as real dimensions, not default values.
         * ``wx.SIZE_FORCE``: normally, if the position and the size of the window are already
           the same as the parameters of this function, nothing is done. but with this flag a window
           resize may be forced even in this case (supported in wx 2.6.2 and later and only implemented
           for MSW and ignored elsewhere currently).
        """

        # At least on MSW, changing the size of a window will cause GetSize() to
        # report the new size, but a size event may not be handled immediately.
        # If self minimised check was performed in the OnSize handler, then
        # GetSize() could return a size much larger than the minimised size while
        # IsMinimised() returns True. This would then affect layout, as the panel
        # will refuse to grow any larger while in limbo between minimised and non.

        minimised = (self._flags & RIBBON_PANEL_NO_AUTO_MINIMISE) == 0 and self.IsMinimised(wx.Size(width, height))

        if minimised != self._minimised:
            self._minimised = minimised

            for child in self.GetChildren():
                child.Show(not minimised)

            self.Refresh()

        RibbonControl.DoSetSize(self, x, y, width, height, sizeFlags)


    def IsMinimised2(self, at_size):
        """
        Query if the panel would be minimised at a given size.

        :param `at_size`: an instance of :class:`wx.Size`, giving the size at which the
         panel should be tested for minimisation.
        """

        if self.GetSizer():
            # we have no information on size change direction
            # so check both
            size = self.GetMinNotMinimisedSize()
            if size.x > at_size.x or size.y > at_size.y:
                return True

            return False

        if not self._minimised_size.IsFullySpecified():
            return False

        return (at_size.x <= self._minimised_size.x and \
                at_size.y <= self._minimised_size.y) or \
                at_size.x < self._smallest_unminimised_size.x or \
                at_size.y < self._smallest_unminimised_size.y


    def OnEraseBackground(self, event):
        """
        Handles the ``wx.EVT_ERASE_BACKGROUND`` event for :class:`RibbonPanel`.

        :param `event`: a :class:`EraseEvent` event to be processed.
        """

        # All painting done in main paint handler to minimise flicker
        pass


    def OnPaint(self, event):
        """
        Handles the ``wx.EVT_PAINT`` event for :class:`RibbonPanel`.

        :param `event`: a :class:`PaintEvent` event to be processed.
        """

        dc = wx.AutoBufferedPaintDC(self)

        if self._art != None:
            if self.IsMinimised():
                self._art.DrawMinimisedPanel(dc, self, wx.Rect(0, 0, *self.GetSize()), self._minimised_icon_resized)
            else:
                self._art.DrawPanelBackground(dc, self, wx.Rect(0, 0, *self.GetSize()))


    def IsSizingContinuous(self):
        """
        Returns ``True`` if this window can take any size (greater than its minimum size),
        ``False`` if it can only take certain sizes.

        :see: :meth:`RibbonControl.GetNextSmallerSize() <lib.agw.ribbon.control.RibbonControl.GetNextSmallerSize>`,
         :meth:`RibbonControl.GetNextLargerSize() <lib.agw.ribbon.control.RibbonControl.GetNextLargerSize>`
        """

        # A panel never sizes continuously, even if all of its children can,
        # as it would appear out of place along side non-continuous panels.

        # JS 2012-03-09: introducing wxRIBBON_PANEL_STRETCH to allow
        # the panel to fill its parent page. For example we might have
        # a list of styles in one of the pages, which should stretch to
        # fill available space.
        return self._flags & RIBBON_PANEL_STRETCH


    def GetBestSizeForParentSize(self, parentSize):
        """ Finds the best width and height given the parent's width and height. """

        if len(self.GetChildren()) == 1:
            win = self.GetChildren()[0]

            if isinstance(win, RibbonControl):
                temp_dc = wx.ClientDC(self)
                childSize = win.GetBestSizeForParentSize(parentSize)
                clientParentSize = self._art.GetPanelClientSize(temp_dc, self, wx.Size(*parentSize), None)
                overallSize = self._art.GetPanelSize(temp_dc, self, wx.Size(*clientParentSize), None)
                return overallSize

        return self.GetSize()


    def DoGetNextSmallerSize(self, direction, relative_to):
        """
        Implementation of :meth:`RibbonControl.GetNextSmallerSize() <lib.agw.ribbon.control.RibbonControl.GetNextSmallerSize>`.

        Controls which have non-continuous sizing must override this virtual function
        rather than :meth:`RibbonControl.GetNextSmallerSize() <lib.agw.ribbon.control.RibbonControl.GetNextSmallerSize>`.
        """

        if self._expanded_panel != None:
            # Next size depends upon children, who are currently in the
            # expanded panel
            return self._expanded_panel.DoGetNextSmallerSize(direction, relative_to)

        if self._art is not None:

            dc = wx.ClientDC(self)
            child_relative, dummy = self._art.GetPanelClientSize(dc, self, wx.Size(*relative_to), None)
            smaller = wx.Size(-1, -1)
            minimise = False

            if self.GetSizer():

                # Get smallest non minimised size
                smaller = self.GetMinSize()

                # and adjust to child_relative for parent page
                if self._art.GetFlags() & RIBBON_BAR_FLOW_VERTICAL:
                     minimise = child_relative.y <= smaller.y
                     if smaller.x < child_relative.x:
                        smaller.x = child_relative.x
                else:
                    minimise = child_relative.x <= smaller.x
                    if smaller.y < child_relative.y:
                        smaller.y = child_relative.y

            elif len(self.GetChildren()) == 1:

                # Simple (and common) case of single ribbon child or Sizer
                ribbon_child = self.GetChildren()[0]
                if isinstance(ribbon_child, RibbonControl):
                    smaller = ribbon_child.GetNextSmallerSize(direction, child_relative)
                    minimise = smaller == child_relative

            if minimise:
                if self.CanAutoMinimise():
                    minimised = wx.Size(*self._minimised_size)

                    if direction == wx.HORIZONTAL:
                        minimised.SetHeight(relative_to.GetHeight())
                    elif direction == wx.VERTICAL:
                        minimised.SetWidth(relative_to.GetWidth())

                    return minimised

                else:
                    return relative_to

            elif smaller.IsFullySpecified(): # Use fallback if !(sizer/child = 1)
                return self._art.GetPanelSize(dc, self, wx.Size(*smaller), None)

        # Fallback: Decrease by 20% (or minimum size, whichever larger)
        current = wx.Size(*relative_to)
        minimum = wx.Size(*self.GetMinSize())

        if direction & wx.HORIZONTAL:
            current.x = (current.x * 4) / 5
            if current.x < minimum.x:
                current.x = minimum.x

        if direction & wx.VERTICAL:
            current.y = (current.y * 4) / 5
            if current.y < minimum.y:
                current.y = minimum.y

        return current


    def DoGetNextLargerSize(self, direction, relative_to):
        """
        Implementation of :meth:`RibbonControl.GetNextLargerSize() <lib.agw.ribbon.control.RibbonControl.GetNextLargerSize>`.

        Controls which have non-continuous sizing must override this virtual function
        rather than :meth:`RibbonControl.GetNextLargerSize() <lib.agw.ribbon.control.RibbonControl.GetNextLargerSize>`.
        """

        if self._expanded_panel != None:
            # Next size depends upon children, who are currently in the
            # expanded panel
            return self._expanded_panel.DoGetNextLargerSize(direction, relative_to)

        if self.IsMinimised(relative_to):
            current = wx.Size(*relative_to)
            min_size = wx.Size(*self.GetMinNotMinimisedSize())

            if direction == wx.HORIZONTAL:
                if min_size.x > current.x and min_size.y == current.y:
                    return min_size

            elif direction == wx.VERTICAL:
                if min_size.x == current.x and min_size.y > current.y:
                    return min_size

            elif direction == wx.BOTH:
                if min_size.x > current.x and min_size.y > current.y:
                    return min_size

        if self._art is not None:

            dc = wx.ClientDC(self)
            child_relative, dummy = self._art.GetPanelClientSize(dc, self, wx.Size(*relative_to), None)
            larger = wx.Size(-1, -1)

            if self.GetSizer():

                # We could just let the sizer expand in flow direction but see comment
                # in IsSizingContinuous()
                larger = self.GetPanelSizerBestSize()

                # and adjust for page in non flow direction
                if self._art.GetFlags() & RIBBON_BAR_FLOW_VERTICAL:
                     if larger.x != child_relative.x:
                        larger.x = child_relative.x

                elif larger.y != child_relative.y:
                    larger.y = child_relative.y

            elif len(self.GetChildren()) == 1:

                # Simple (and common) case of single ribbon child
                ribbon_child = self.GetChildren()[0]
                if isinstance(ribbon_child, RibbonControl):
                    larger = ribbon_child.GetNextLargerSize(direction, child_relative)

            if larger.IsFullySpecified(): # Use fallback if !(sizer/child = 1)
                if larger == child_relative:
                    return relative_to
                else:
                    return self._art.GetPanelSize(dc, self, wx.Size(*larger), None)


        # Fallback: Increase by 25% (equal to a prior or subsequent 20% decrease)
        # Note that due to rounding errors, this increase may not exactly equal a
        # matching decrease - an ideal solution would not have these errors, but
        # avoiding them is non-trivial unless an increase is by 100% rather than
        # a fractional amount. This would then be non-ideal as the resizes happen
        # at very large intervals.
        current = wx.Size(*relative_to)

        if direction & wx.HORIZONTAL:
            current.x = (current.x * 5 + 3) / 4

        if direction & wx.VERTICAL:
            current.y = (current.y * 5 + 3) / 4

        return current



    def CanAutoMinimise(self):
        """ Query if the panel can automatically minimise itself at small sizes. """

        return (self._flags & RIBBON_PANEL_NO_AUTO_MINIMISE) == 0 \
               and self._minimised_size.IsFullySpecified()


    def GetMinSize(self):
        """
        Returns the minimum size of the window, an indication to the sizer layout mechanism
        that this is the minimum required size.

        This method normally just returns the value set by `SetMinSize`, but it can be
        overridden to do the calculation on demand.
        """

        if self._expanded_panel != None:
            # Minimum size depends upon children, who are currently in the
            # expanded panel
            return self._expanded_panel.GetMinSize()

        if self.CanAutoMinimise():
            return wx.Size(*self._minimised_size)
        else:
            return self.GetMinNotMinimisedSize()


    def GetMinNotMinimisedSize(self):

        # Ask sizer if present
        if self.GetSizer():
            dc = wx.ClientDC(self)
            return self._art.GetPanelSize(dc, self, wx.Size(*self.GetPanelSizerMinSize()), None)

        # Common case of no sizer and single child taking up the entire panel
        elif len(self.GetChildren()) == 1:
            child = self.GetChildren()[0]
            dc = wx.ClientDC(self)
            return self._art.GetPanelSize(dc, self, wx.Size(*child.GetMinSize()), None)

        return wx.Size(*RibbonControl.GetMinSize(self))


    def GetPanelSizerMinSize(self):

        # Called from Realize() to set self._smallest_unminimised_size and from other
        # functions to get the minimum size.
        # The panel will be invisible when minimised and sizer calcs will be 0
        # Uses self._smallest_unminimised_size in preference to self.GetSizer().CalcMin()
        # to eliminate flicker.

        # Check if is visible and not previously calculated
        if self.IsShown() and not self._smallest_unminimised_size.IsFullySpecified():
             return self.GetSizer().CalcMin()

        # else use previously calculated self._smallest_unminimised_size
        dc = wx.ClientDC(self)
        return self._art.GetPanelClientSize(dc, self, wx.Size(*self._smallest_unminimised_size), None)[0]


    def GetPanelSizerBestSize(self):

        size = self.GetPanelSizerMinSize()
        # TODO allow panel to increase its size beyond minimum size
        # by steps similarly to ribbon control panels (preferred for aesthetics)
        # or continuously.
        return size


    def DoGetBestSize(self):
        """
        Gets the size which best suits the window: for a control, it would be the
        minimal size which doesn't truncate the control, for a panel - the same size
        as it would have after a call to `Fit()`.

        :return: An instance of :class:`wx.Size`.

        :note: Overridden from :class:`wx.Control`.
        """

        # Ask sizer if present
        if self.GetSizer():
            dc = wx.ClientDC(self)
            return self._art.GetPanelSize(dc, self, wx.Size(*self.GetPanelSizerBestSize()), None)

        # Common case of no sizer and single child taking up the entire panel
        elif len(self.GetChildren()) == 1:
            child = self.GetChildren()[0]
            dc = wx.ClientDC(self)
            return self._art.GetPanelSize(dc, self, wx.Size(*child.GetBestSize()), None)

        return wx.Size(*RibbonControl.DoGetBestSize(self))


    def Realize(self):
        """
        Realize all children of the panel.

        :note: Reimplemented from :class:`~wx.lib.agw.ribbon.control.RibbonControl`.
        """

        status = True
        children = self.GetChildren()

        for child in children:
            if not isinstance(child, RibbonControl):
                continue

            if not child.Realize():
                status = False

        minimum_children_size = wx.Size(0, 0)

        # Ask sizer if there is one present
        if self.GetSizer():
            minimum_children_size = wx.Size(*self.GetPanelSizerMinSize())
        elif len(children) == 1:
            minimum_children_size = wx.Size(*children[0].GetMinSize())

        if self._art != None:
            temp_dc = wx.ClientDC(self)
            self._smallest_unminimised_size = self._art.GetPanelSize(temp_dc, self, wx.Size(*minimum_children_size), None)

            panel_min_size = self.GetMinNotMinimisedSize()
            self._minimised_size, bitmap_size, self._preferred_expand_direction = self._art.GetMinimisedPanelMinimumSize(temp_dc, self, 1, 1)

            if self._minimised_icon.IsOk() and self._minimised_icon.GetSize() != bitmap_size:
                img = self._minimised_icon.ConvertToImage()
                img.Rescale(bitmap_size.GetWidth(), bitmap_size.GetHeight(), wx.IMAGE_QUALITY_HIGH)
                self._minimised_icon_resized = wx.Bitmap(img)
            else:
                self._minimised_icon_resized = self._minimised_icon

            if self._minimised_size.x > panel_min_size.x and self._minimised_size.y > panel_min_size.y:
                # No point in having a minimised size which is larger than the
                # minimum size which the children can go to.
                self._minimised_size = wx.Size(-1, -1)
            else:
                if self._art.GetFlags() & RIBBON_BAR_FLOW_VERTICAL:
                    self._minimised_size.x = panel_min_size.x
                else:
                    self._minimised_size.y = panel_min_size.y

        else:
            self._minimised_size = wx.Size(-1, -1)

        return self.Layout() and status


    def Layout(self):

        if self.IsMinimised():
            # Children are all invisible when minimised
            return True

        dc = wx.ClientDC(self)
        size, position = self._art.GetPanelClientSize(dc, self, wx.Size(*self.GetSize()), wx.Point())

        children = self.GetChildren()

        if self.GetSizer():
            self.GetSizer().SetDimension(position.x, position.y, size.x, size.y) # SetSize and Layout()
        elif len(children) == 1:
           # Common case of no sizer and single child taking up the entire panel
             children[0].SetSize(position.x, position.y, size.GetWidth(), size.GetHeight())

        if self.HasExtButton():
            self._ext_button_rect = self._art.GetPanelExtButtonArea(dc, self, self.GetSize())

        return True


    def OnMouseClick(self, event):
        """
        Handles the ``wx.EVT_LEFT_DOWN`` event for :class:`RibbonPanel`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        if self.IsMinimised():
            if self._expanded_panel != None:
                self.HideExpanded()
            else:
                self.ShowExpanded()

        elif self.IsExtButtonHovered():
            notification = RibbonPanelEvent(wxEVT_COMMAND_RIBBONPANEL_EXTBUTTON_ACTIVATED, self.GetId())
            notification.SetEventObject(self)
            notification.SetPanel(self)
            self.ProcessEvent(notification)


    def GetExpandedDummy(self):
        """
        Get the dummy panel of an expanded panel.

        :note: This should be called on an expanded panel to get the dummy associated
         with it - it will return ``None`` when called on the dummy itself.

        :see: :meth:`~RibbonPanel.ShowExpanded`, :meth:`~RibbonPanel.GetExpandedPanel`
        """

        return self._expanded_dummy


    def GetExpandedPanel(self):
        """
        Get the expanded panel of a dummy panel.

        :note: This should be called on a dummy panel to get the expanded panel
         associated with it - it will return ``None`` when called on the expanded panel
         itself.

        :see: :meth:`~RibbonPanel.ShowExpanded`, :meth:`~RibbonPanel.GetExpandedDummy`
        """

        return self._expanded_panel


    def ShowExpanded(self):
        """
        Show the panel externally expanded.

        When a panel is minimised, it can be shown full-size in a pop-out window, which
        is refered to as being (externally) expanded.

        :returns: ``True`` if the panel was expanded, ``False`` if it was not (possibly
         due to it not being minimised, or already being expanded).

        :note: When a panel is expanded, there exist two panels - the original panel
         (which is refered to as the dummy panel) and the expanded panel. The original
         is termed a dummy as it sits in the ribbon bar doing nothing, while the expanded
         panel holds the panel children.

        :see: :meth:`~RibbonPanel.HideExpanded`, :meth:`~RibbonPanel.GetExpandedPanel`
        """

        if not self.IsMinimised():
            return False

        if self._expanded_dummy != None or self._expanded_panel != None:
            return False

        size = self.GetBestSize()
        pos = self.GetExpandedPosition(wx.Rect(self.GetScreenPosition(), self.GetSize()), size, self._preferred_expand_direction).GetTopLeft()

        # Need a top-level frame to contain the expanded panel
        container = wx.Frame(None, wx.ID_ANY, self.GetLabel(), pos, size, wx.FRAME_NO_TASKBAR | wx.BORDER_NONE)

        self._expanded_panel = RibbonPanel(container, wx.ID_ANY, self.GetLabel(), self._minimised_icon, wx.Point(0, 0), size, self._flags)
        self._expanded_panel.SetArtProvider(self._art)
        self._expanded_panel._expanded_dummy = self

        # Move all children to the new panel.
        # Conceptually it might be simpler to reparent self entire panel to the
        # container and create a new panel to sit in its place while expanded.
        # This approach has a problem though - when the panel is reinserted into
        # its original parent, it'll be at a different position in the child list
        # and thus assume a new position.
        # NB: Children iterators not used as behaviour is not well defined
        # when iterating over a container which is being emptied

        for child in self.GetChildren():
            child.Reparent(self._expanded_panel)
            child.Show()


        # Move sizer to new panel
        if self.GetSizer():
            sizer = self.GetSizer()
            self.SetSizer(None, False)
            self._expanded_panel.SetSizer(sizer)

        self._expanded_panel.Realize()
        self.Refresh()
        container.Show()
        self._expanded_panel.SetFocus()

        return True


    def ShouldSendEventToDummy(self, event):

        # For an expanded panel, filter events between being sent up to the
        # floating top level window or to the dummy panel sitting in the ribbon
        # bar.

        # Child focus events should not be redirected, as the child would not be a
        # child of the window the event is redirected to. All other command events
        # seem to be suitable for redirecting.
        return event.IsCommandEvent() and event.GetEventType() != wx.wxEVT_CHILD_FOCUS


    def TryAfter(self, event):

        if self._expanded_dummy and self.ShouldSendEventToDummy(event):
            propagateOnce = wx.PropagateOnce(event)
            return self._expanded_dummy.GetEventHandler().ProcessEvent(event)
        else:
            return RibbonControl.TryAfter(self, event)


    def OnKillFocus(self, event):
        """
        Handles the ``wx.EVT_KILL_FOCUS`` event for :class:`RibbonPanel`.

        :param `event`: a :class:`FocusEvent` event to be processed.
        """

        if self._expanded_dummy:
            receiver = event.GetWindow()

            if IsAncestorOf(self, receiver):
                self._child_with_focus = receiver
                receiver.Bind(wx.EVT_KILL_FOCUS, self.OnChildKillFocus)

            elif receiver is None or receiver != self._expanded_dummy:
                self.HideExpanded()


    def OnChildKillFocus(self, event):
        """
        Handles the ``wx.EVT_KILL_FOCUS`` event for children of :class:`RibbonPanel`.

        :param `event`: a :class:`FocusEvent` event to be processed.
        """

        if self._child_with_focus == None:
            return # Should never happen, but a check can't hurt

        self._child_with_focus.Bind(wx.EVT_KILL_FOCUS, None)
        self._child_with_focus = None

        receiver = event.GetWindow()
        if receiver == self or IsAncestorOf(self, receiver):
            self._child_with_focus = receiver
            receiver.Bind(wx.EVT_KILL_FOCUS, self.OnChildKillFocus)
            event.Skip()

        elif receiver == None or receiver != self._expanded_dummy:
            self.HideExpanded()
            # Do not skip event, as the panel has been de-expanded, causing the
            # child with focus to be reparented (and hidden). If the event
            # continues propogation then bad things happen.

        else:
            event.Skip()


    def HideExpanded(self):
        """
        Hide the panel's external expansion.

        :returns: ``True`` if the panel was un-expanded, ``False`` if it was not
         (normally due to it not being expanded in the first place).

        :see: :meth:`~RibbonPanel.HideExpanded`, :meth:`~RibbonPanel.GetExpandedPanel`
        """

        if self._expanded_dummy == None:
            if self._expanded_panel:
                return self._expanded_panel.HideExpanded()
            else:
                return False

        # Move children back to original panel
        # NB: Children iterators not used as behaviour is not well defined
        # when iterating over a container which is being emptied
        for child in self.GetChildren():
            child.Reparent(self._expanded_dummy)
            child.Hide()

        # TODO: Move sizer back
        self._expanded_dummy._expanded_panel = None
        self._expanded_dummy.Realize()
        self._expanded_dummy.Refresh()
        parent = self.GetParent()
        self.Destroy()
        parent.Destroy()

        return True


    def GetExpandedPosition(self, panel, expanded_size, direction):

        # Strategy:
        # 1) Determine primary position based on requested direction
        # 2) Move the position so that it sits entirely within a display
        #    (for single monitor systems, this moves it into the display region,
        #     but for multiple monitors, it does so without splitting it over
        #     more than one display)
        # 2.1) Move in the primary axis
        # 2.2) Move in the secondary axis

        primary_x = False
        secondary_x = secondary_y = 0
        pos = wx.Point()

        if direction == wx.NORTH:
            pos.x = panel.GetX() + (panel.GetWidth() - expanded_size.GetWidth()) / 2
            pos.y = panel.GetY() - expanded_size.GetHeight()
            primary_x = True
            secondary_y = 1

        elif direction == wx.EAST:
            pos.x = panel.GetRight()
            pos.y = panel.GetY() + (panel.GetHeight() - expanded_size.GetHeight()) / 2
            secondary_x = -1

        elif direction == wx.SOUTH:
            pos.x = panel.GetX() + (panel.GetWidth() - expanded_size.GetWidth()) / 2
            pos.y = panel.GetBottom()
            primary_x = True
            secondary_y = -1

        else:
            pos.x = panel.GetX() - expanded_size.GetWidth()
            pos.y = panel.GetY() + (panel.GetHeight() - expanded_size.GetHeight()) / 2
            secondary_x = 1

        expanded = wx.Rect(pos, expanded_size)
        best = wx.Rect(*expanded)
        best_distance = 10000

        display_n = wx.Display.GetCount()

        for display_i in range(display_n):
            display = wx.Display(display_i).GetGeometry()
            if display.Contains(expanded):
                return expanded

            elif display.Intersects(expanded):
                new_rect = wx.Rect(*expanded)
                distance = 0

                if primary_x:
                    if expanded.GetRight() > display.GetRight():
                        distance = expanded.GetRight() - display.GetRight()
                        new_rect.x -= distance

                    elif expanded.GetLeft() < display.GetLeft():
                        distance = display.GetLeft() - expanded.GetLeft()
                        new_rect.x += distance

                else:
                    if expanded.GetBottom() > display.GetBottom():
                        distance = expanded.GetBottom() - display.GetBottom()
                        new_rect.y -= distance

                    elif expanded.GetTop() < display.GetTop():
                        distance = display.GetTop() - expanded.GetTop()
                        new_rect.y += distance

                if not display.Contains(new_rect):
                    # Tried moving in primary axis, but failed.
                    # Hence try moving in the secondary axis.
                    dx = secondary_x * (panel.GetWidth() + expanded_size.GetWidth())
                    dy = secondary_y * (panel.GetHeight() + expanded_size.GetHeight())
                    new_rect.x += dx
                    new_rect.y += dy

                    # Squaring makes secondary moves more expensive (and also
                    # prevents a negative cost)
                    distance += dx * dx + dy * dy

                if display.Contains(new_rect) and distance < best_distance:
                    best = new_rect
                    best_distance = distance

        return best


    def GetMinimisedIcon(self):
        """
        Get the bitmap to be used in place of the panel children when it is minimised.
        """

        return self._minimised_icon


    def GetDefaultBorder(self):
        """ Returns the default border style for :class:`RibbonPanel`. """

        return wx.BORDER_NONE


    def GetFlags(self):
        """ Returns the AGW-specific window style for :class:`RibbonPanel`. """

        return self._flags

