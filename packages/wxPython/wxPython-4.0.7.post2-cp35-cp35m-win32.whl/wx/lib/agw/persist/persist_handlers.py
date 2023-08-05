# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------- #
#
# Tags:        phoenix-port, unittest, documented, py3-port
#
# End Of Comments
# --------------------------------------------------------------------------- #
"""
This module contains different classes which handle different kind of saving/restoring
actions depending on the widget kind.
"""

import wx
import datetime

import wx.adv
import wx.html

# use this instead of wx.gizmos.TreeListCtrl
import wx.dataview as dv

# Will likely not be wrapped
# import wx.aui

# Not wrapped, unmaintained
# import wx.gizmos

# Not wrapped yet, coming soon
# import wx.media

import wx.lib.scrolledpanel as scrolled
import wx.lib.expando as expando
import wx.lib.buttons as buttons
import wx.lib.masked as masked
import wx.lib.colourselect as csel

import wx.lib.agw.aui as AUI
import wx.lib.agw.cubecolourdialog as CCD
import wx.lib.agw.customtreectrl as CT
import wx.lib.agw.flatmenu as FM
import wx.lib.agw.flatnotebook as FNB
import wx.lib.agw.floatspin as FS
import wx.lib.agw.foldpanelbar as FPB
import wx.lib.agw.hypertreelist as HTL
import wx.lib.agw.knobctrl as KC
import wx.lib.agw.labelbook as LBK
import wx.lib.agw.pycollapsiblepane as PCP

try:
    import wx.lib.agw.shapedbutton as SB
    hasSB = True
except:
    hasSB = False
    pass

import wx.lib.agw.ultimatelistctrl as ULC

from .persist_constants import *


def PyDate2wxDate(date):
    """
    Transforms a datetime.date object into a :class:`DateTime` one.

    :param `date`: a `datetime.date` object.
    """

    tt = date.timetuple()
    dmy = (tt[2], tt[1]-1, tt[0])
    return wx.DateTime.FromDMY(*dmy)


def wxDate2PyDate(date):
    """
    Transforms a :class:`DateTime` object into a `datetime.date` one.

    :param date: a :class:`DateTime` object.
    """

    if date.IsValid():
        ymd = list(map(int, date.FormatISODate().split('-')))
        return datetime.date(*ymd)
    else:
        return None


def CreateFont(font):
    """
    Creates a tuple of 7 :class:`wx.Font` attributes from the `font` input parameter.

    :param `font`: a :class:`wx.Font` instance.

    :returns: A tuple of 7 :class:`wx.Font` attributes from the `font` input parameter.
    """

    return font.GetPointSize(), font.GetFamily(), font.GetStyle(), font.GetWeight(), \
           font.GetUnderlined(), font.GetFaceName(), font.GetEncoding()


# ----------------------------------------------------------------------------------- #

class AbstractHandler(object):
    """
    Base class for persistent windows, uses the window name as persistent name by
    default and automatically reacts to the window destruction.

    .. note::

       This is an abstract class. If you wish to add another (custom) handler
       for your widgets, you should derive from :class:`AbstractHandler` and override
       the :meth:`Save() <AbstractHandler.Save>`,
       :meth:`Restore() <AbstractHandler.Restore>` and
       :meth:`GetKind() <AbstractHandler.GetKind>` methods.

    """

    def __init__(self, pObject):
        """
        Default class constructor.

        :param `pObject`: a :class:`~wx.lib.agw.persist.persistencemanager.PersistentObject` containing information about the
         persistent widget.
        """

        object.__init__(self)
        self._pObject = pObject
        self._window = pObject.GetWindow()
        if not hasattr(self._window, 'persistValue'):
            self._window.persistValue = None

        # need to move the import to here, otherwise we error in Python 3
        from . import persistencemanager as PM
        self._manager = PM.PersistenceManager.Get()

    def Save(self):
        """
        Saves the widget's settings by calling :meth:`PersistentObject.SaveValue() <lib.agw.persist.persistencemanager.PersistentObject.SaveValue>`, which in
        turns calls :meth:`PersistenceManager.SaveValue() <lib.agw.persist.persistencemanager.PersistenceManager.SaveValue>`.

        :note: This method must be overridden in derived classes.
        """

        pass


    def Restore(self):
        """
        Restores the widget's settings by calling :meth:`PersistentObject.RestoreValue() <lib.agw.persist.persistencemanager.PersistentObject.RestoreValue>`, which in
        turns calls :meth:`PersistenceManager.RestoreValue() <lib.agw.persist.persistencemanager.PersistenceManager.RestoreValue>`.

        :note: This method must be overridden in derived classes.
        """

        pass


    def GetKind(self):
        """
        Returns a short and meaningful *string* description of your widget.

        :note: This method must be overridden in derived classes.
        """

        pass


# ----------------------------------------------------------------------------------- #

class BookHandler(AbstractHandler):
    """
    Supports saving/restoring book control selection.

    This class handles the following wxPython widgets:

    - :class:`Toolbook`;
    - :class:`Choicebook`;
    - :class:`Listbook`;
    - :class:`Treebook` (except for opened tree branches, see :class:`TreebookHandler` for this);
    - :class:`Notebook`;
    - :class:`lib.agw.aui.auibook.AuiNotebook`;
    - :class:`lib.agw.flatnotebook.FlatNotebook`;
    - :class:`lib.agw.labelbook.LabelBook`;
    - :class:`lib.agw.labelbook.FlatImageBook`.

    """

    def __init__(self, pObject):

        AbstractHandler.__init__(self, pObject)


    def Save(self):

        book, obj = self._window, self._pObject
        obj.SaveValue(PERSIST_BOOK_SELECTION, book.GetSelection())

        if issubclass(book.__class__, AUI.AuiNotebook):
            if self._manager.GetManagerStyle() & PM_SAVE_RESTORE_AUI_PERSPECTIVES:
                # Allowed to save and restore perspectives
                perspective = book.SavePerspective()
                obj.SaveValue(PERSIST_BOOK_AGW_AUI_PERSPECTIVE, perspective)


    def Restore(self):

        book, obj = self._window, self._pObject
        sel = obj.RestoreValue(PERSIST_BOOK_SELECTION)

        retVal = True
        if issubclass(book.__class__, AUI.AuiNotebook):
            if self._manager.GetManagerStyle() & PM_SAVE_RESTORE_AUI_PERSPECTIVES:
                retVal = False
                # Allowed to save and restore perspectives
                perspective = obj.RestoreValue(PERSIST_BOOK_AGW_AUI_PERSPECTIVE)
                if perspective is not None:
                    retVal = book.LoadPerspective(perspective)
                    wx.CallAfter(book.Refresh)

        if sel is not None:
            if sel >= 0 and sel < book.GetPageCount():
                book.SetSelection(sel)
                return True and retVal

        return False


    def GetKind(self):

        return PERSIST_BOOK_KIND


# ----------------------------------------------------------------------------------- #

class TreebookHandler(BookHandler):
    """
    Supports saving/restoring open tree branches.

    This class handles the following wxPython widgets:

    - :class:`Treebook` (except for page selection, see :class:`BookHandler` for this).

    """

    def __init__(self, pObject):

        BookHandler.__init__(self, pObject)


    def Save(self):

        book, obj = self._window, self._pObject

        expanded = ""
        for page in range(book.GetPageCount()):
            if book.IsNodeExpanded(page):
                if expanded:
                    expanded += PERSIST_SEP

                expanded += "%u"%page

        obj.SaveValue(PERSIST_TREEBOOK_EXPANDED_BRANCHES, expanded)

        return BookHandler.Save(self)


    def Restore(self):

        book, obj = self._window, self._pObject

        expanded = obj.RestoreValue(PERSIST_TREEBOOK_EXPANDED_BRANCHES)

        if expanded:
            indices = expanded.split(PERSIST_SEP)
            pageCount = book.GetPageCount()

            for indx in indices:
                idx = int(indx)
                if idx >= 0 and idx < pageCount:
                    book.ExpandNode(idx)

        return BookHandler.Restore(self)


    def GetKind(self):

        return PERSIST_TREEBOOK_KIND


# ----------------------------------------------------------------------------------- #

class AUIHandler(AbstractHandler):
    """
    Supports saving/restoring :class:`lib.agw.aui.framemanager.AuiManager` perspectives.
    """

    def __init__(self, pObject):

        AbstractHandler.__init__(self, pObject)


    def Save(self):

        # Save the AUI perspectives if PersistenceManager allows it
        eventHandler = self._window.GetEventHandler()

        isAGWAui = isinstance(eventHandler, AUI.AuiManager)
        if not isAGWAui:
            return True

        if self._manager.GetManagerStyle() & PM_SAVE_RESTORE_AUI_PERSPECTIVES:
            # Allowed to save and restore perspectives
            perspective = eventHandler.SavePerspective()
            if isAGWAui:
                name = PERSIST_AGW_AUI_PERSPECTIVE
            else:
                name = PERSIST_AUI_PERSPECTIVE

            self._pObject.SaveValue(name, perspective)

        return True


    def Restore(self):

        # Restore the AUI perspectives if PersistenceManager allows it
        eventHandler = self._window.GetEventHandler()
        restoreCodeCaption = False

        isAGWAui = isinstance(eventHandler, AUI.AuiManager)
        if not isAGWAui:
            return True

        if self._manager.GetManagerStyle() & PM_SAVE_RESTORE_AUI_PERSPECTIVES:
            # Allowed to save and restore perspectives
            if isAGWAui:
                name = PERSIST_AGW_AUI_PERSPECTIVE
                restoreCodeCaption = self._manager.GetManagerStyle()
                restoreCodeCaption &= ~(PM_RESTORE_CAPTION_FROM_CODE)
            else:
                name = PERSIST_AUI_PERSPECTIVE

            perspective = self._pObject.RestoreValue(name)
            if perspective is not None:
                if restoreCodeCaption:
                    eventHandler.LoadPerspective(perspective,
                                                 restorecaption=True)
                else:
                    eventHandler.LoadPerspective(perspective)
                return True

        return True


    def GetKind(self):

        return PERSIST_AUIPERSPECTIVE_KIND


# ----------------------------------------------------------------------------------- #

class TLWHandler(AUIHandler):
    """
    Supports saving/restoring window position and size as well as
    maximized/iconized/restore state for toplevel windows.

    This class handles the following wxPython widgets:

    - All :class:`wx.Frame` derived classes;
    - All :class:`Dialog` derived classes.

    |

    In addition, if the toplevel window has an associated AuiManager (whether it is
    :class:`~wx.lib.agw.aui.framemanager.AuiManager`) and
    :class:`~wx.lib.agw.persist.persistencemanager.PersistenceManager`
    has the ``PM_SAVE_RESTORE_AUI_PERSPECTIVES`` style set (the default), this class
    will also save and restore AUI perspectives using the underlying :class:`AUIHandler`
    class.

    """

    def __init__(self, pObject):

        AUIHandler.__init__(self, pObject)


    def Save(self):

        tlw, obj = self._window, self._pObject

        pos = tlw.GetScreenPosition()
        obj.SaveValue(PERSIST_TLW_X, pos.x)
        obj.SaveValue(PERSIST_TLW_Y, pos.y)

        # Notice that we use GetSize() here and not GetClientSize() because
        # the latter doesn't return correct results for the minimized windows
        # (at least not under Windows)
        #
        # Of course, it shouldn't matter anyhow usually, the client size
        # should be preserved as well unless the size of the decorations
        # changed between the runs
        size = tlw.GetSize()
        obj.SaveValue(PERSIST_TLW_W, size.x)
        obj.SaveValue(PERSIST_TLW_H, size.y)

        obj.SaveValue(PERSIST_TLW_MAXIMIZED, tlw.IsMaximized())
        obj.SaveValue(PERSIST_TLW_ICONIZED, tlw.IsIconized())

        return AUIHandler.Save(self)


    def Restore(self):

        tlw, obj = self._window, self._pObject

        x, y = obj.RestoreValue(PERSIST_TLW_X), obj.RestoreValue(PERSIST_TLW_Y)
        w, h = obj.RestoreValue(PERSIST_TLW_W), obj.RestoreValue(PERSIST_TLW_H)

        hasPos = x is not None and y is not None
        hasSize = w is not None and h is not None

        if hasPos:
            # To avoid making the window completely invisible if it had been
            # shown on a monitor which was disconnected since the last run
            # (this is pretty common for notebook with external displays)
            #
            # NB: we should allow window position to be (slightly) off screen,
            #     it's not uncommon to position the window so that its upper
            #     left corner has slightly negative coordinate
            if wx.Display.GetFromPoint(wx.Point(x, y)) != wx.NOT_FOUND or \
               (hasSize and wx.Display.GetFromPoint(wx.Point(x+w, y+h)) != wx.NOT_FOUND):
                tlw.Move(wx.Point(x, y), wx.SIZE_ALLOW_MINUS_ONE)

            # else: should we try to adjust position/size somehow?

        if hasSize:
            tlw.SetSize((w, h))

        # Note that the window can be both maximized and iconized
        maximized = obj.RestoreValue(PERSIST_TLW_MAXIMIZED)
        if maximized:
            tlw.Maximize()

        iconized = obj.RestoreValue(PERSIST_TLW_ICONIZED)
        if iconized:
            tlw.Iconize()

        # The most important property of the window that we restore is its
        # size, so disregard the value of hasPos here
        return (hasSize and AUIHandler.Restore(self))


    def GetKind(self):

        return PERSIST_TLW_KIND


# ----------------------------------------------------------------------------------- #

class CheckBoxHandler(AbstractHandler):
    """
    Supports saving/restoring a :class:`CheckBox` state.

    This class handles the following wxPython widgets:

    - :class:`CheckBox`.

    """

    def __init__(self, pObject):

        AbstractHandler.__init__(self, pObject)


    def Save(self):

        check, obj = self._window, self._pObject

        if check.Is3State():
            obj.SaveCtrlValue(PERSIST_CHECKBOX_3STATE, check.Get3StateValue())
        else:
            obj.SaveCtrlValue(PERSIST_CHECKBOX, check.GetValue())

        return True


    def Restore(self):

        check, obj = self._window, self._pObject

        if check.Is3State():
            value = obj.RestoreCtrlValue(PERSIST_CHECKBOX_3STATE)
            if value is not None:
                check.Set3StateValue(value)
                return True
        else:
            value = obj.RestoreCtrlValue(PERSIST_CHECKBOX)
            if value is not None:
                check.SetValue(value)
                return True

        return False


    def GetKind(self):

        return PERSIST_CHECKBOX_KIND


# ----------------------------------------------------------------------------------- #

class ListBoxHandler(AbstractHandler):
    """
    Supports saving/restoring selected items in :class:`ListBox`, :class:`ListCtrl`, :class:`ListView`,
    :class:`VListBox`, :class:`html.HtmlListBox`, :class:`html.SimpleHtmlListBox`, :class:`adv.EditableListBox`.

    This class handles the following wxPython widgets:

    - :class:`ListBox`;
    - :class:`ListCtrl` (only for selected items. For column sizes see :class:`ListCtrlHandler`);
    - :class:`ListView` (only for selected items. For column sizes see :class:`ListCtrlHandler`);
    - :class:`VListBox`;
    - :class:`html.HtmlListBox`;
    - :class:`html.SimpleHtmlListBox`;
    - :class:`adv.EditableListBox`.

    """

    def __init__(self, pObject):

        AbstractHandler.__init__(self, pObject)


    def GetSelections(self, listBox):
        """
        Returns a list of selected items for :class:`ListBox`, :class:`ListCtrl`, :class:`ListView`,
        :class:`VListBox`, :class:`html.HtmlListBox`, :class:`html.SimpleHtmlListBox`, :class:`adv.EditableListBox`.

        :param `listBox`: an instance of :class:`ListBox`, :class:`ListCtrl`, :class:`ListView`,
         :class:`VListBox`, :class:`html.HtmlListBox`, :class:`html.SimpleHtmlListBox`, :class:`adv.EditableListBox`..
        """

        indices = []

        if isinstance(listBox, (wx.html.HtmlListBox, wx.html.SimpleHtmlListBox)):
            if listBox.GetSelectedCount() == 0:
                return indices
        else:
            if listBox.GetSelectedItemCount() == 0:
                return indices

        isVirtual = issubclass(listBox.__class__, wx.VListBox)

        if isVirtual:
            # This includes wx.SimpleHtmlListBox and wx.HtmlListBox
            if listBox.GetWindowStyleFlag() & wx.LB_SINGLE:
                selection = listBox.GetSelection()
                return (selection >= 0 and [selection] or [indices])[0]
        else:
            # wx.ListCtrl
            if listBox.GetWindowStyleFlag() & wx.LC_SINGLE_SEL:
                selection = listBox.GetSelection()
                return (selection >= 0 and [selection] or [indices])[0]

        if isVirtual:
            item, cookie = listBox.GetFirstSelected()
            while item != wx.NOT_FOUND:
                indices.append(item)
                item, cookie = listBox.GetNextSelected(cookie)

            return indices

        lastFound = -1
        # Loop until told to stop
        while 1:
            index = listBox.GetNextItem(lastFound, wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED)
            if index == wx.NOT_FOUND:
                # No item selected
                break
            else:
                # Found one item, append to the list of condemned
                lastFound = index
                indices.append(index)

        return indices


    def Save(self):

        if self._manager.GetManagerStyle() & PM_SAVE_RESTORE_TREE_LIST_SELECTIONS == 0:
            # We don't want to save selected items
            return True

        listBox, obj = self._window, self._pObject

        if issubclass(listBox.__class__, wx.ListBox):
            selections = listBox.GetSelections()
        else:
            selections = self.GetSelections(listBox)

        obj.SaveValue(PERSIST_LISTBOX_SELECTIONS, selections)
        return True


    def Restore(self):

        if self._manager.GetManagerStyle() & PM_SAVE_RESTORE_TREE_LIST_SELECTIONS == 0:
            # We don't want to save selected items
            return True

        listBox, obj = self._window, self._pObject

        isVirtual = issubclass(listBox.__class__, wx.VListBox) or isinstance(listBox, wx.CheckListBox)

        isHtml = isinstance(listBox, wx.html.HtmlListBox)
        if isVirtual and not isHtml:
            count = listBox.GetCount()
        else:
            count = listBox.GetItemCount()

        selections = obj.RestoreValue(PERSIST_LISTBOX_SELECTIONS)

        if selections is not None:
            for index in selections:
                if index < count:
                    listBox.Select(index)

            return True

        return False


    def GetKind(self):

        return PERSIST_LISTBOX_KIND


# ----------------------------------------------------------------------------------- #

class ListCtrlHandler(ListBoxHandler):
    """
    Supports saving/restoring selected items and column sizes in :class:`ListCtrl`.

    This class handles the following wxPython widgets:

    - :class:`ListCtrl` (only for column sizes. For selected items see :class:`ListBoxHandler`);
    - :class:`ListView` (only for column sizes. For selected items see :class:`ListBoxHandler`).
    """

    def __init__(self, pObject):

        ListBoxHandler.__init__(self, pObject)


    def Save(self):

        listCtrl, obj = self._window, self._pObject

        retVal = ListBoxHandler.Save(self)

        if not listCtrl.InReportView():
            return retVal

        colSizes = []
        for col in range(listCtrl.GetColumnCount()):
            colSizes.append(listCtrl.GetColumnWidth(col))

        obj.SaveValue(PERSIST_LISTCTRL_COLWIDTHS, colSizes)

        return retVal


    def Restore(self):

        listCtrl, obj = self._window, self._pObject

        retVal = ListBoxHandler.Restore(self)

        if not listCtrl.InReportView():
            return retVal

        colSizes = obj.RestoreValue(PERSIST_LISTCTRL_COLWIDTHS)
        if colSizes is None:
            return False

        count = listCtrl.GetColumnCount()
        for col, size in enumerate(colSizes):
            if col < count:
                listCtrl.SetColumnWidth(col, size)

        return retVal


    def GetKind(self):

        return PERSIST_LISTCTRL_KIND


# ----------------------------------------------------------------------------------- #

class CheckListBoxHandler(ListBoxHandler):
    """
    Supports saving/restoring checked and selected items in :class:`CheckListBox`.

    This class handles the following wxPython widgets:

    - :class:`CheckListBox` (only for checked items. For selected items see :class:`ListBoxHandler`).

    """

    def __init__(self, pObject):

        ListBoxHandler.__init__(self, pObject)


    def Save(self):

        checkList, obj = self._window, self._pObject

        checked = []
        for index in range(checkList.GetCount()):
            if checkList.IsChecked(index):
                checked.append(index)

        obj.SaveValue(PERSIST_CHECKLIST_CHECKED, checked)

        return ListBoxHandler.Save(self)


    def Restore(self):

        checkList, obj = self._window, self._pObject

        checked = obj.RestoreValue(PERSIST_CHECKLIST_CHECKED)
        count = checkList.GetCount()
        if checked is not None:
            for index in checked:
                if index < count:
                    checkList.Check(index)

        return ListBoxHandler.Restore(self)


    def GetKind(self):

        return PERSIST_CHECKLISTBOX_KIND


# ----------------------------------------------------------------------------------- #

class ChoiceComboHandler(AbstractHandler):
    """
    Supports saving/restoring :class:`Choice`, :class:`ComboBox` and :class:`adv.OwnerDrawnComboBox`
    selection.

    This class handles the following wxPython widgets:

    - :class:`Choice`;
    - :class:`ComboBox`;
    - :class:`adv.OwnerDrawnComboBox`.

    """

    def __init__(self, pObject):

        AbstractHandler.__init__(self, pObject)


    def Save(self):

        combo, obj = self._window, self._pObject

        value = combo.GetStringSelection()
        obj.SaveCtrlValue(PERSIST_CHOICECOMBO_SELECTION, value)
        return True


    def Restore(self):

        combo, obj = self._window, self._pObject

        value = obj.RestoreCtrlValue(PERSIST_CHOICECOMBO_SELECTION)
        if value is not None:
            if value in combo.GetStrings():
                combo.SetStringSelection(value)

            return True

        return False


    def GetKind(self):

        return PERSIST_CHOICECOMBO_KIND


# ----------------------------------------------------------------------------------- #

class FoldPanelBarHandler(AbstractHandler):
    """
    Supports saving/restoring of :class:`lib.agw.foldpanelbar.FoldPanelBar`.

    This class handles the following wxPython widgets

    - :class:`lib.agw.foldpanelbar.FoldPanelBar`
    """

    def __init__(self, pObject):

        AbstractHandler.__init__(self, pObject)


    def Save(self):

        fpb, obj = self._window, self._pObject
        expanded = [fpb.GetFoldPanel(i).IsExpanded() for i in range(fpb.GetCount())]
        obj.SaveValue(PERSIST_FOLDPANELBAR_EXPANDED, expanded)

        return True


    def Restore(self):

        fpb, obj = self._window, self._pObject
        expanded = obj.RestoreValue(PERSIST_FOLDPANELBAR_EXPANDED)

        if expanded is None:
            return False
        else:
            for idx, expand in enumerate(expanded):
                panel = fpb.GetFoldPanel(idx)
                if expand:
                    fpb.Expand(panel)
                else:
                    fpb.Collapse(panel)

            return True


    def GetKind(self):

        return PERSIST_FOLDPANELBAR_KIND


# ----------------------------------------------------------------------------------- #

class RadioBoxHandler(AbstractHandler):
    """
    Supports saving/restoring a :class:`RadioBox` state.

    This class handles the following wxPython widgets:

    - :class:`RadioBox`.

    """

    def __init__(self, pObject):

        AbstractHandler.__init__(self, pObject)


    def Save(self):

        radio, obj = self._window, self._pObject
        obj.SaveCtrlValue(PERSIST_RADIOBOX_SELECTION, radio.GetSelection())
        return True


    def Restore(self):

        radio, obj = self._window, self._pObject
        value = obj.RestoreCtrlValue(PERSIST_RADIOBOX_SELECTION)
        if value is not None:
            if value < radio.GetCount():
                radio.SetSelection(value)
                return True

        return False


    def GetKind(self):

        return PERSIST_RADIOBOX_KIND


# ----------------------------------------------------------------------------------- #

class RadioButtonHandler(AbstractHandler):
    """
    Supports saving/restoring a :class:`RadioButton` state.

    This class handles the following wxPython widgets:

    - :class:`RadioButton`.

    """

    def __init__(self, pObject):

        AbstractHandler.__init__(self, pObject)


    def Save(self):

        radio, obj = self._window, self._pObject
        obj.SaveCtrlValue(PERSIST_RADIOBUTTON_VALUE, radio.GetValue())
        return True


    def Restore(self):

        radio, obj = self._window, self._pObject
        value = obj.RestoreCtrlValue(PERSIST_RADIOBUTTON_VALUE)
        if value is not None:
            radio.SetValue(value)
            return True

        return False


    def GetKind(self):

        return PERSIST_RADIOBUTTON_KIND


# ----------------------------------------------------------------------------------- #

class ScrolledWindowHandler(AbstractHandler):
    """
    Supports saving/restoring a :class:`ScrolledWindow` / :class:`lib.scrolledpanel.ScrolledPanel`
    scroll position.

    This class handles the following wxPython widgets:

    - :class:`ScrolledWindow`;
    - :class:`lib.scrolledpanel.ScrolledPanel`.

    """

    def __init__(self, pObject):

        AbstractHandler.__init__(self, pObject)


    def Save(self):

        scroll, obj = self._window, self._pObject

        scrollPos = scroll.GetScrollPos(wx.HORIZONTAL)
        obj.SaveValue(PERSIST_SCROLLEDWINDOW_POS_H, scrollPos)
        scrollPos = scroll.GetScrollPos(wx.VERTICAL)
        obj.SaveValue(PERSIST_SCROLLEDWINDOW_POS_V, scrollPos)
        return True


    def Restore(self):

        scroll, obj = self._window, self._pObject
        hpos = obj.RestoreValue(PERSIST_SCROLLEDWINDOW_POS_H)
        vpos = obj.RestoreValue(PERSIST_SCROLLEDWINDOW_POS_V)

        if hpos:
            scroll.SetScrollPos(wx.HORIZONTAL, hpos)
        if vpos:
            scroll.SetScrollPos(wx.VERTICAL, vpos, True)

        return True


    def GetKind(self):

        return PERSIST_SCROLLEDWINDOW_KIND


# ----------------------------------------------------------------------------------- #

class SliderHandler(AbstractHandler):
    """
    Supports saving/restoring a :class:`Slider` / :class:`lib.agw.knobctrl.KnobCtrl` thumb position.

    This class handles the following wxPython widgets:

    - :class:`Slider`;
    - :class:`lib.agw.knobctrl.KnobCtrl`.

    """

    def __init__(self, pObject):

        AbstractHandler.__init__(self, pObject)


    def Save(self):

        slider, obj = self._window, self._pObject
        obj.SaveCtrlValue(PERSIST_SLIDER_VALUE, slider.GetValue())
        return True


    def Restore(self):

        slider, obj = self._window, self._pObject
        value = obj.RestoreCtrlValue(PERSIST_SLIDER_VALUE)

        if issubclass(slider.__class__, wx.Slider):
            minVal, maxVal = slider.GetMin(), slider.GetMax()
        else:
            # KnobCtrl
            minVal, maxVal = slider.GetMinValue(), slider.GetMaxValue()

        if value is not None:
            if value >= minVal and value <= maxVal:
                slider.SetValue(value)
                return True

        return False


    def GetKind(self):

        return PERSIST_SLIDER_KIND


# ----------------------------------------------------------------------------------- #

class SpinHandler(AbstractHandler):
    """
    Supports saving/restoring a :class:`SpinButton` / :class:`SpinCtrl` value.

    This class handles the following wxPython widgets:

    - :class:`SpinCtrl`;
    - :class:`SpinButton`.
    """

    def __init__(self, pObject):

        AbstractHandler.__init__(self, pObject)


    def Save(self):

        spin, obj = self._window, self._pObject
        obj.SaveCtrlValue(PERSIST_SPIN_VALUE, spin.GetValue())
        return True


    def Restore(self):

        spin, obj = self._window, self._pObject
        value = obj.RestoreCtrlValue(PERSIST_SPIN_VALUE)

        if value is not None:
            minVal, maxVal = spin.GetMin(), spin.GetMax()
            if value >= minVal and value <= maxVal:
                spin.SetValue(value)
                return True

        return False


    def GetKind(self):

        return PERSIST_SPIN_KIND


# ----------------------------------------------------------------------------------- #

class SplitterHandler(AbstractHandler):
    """
    Supports saving/restoring a :class:`SplitterWindow` splitter position.

    This class handles the following wxPython widgets:

    - :class:`SplitterWindow`.

    """

    def __init__(self, pObject):

        AbstractHandler.__init__(self, pObject)


    def Save(self):

        splitter, obj = self._window, self._pObject
        obj.SaveValue(PERSIST_SPLITTER_POSITION, splitter.GetSashPosition())
        return True


    def Restore(self):

        splitter, obj = self._window, self._pObject
        value = obj.RestoreValue(PERSIST_SPLITTER_POSITION)

        if value is None:
            return False

        if not splitter.IsSplit():
            return False

        width, height = splitter.GetClientSize()
        minPaneSize = splitter.GetMinimumPaneSize()
        direction = splitter.GetSplitMode()

        if direction == wx.SPLIT_HORIZONTAL:
            # Top and bottom panes
            if value > height - minPaneSize:
                return False
        else:
            # Left and right panes
            if value > width - minPaneSize:
                return False

        splitter.SetSashPosition(value)
        return True


    def GetKind(self):

        return PERSIST_SPLITTER_KIND


# ----------------------------------------------------------------------------------- #

class TextCtrlHandler(AbstractHandler):
    """
    Supports saving/restoring a :class:`TextCtrl` entered string.

    This class handles the following wxPython widgets:

    - :class:`TextCtrl`;
    - :class:`SearchCtrl`;
    - :class:`lib.expando.ExpandoTextCtrl`;
    - :class:`lib.masked.textctrl.TextCtrl`;
    - :class:`lib.masked.combobox.ComboBox`;
    - :class:`lib.masked.ipaddrctrl.IpAddrCtrl`;
    - :class:`lib.masked.timectrl.TimeCtrl`;
    - :class:`lib.masked.numctrl.NumCtrl`;

    """

    def __init__(self, pObject):

        AbstractHandler.__init__(self, pObject)


    def Save(self):

        text, obj = self._window, self._pObject
        obj.SaveCtrlValue(PERSIST_TEXTCTRL_VALUE, text.GetValue())
        return True


    def Restore(self):

        text, obj = self._window, self._pObject
        value = obj.RestoreCtrlValue(PERSIST_TEXTCTRL_VALUE)

        if value is not None:
            text.ChangeValue(value)
            return True

        return False


    def GetKind(self):

        return PERSIST_TEXTCTRL_KIND


# ----------------------------------------------------------------------------------- #

class ToggleButtonHandler(AbstractHandler):
    """
    Supports saving/restoring a :class:`ToggleButton` and friends state.

    This class handles the following wxPython widgets:

    - :class:`ToggleButton`;
    - :class:`lib.buttons.GenToggleButton`;
    - :class:`lib.buttons.GenBitmapToggleButton`;
    - :class:`lib.buttons.GenBitmapTextToggleButton`;
    - :class:`lib.agw.shapedbutton.SToggleButton`;
    - :class:`lib.agw.shapedbutton.SBitmapToggleButton`;
    - :class:`lib.agw.shapedbutton.SBitmapTextToggleButton`.

    """

    def __init__(self, pObject):

        AbstractHandler.__init__(self, pObject)


    def Save(self):

        toggle, obj = self._window, self._pObject
        obj.SaveValue(PERSIST_TOGGLEBUTTON_TOGGLED, toggle.GetValue())
        return True


    def Restore(self):

        toggle, obj = self._window, self._pObject
        value = obj.RestoreValue(PERSIST_TOGGLEBUTTON_TOGGLED)

        if value is not None:
            toggle.SetValue(value)
            return True

        return False


    def GetKind(self):

        return PERSIST_TOGGLEBUTTON_KIND

# ----------------------------------------------------------------------------------- #

class TreeCtrlHandler(AbstractHandler):
    """
    Supports saving/restoring a :class:`TreeCtrl` expansion state, selections and
    checked items state (meaningful only for :class:`lib.agw.customtreectrl.CustomTreeCtrl`).

    This class handles the following wxPython widgets:

    - :class:`TreeCtrl`;
    - :class:`GenericDirCtrl`;
    - :class:`lib.agw.customtreectrl.CustomTreeCtrl`;
    - :class:`lib.agw.hypertreelist.HyperTreeList`;

    """

    def __init__(self, pObject):

        AbstractHandler.__init__(self, pObject)


    def GetItemChildren(self, item=None, recursively=False):
        """
        Return the children of item as a list.

        :param `item`: a :class:`TreeCtrl` item or a :class:`~wx.lib.agw.customtreectrl.CustomTreeCtrl` item;
        :param `recursively`: whether to recurse into the item hierarchy or not.
        """

        if not item:
            item = self._window.GetRootItem()
            if not item:
                return []

        children = []
        child, cookie = self._window.GetFirstChild(item)

        while child and child.IsOk():
            children.append(child)
            if recursively:
                children.extend(self.GetItemChildren(child, True))
            child, cookie = self._window.GetNextChild(item, cookie)

        return children


    def GetIndexOfItem(self, item):
        """
        Return the index of item.

        :param `item`: a :class:`TreeCtrl` item or a :class:`~wx.lib.agw.customtreectrl.CustomTreeCtrl` item;
        """

        parent = self._window.GetItemParent(item)
        if parent:
            parentIndices = self.GetIndexOfItem(parent)
            ownIndex = self.GetItemChildren(parent).index(item)
            return parentIndices + (ownIndex,)
        else:
            return ()


    def GetItemIdentity(self, item):
        """
        Return a hashable object that represents the identity of the
        item. By default this returns the position of the item in the
        tree. You may want to override this to return the item label
        (if you know that labels are unique and don't change), or return
        something that represents the underlying domain object, e.g.
        a database key.

        :param `item`: a :class:`TreeCtrl` item or a :class:`~wx.lib.agw.customtreectrl.CustomTreeCtrl` item;
        """

        return self.GetIndexOfItem(item)


    def GetExpansionState(self):
        """
        Returns list of expanded items. Expanded items are coded as determined by
        the result of :meth:`TreeCtrlHandler.GetItemIdentity() <TreeCtrlHandler.GetItemIdentity>`.
        """

        root = self._window.GetRootItem()
        if not root:
            return []
        if self._window.HasFlag(wx.TR_HIDE_ROOT):
            return self.GetExpansionStateOfChildren(root)
        else:
            return self.GetExpansionStateOfItem(root)


    def SetExpansionState(self, listOfExpandedItems):
        """
        Expands all tree items whose identity, as determined by :meth:`TreeCtrlHandler.GetItemIdentity() <TreeCtrlHandler.GetItemIdentity>`,
        is present in the list and collapses all other tree items.

        :param `listOfExpandedItems`: a list of expanded :class:`TreeCtrl` or
         :class:`~wx.lib.agw.customtreectrl.CustomTreeCtrl` items.
        """

        root = self._window.GetRootItem()
        if not root:
            return
        if self._window.HasFlag(wx.TR_HIDE_ROOT):
            self.SetExpansionStateOfChildren(listOfExpandedItems, root)
        else:
            self.SetExpansionStateOfItem(listOfExpandedItems, root)


    def GetSelectionState(self):
        """
        Returns a list of selected items. Selected items are coded as determined by
        the result of :meth:`TreeCtrlHandler.GetItemIdentity() <TreeCtrlHandler.GetItemIdentity>`.
        """

        root = self._window.GetRootItem()
        if not root:
            return []
        if self._window.HasFlag(wx.TR_HIDE_ROOT):
            return self.GeSelectionStateOfChildren(root)
        else:
            return self.GetSelectionStateOfItem(root)


    def SetSelectionState(self, listOfSelectedItems):
        """
        Selects all tree items whose identity, as determined by :meth:`TreeCtrlHandler.GetItemIdentity() <TreeCtrlHandler.GetItemIdentity>`,
        is present in the list and unselects all other tree items.

        :param `listOfSelectedItems`: a list of selected :class:`TreeCtrl` or
         :class:`~wx.lib.agw.customtreectrl.CustomTreeCtrl` items.
        """

        root = self._window.GetRootItem()
        if not root:
            return
        if self._window.HasFlag(wx.TR_HIDE_ROOT):
            self.SetSelectedStateOfChildren(listOfSelectedItems, root)
        else:
            self.SetSelectedStateOfItem(listOfSelectedItems, root)


    def GetCheckedState(self):
        """
        Returns a list of checked items. Checked items are coded as determined by
        the result of :meth:`TreeCtrlHandler.GetItemIdentity() <TreeCtrlHandler.GetItemIdentity>`.

        :note:

         This is meaningful only for :class:`~wx.lib.agw.customtreectrl.CustomTreeCtrl` and
         :class:`~wx.lib.agw.hypertreelist.HyperTreeList`.
        """

        root = self._window.GetRootItem()
        if not root:
            return []
        if self._window.HasFlag(wx.TR_HIDE_ROOT):
            return self.GetCheckedStateOfChildren(root)
        else:
            return self.GetCheckedStateOfItem(root)


    def SetCheckedState(self, listOfCheckedItems):
        """
        Checks all tree items whose identity, as determined by :meth:`TreeCtrlHandler.GetItemIdentity() <TreeCtrlHandler.GetItemIdentity>`, is present
        in the list and unchecks all other tree items.

        :param `listOfCheckedItems`: a list of checked :class:`~wx.lib.agw.customtreectrl.CustomTreeCtrl` items.

        :note:

         This is meaningful only for :class:`~wx.lib.agw.customtreectrl.CustomTreeCtrl` and
         :class:`~wx.lib.agw.hypertreelist.HyperTreeList`.
        """

        root = self._window.GetRootItem()
        if not root:
            return
        if self._window.HasFlag(wx.TR_HIDE_ROOT):
            self.SetCheckedStateOfChildren(listOfCheckedItems, root)
        else:
            self.SetCheckedStateOfItem(listOfCheckedItems, root)


    def GetExpansionStateOfItem(self, item):
        """
        Returns the expansion state of a tree item.

        :param `item`: a :class:`TreeCtrl` item or a :class:`~wx.lib.agw.customtreectrl.CustomTreeCtrl` item.
        """

        listOfExpandedItems = []
        if self._window.IsExpanded(item):
            listOfExpandedItems.append(self.GetItemIdentity(item))
            listOfExpandedItems.extend(self.GetExpansionStateOfChildren(item))

        return listOfExpandedItems


    def GetExpansionStateOfChildren(self, item):
        """
        Returns the expansion state of the children of a tree item.

        :param `item`: a :class:`TreeCtrl` item or a :class:`~wx.lib.agw.customtreectrl.CustomTreeCtrl` item.
        """

        listOfExpandedItems = []
        for child in self.GetItemChildren(item):
            listOfExpandedItems.extend(self.GetExpansionStateOfItem(child))

        return listOfExpandedItems


    def GetCheckedStateOfItem(self, item):
        """
        Returns the checked/unchecked state of a tree item.

        :param `item`: a :class:`~wx.lib.agw.customtreectrl.CustomTreeCtrl` item.
        """

        listOfCheckedItems = []
        if self._window.IsItemChecked(item):
            listOfCheckedItems.append(self.GetItemIdentity(item))

        listOfCheckedItems.extend(self.GetCheckedStateOfChildren(item))

        return listOfCheckedItems


    def GetCheckedStateOfChildren(self, item):
        """
        Returns the checked/unchecked state of the children of a tree item.

        :param `item`: a :class:`~wx.lib.agw.customtreectrl.CustomTreeCtrl` item.
        """

        listOfCheckedItems = []
        for child in self.GetItemChildren(item):
            listOfCheckedItems.extend(self.GetCheckedStateOfItem(child))

        return listOfCheckedItems


    def GetSelectionStateOfItem(self, item):
        """
        Returns the selection state of a tree item.

        :param `item`: a :class:`TreeCtrl` item or a :class:`~wx.lib.agw.customtreectrl.CustomTreeCtrl` item.
        """

        listOfSelectedItems = []
        if self._window.IsSelected(item):
            listOfSelectedItems.append(self.GetItemIdentity(item))

        listOfSelectedItems.extend(self.GetSelectionStateOfChildren(item))
        return listOfSelectedItems


    def GetSelectionStateOfChildren(self, item):
        """
        Returns the selection state of the children of a tree item.

        :param `item`: a :class:`TreeCtrl` item or a :class:`~wx.lib.agw.customtreectrl.CustomTreeCtrl` item.
        """

        listOfSelectedItems = []
        for child in self.GetItemChildren(item):
            listOfSelectedItems.extend(self.GetSelectionStateOfItem(child))

        return listOfSelectedItems


    def SetExpansionStateOfItem(self, listOfExpandedItems, item):
        """
        Sets the expansion state of a tree item (expanded or collapsed).

        :param `listOfExpandedItems`: a list of expanded :class:`TreeCtrl` or
         :class:`~wx.lib.agw.customtreectrl.CustomTreeCtrl` items;
        :param `item`: a :class:`TreeCtrl` item or a :class:`~wx.lib.agw.customtreectrl.CustomTreeCtrl` item.
        """

        if self.GetItemIdentity(item) in listOfExpandedItems:
            self._window.Expand(item)
            self.SetExpansionStateOfChildren(listOfExpandedItems, item)
        else:
            self._window.Collapse(item)


    def SetExpansionStateOfChildren(self, listOfExpandedItems, item):
        """
        Sets the expansion state of the children of a tree item (expanded or collapsed).

        :param `listOfExpandedItems`: a list of expanded :class:`TreeCtrl` or
         :class:`~wx.lib.agw.customtreectrl.CustomTreeCtrl` items;
        :param `item`: a :class:`TreeCtrl` item or a :class:`~wx.lib.agw.customtreectrl.CustomTreeCtrl` item.
        """

        for child in self.GetItemChildren(item):
            self.SetExpansionStateOfItem(listOfExpandedItems, child)


    def SetCheckedStateOfItem(self, listOfCheckedItems, item):
        """
        Sets the checked/unchecked state of a tree item.

        :param `listOfCheckedItems`: a list of checked :class:`~wx.lib.agw.customtreectrl.CustomTreeCtrl` items;
        :param `item`: a :class:`~wx.lib.agw.customtreectrl.CustomTreeCtrl` item.
        """

        if self.GetItemIdentity(item) in listOfCheckedItems:
            self._window.CheckItem2(item, True)
        else:
            self._window.CheckItem2(item, False)

        self.SetCheckedStateOfChildren(listOfCheckedItems, item)


    def SetCheckedStateOfChildren(self, listOfCheckedItems, item):
        """
        Sets the checked/unchecked state of the children of a tree item.

        :param `listOfCheckedItems`: a list of checked :class:`~wx.lib.agw.customtreectrl.CustomTreeCtrl` items;
        :param `item`: a :class:`~wx.lib.agw.customtreectrl.CustomTreeCtrl` item.
        """

        for child in self.GetItemChildren(item):
            self.SetCheckedStateOfItem(listOfCheckedItems, child)


    def SetSelectedStateOfItem(self, listOfSelectedItems, item):
        """
        Sets the selection state of a tree item.

        :param `listOfSelectedItems`: a list of selected :class:`TreeCtrl` or
         :class:`~wx.lib.agw.customtreectrl.CustomTreeCtrl` items;
        :param `item`: a :class:`TreeCtrl` item or a :class:`~wx.lib.agw.customtreectrl.CustomTreeCtrl` item.
        """

        if self.GetItemIdentity(item) in listOfSelectedItems:
            self._window.SelectItem(item)

        self.SetSelectedStateOfChildren(listOfSelectedItems, item)


    def SetSelectedStateOfChildren(self, listOfSelectedItems, item):
        """
        Sets the selection state of the children of a tree item.

        :param `listOfSelectedItems`: a list of selected :class:`TreeCtrl` or
         :class:`~wx.lib.agw.customtreectrl.CustomTreeCtrl` items;
        :param `item`: a :class:`TreeCtrl` item or a :class:`~wx.lib.agw.customtreectrl.CustomTreeCtrl` item.
        """

        for child in self.GetItemChildren(item):
            self.SetSelectedStateOfItem(listOfSelectedItems, child)


    def Save(self):

        tree, obj = self._window, self._pObject

        obj.SaveCtrlValue(PERSIST_TREECTRL_EXPANSION, self.GetExpansionState())

        if issubclass(tree.__class__, (HTL.HyperTreeList, CT.CustomTreeCtrl)):
            obj.SaveCtrlValue(PERSIST_TREECTRL_CHECKED_ITEMS, self.GetCheckedState())

        if self._manager.GetManagerStyle() & PM_SAVE_RESTORE_TREE_LIST_SELECTIONS == 0:
            # We don't want to save selected items
            return True

        obj.SaveCtrlValue(PERSIST_TREECTRL_SELECTIONS, self.GetSelectionState())
        return True


    def Restore(self):

        tree, obj = self._window, self._pObject
        expansion = obj.RestoreCtrlValue(PERSIST_TREECTRL_EXPANSION)
        selections = obj.RestoreCtrlValue(PERSIST_TREECTRL_SELECTIONS)

        if expansion is not None:
            self.SetExpansionState(expansion)

        if self._manager.GetManagerStyle() & PM_SAVE_RESTORE_TREE_LIST_SELECTIONS:
            # We want to restore selected items
            if selections is not None:
                self.SetSelectionState(selections)

        if not issubclass(tree.__class__, (HTL.HyperTreeList, CT.CustomTreeCtrl)):
            return (expansion is not None and selections is not None)

        checked = obj.RestoreCtrlValue(PERSIST_TREECTRL_CHECKED_ITEMS)
        if checked is not None:
            self.SetCheckedState(checked)

        return (expansion is not None and selections is not None and checked is not None)


    def GetKind(self):

        return PERSIST_TREECTRL_KIND


# ----------------------------------------------------------------------------------- #

class TreeListCtrlHandler(TreeCtrlHandler):
    """
    Supports saving/restoring a :class:`lib.agw.hypertreelist.HyperTreeList` expansion state,
    selections, column widths and checked items state (meaningful only for :class:`~wx.lib.agw.hypertreelist.HyperTreeList`).

    This class handles the following wxPython widgets:

    - :class:`lib.agw.hypertreelist.HyperTreeList`.

    """

    def __init__(self, pObject):

        TreeCtrlHandler.__init__(self, pObject)


    def Save(self):

        treeList, obj = self._window, self._pObject

        colSizes = []
        for col in range(treeList.GetColumnCount()):
            colSizes.append(treeList.GetColumnWidth(col))

        obj.SaveValue(PERSIST_TREELISTCTRL_COLWIDTHS, colSizes)

        return TreeCtrlHandler.Save(self)


    def Restore(self):

        treeList, obj = self._window, self._pObject
        colSizes = obj.RestoreValue(PERSIST_TREELISTCTRL_COLWIDTHS)
        retVal = False

        count = treeList.GetColumnCount()
        if colSizes is not None:
            retVal = True
            for col, size in enumerate(colSizes):
                if col < count:
                    treeList.SetColumnWidth(col, size)

        return (retVal and TreeCtrlHandler.Restore(self))


    def GetKind(self):

        return PERSIST_TREELISTCTRL_KIND


# ----------------------------------------------------------------------------------- #

class CalendarCtrlHandler(AbstractHandler):
    """
    Supports saving/restoring a :class:`adv.CalendarCtrl` date.

    This class handles the following wxPython widgets:

    - :class:`adv.CalendarCtrl`.

    """

    def __init__(self, pObject):

        AbstractHandler.__init__(self, pObject)


    def Save(self):

        calend, obj = self._window, self._pObject
        obj.SaveCtrlValue(PERSIST_CALENDAR_DATE, wxDate2PyDate(calend.GetDate()))
        return True


    def Restore(self):

        calend, obj = self._window, self._pObject
        value = obj.RestoreCtrlValue(PERSIST_CALENDAR_DATE)

        if value is not None:
            calend.SetDate(PyDate2wxDate(value))
            return True

        return False


    def GetKind(self):

        return PERSIST_CALENDAR_KIND


# ----------------------------------------------------------------------------------- #

class CollapsiblePaneHandler(AbstractHandler):
    """
    Supports saving/restoring a :class:`CollapsiblePane` / :class:`lib.agw.pycollapsiblepane.PyCollapsiblePane` state.

    This class handles the following wxPython widgets:

    - :class:`CollapsiblePane`;
    - :class:`lib.agw.pycollapsiblepane.PyCollapsiblePane`.
    """

    def __init__(self, pObject):

        AbstractHandler.__init__(self, pObject)


    def Save(self):

        collPane, obj = self._window, self._pObject
        obj.SaveValue(PERSIST_COLLAPSIBLE_STATE, collPane.IsCollapsed())
        return True


    def Restore(self):

        collPane, obj = self._window, self._pObject
        value = obj.RestoreValue(PERSIST_COLLAPSIBLE_STATE)

        if value is not None:
            collPane.Collapse(value)
            return True

        return False


    def GetKind(self):

        return PERSIST_COLLAPSIBLE_KIND


# ----------------------------------------------------------------------------------- #

class DatePickerHandler(AbstractHandler):
    """
    Supports saving/restoring a :class:`adv.DatePickerCtrl` date.

    This class handles the following wxPython widgets:

    - :class:`~adv.DatePickerCtrl`.

    """

    def __init__(self, pObject):

        AbstractHandler.__init__(self, pObject)


    def Save(self):

        datePicker, obj = self._window, self._pObject
        obj.SaveCtrlValue(PERSIST_DATEPICKER_DATE, wxDate2PyDate(datePicker.GetValue()))
        return True


    def Restore(self):

        datePicker, obj = self._window, self._pObject
        value = obj.RestoreCtrlValue(PERSIST_DATEPICKER_DATE)

        if value is not None:
            datePicker.SetValue(PyDate2wxDate(value))
            return True

        return False


    def GetKind(self):

        return PERSIST_DATEPICKER_KIND


# ----------------------------------------------------------------------------------- #

class MediaCtrlHandler(AbstractHandler):
    """
    Supports saving/restoring a :class:`media.MediaCtrl` movie position, volume and playback
    rate.

    This class handles the following wxPython widgets:

    - :class:`media.MediaCtrl`.

    """

    def __init__(self, pObject):

        AbstractHandler.__init__(self, pObject)


    def Save(self):

        mediaCtrl, obj = self._window, self._pObject
        obj.SaveValue(PERSIST_MEDIA_POS, mediaCtrl.Tell())
        obj.SaveValue(PERSIST_MEDIA_VOLUME, mediaCtrl.GetVolume())
        obj.SaveValue(PERSIST_MEDIA_RATE, mediaCtrl.GetPlaybackRate())
        return True


    def Restore(self):

        mediaCtrl, obj = self._window, self._pObject
        position = obj.RestoreValue(PERSIST_MEDIA_POS)
        volume = obj.RestoreValue(PERSIST_MEDIA_VOLUME)
        rate = obj.RestoreValue(PERSIST_MEDIA_RATE)

        if position is not None:
            mediaCtrl.Seek(position)

        if volume is not None:
            mediaCtrl.SetVolume(volume)

        if rate is not None:
            mediaCtrl.SetPlaybackRate(rate)

        return (osition is not None and volume is not None and rate is not None)


    def GetKind(self):

        return PERSIST_MEDIA_KIND


# ----------------------------------------------------------------------------------- #

class ColourPickerHandler(AbstractHandler):
    """
    Supports saving/restoring a :class:`wx.ColourPickerCtrl` / :class:`lib.colourselect.ColourSelect` colour.

    This class handles the following wxPython widgets:

    - :class:`wx.ColourPickerCtrl`;
    - :class:`lib.colourselect.ColourSelect`.

    """

    def __init__(self, pObject):

        AbstractHandler.__init__(self, pObject)


    def Save(self):

        colPicker, obj = self._window, self._pObject
        obj.SaveValue(PERSIST_COLOURPICKER_COLOUR, colPicker.GetColour().Get(includeAlpha=True))
        return True


    def Restore(self):

        colPicker, obj = self._window, self._pObject
        value = obj.RestoreValue(PERSIST_COLOURPICKER_COLOUR)

        if value is not None:
            colPicker.SetColour(wx.Colour(*value))
            return True

        return False


    def GetKind(self):

        return PERSIST_COLOURPICKER_KIND


# ----------------------------------------------------------------------------------- #

class FileDirPickerHandler(AbstractHandler):
    """
    Supports saving/restoring a :class:`FilePickerCtrl` / :class:`DirPickerCtrl` path.

    This class handles the following wxPython widgets:

    - :class:`FilePickerCtrl`;
    - :class:`DirPickerCtrl`.

    """

    def __init__(self, pObject):

        AbstractHandler.__init__(self, pObject)


    def Save(self):

        picker, obj = self._window, self._pObject

        path = picker.GetPath()
        if issubclass(picker.__class__, wx.FileDialog):
            if picker.GetWindowStyleFlag() & wx.FD_MULTIPLE:
                path = picker.GetPaths()

        obj.SaveValue(PERSIST_FILEDIRPICKER_PATH, path)
        return True


    def Restore(self):

        picker, obj = self._window, self._pObject
        value = obj.RestoreValue(PERSIST_FILEDIRPICKER_PATH)

        if value is not None:
            if issubclass(picker.__class__, wx.FileDialog):
                if type(value) == list:
                    value = value[-1]

            picker.SetPath(value)
            return True

        return False


    def GetKind(self):

        return PERSIST_FILEDIRPICKER_KIND


# ----------------------------------------------------------------------------------- #

class FontPickerHandler(AbstractHandler):
    """
    Supports saving/restoring a :class:`wx.FontPickerCtrl` font.

    This class handles the following wxPython widgets:

    - :class:`wx.FontPickerCtrl`.

    """

    def __init__(self, pObject):

        AbstractHandler.__init__(self, pObject)


    def Save(self):

        picker, obj = self._window, self._pObject

        font = picker.GetSelectedFont()
        if not font.IsOk():
            return False

        fontData = CreateFont(font)
        obj.SaveValue(PERSIST_FONTPICKER_FONT, fontData)
        return True


    def Restore(self):

        picker, obj = self._window, self._pObject
        value = obj.RestoreValue(PERSIST_FONTPICKER_FONT)

        if value is not None:
            font = wx.Font(*value)
            if font.IsOk():
                picker.SetSelectedFont(font)
                return True

        return False


    def GetKind(self):

        return PERSIST_FONTPICKER_KIND


# ----------------------------------------------------------------------------------- #

class FileHistoryHandler(AbstractHandler):
    """
    Supports saving/restoring a :class:`FileHistory` list of file names.

    This class handles the following wxPython widgets:

    - :class:`FileHistory`.

    """

    def __init__(self, pObject):

        AbstractHandler.__init__(self, pObject)


    def Save(self):

        history, obj = self._window, self._pObject

        paths = []
        for indx in range(history.GetCount()):
            paths.append(history.GetHistoryFile(indx))

        obj.SaveValue(PERSIST_FILEHISTORY_PATHS, paths)
        return True


    def Restore(self):

        history, obj = self._window, self._pObject
        value = obj.RestoreValue(PERSIST_FILEHISTORY_PATHS)

        if value is not None:
            count = history.GetMaxFiles()
            for indx, path in enumerate(value):
                if indx < count:
                    history.AddFileToHistory(path)
            return True

        return False


    def GetKind(self):

        return PERSIST_FILEHISTORY_KIND


# ----------------------------------------------------------------------------------- #

class MenuBarHandler(AbstractHandler):
    """
    Supports saving/restoring the :class:`wx.MenuBar` and :class:`lib.agw.flatmenu.FlatMenuBar` items state.

    This class handles the following wxPython widgets:

    - :class:`wx.MenuBar`;
    - :class:`lib.agw.flatmenu.FlatMenuBar`.

    """

    def __init__(self, pObject):

        AbstractHandler.__init__(self, pObject)


    def Save(self):

        bar, obj = self._window, self._pObject
        menuCount = bar.GetMenuCount()

        if menuCount == 0:
            # Nothing to save
            return False

        checkRadioItems = {}
        for indx in range(menuCount):
            menu = bar.GetMenu(indx)
            for item in menu.GetMenuItems():
                if item.GetKind() in [wx.ITEM_CHECK, wx.ITEM_RADIO]:
                    checkRadioItems[item.GetId()] = item.IsChecked()

        obj.SaveValue(PERSIST_MENUBAR_CHECKRADIO_ITEMS, checkRadioItems)
        return True


    def Restore(self):

        bar, obj = self._window, self._pObject
        menuCount = bar.GetMenuCount()

        if menuCount == 0:
            # Nothing to restore
            return False

        checkRadioItems = obj.RestoreValue(PERSIST_MENUBAR_CHECKRADIO_ITEMS)

        if checkRadioItems is None:
            return False

        retVal = True
        for indx in range(menuCount):
            menu = bar.GetMenu(indx)
            for item in menu.GetMenuItems():
                if item.GetKind() in [wx.ITEM_CHECK, wx.ITEM_RADIO]:
                    itemId = item.GetId()
                    if itemId in checkRadioItems:
                        item.Check(checkRadioItems[itemId])
                    else:
                        retVal = False

        return retVal


    def GetKind(self):

        return PERSIST_MENUBAR_KIND


# ----------------------------------------------------------------------------------- #

class ToolBarHandler(AbstractHandler):
    """
    Supports saving/restoring the :class:`lib.agw.aui.auibar.AuiToolBar` items state.

    This class handles the following wxPython widgets:

    - :class:`lib.agw.aui.auibar.AuiToolBar`.

    .. todo::

       Find a way to handle :class:`ToolBar` UI settings as it has been done for
       :class:`lib.agw.aui.auibar.AuiToolBar`: currently :class:`ToolBar` doesn't seem
       to have easy access to the underlying toolbar tools.

    """

    def __init__(self, pObject):

        AbstractHandler.__init__(self, pObject)


    def Save(self):

        bar, obj = self._window, self._pObject
        toolCount = bar.GetToolCount()

        if toolCount == 0:
            # Nothing to save
            return False

        checkRadioItems = {}
        for indx in range(toolCount):
            tool = bar.FindToolByIndex(indx)
            if tool is not None:
                if tool.GetKind() in [AUI.ITEM_CHECK, AUI.ITEM_RADIO]:
                    checkRadioItems[tool.GetId()] = tool.GetState() & AUI.AUI_BUTTON_STATE_CHECKED

        obj.SaveValue(PERSIST_TOOLBAR_CHECKRADIO_ITEMS, checkRadioItems)
        return True


    def Restore(self):

        bar, obj = self._window, self._pObject
        toolCount = bar.GetToolCount()

        if toolCount == 0:
            # Nothing to save
            return False

        checkRadioItems = obj.RestoreValue(PERSIST_TOOLBAR_CHECKRADIO_ITEMS)

        if checkRadioItems is None:
            return False

        for indx in range(toolCount):
            tool = bar.FindToolByIndex(indx)
            if tool is not None:
                toolId = tool.GetId()
                if toolId in checkRadioItems:
                    if tool.GetKind() in [AUI.ITEM_CHECK, AUI.ITEM_RADIO]:
                        state = checkRadioItems[toolId]
                        if state & AUI.AUI_BUTTON_STATE_CHECKED:
                            tool.SetState(tool.GetState() | AUI.AUI_BUTTON_STATE_CHECKED)
                        else:
                            tool.SetState(tool.GetState() & ~AUI.AUI_BUTTON_STATE_CHECKED)

        return True


    def GetKind(self):

        return PERSIST_TOOLBAR_KIND

# ----------------------------------------------------------------------------------- #

class FileDirDialogHandler(TLWHandler, FileDirPickerHandler):
    """
    Supports saving/restoring a :class:`DirDialog` / :class:`FileDialog` path.

    This class handles the following wxPython widgets:

    - :class:`DirDialog`;
    - :class:`FileDialog`.
    """

    def __init__(self, pObject):

        TLWHandler.__init__(self, pObject)
        FileDirPickerHandler.__init__(self, pObject)


    def Save(self):

        tlw = TLWHandler.Save(self)
        fdp = FileDirPickerHandler.Save(self)

        return (tlw and fdp)


    def Restore(self):

        tlw = TLWHandler.Restore(self)
        fdp = FileDirPickerHandler.Restore(self)
        return (tlw and fdp)


    def GetKind(self):

        return PERSIST_FILEDIRPICKER_KIND


# ----------------------------------------------------------------------------------- #

class FindReplaceHandler(TLWHandler):
    """
    Supports saving/restoring a :class:`FindReplaceDialog` data (search string, replace string
    and flags).

    This class handles the following wxPython widgets:

    - :class:`FindReplaceDialog`.

    .. todo:: Find a way to properly save and restore dialog data (:class:`wx.ColourDialog`, :class:`wx.FontDialog` etc...).

    """

    def __init__(self, pObject):

        TLWHandler.__init__(self, pObject)


    def Save(self):

        findDialog, obj = self._window, self._pObject
        data = findDialog.GetData()

        obj.SaveValue(PERSIST_FINDREPLACE_FLAGS, data.GetFlags())
        obj.SaveValue(PERSIST_FINDREPLACE_SEARCH, data.GetFindString())
        obj.SaveValue(PERSIST_FINDREPLACE_REPLACE, data.GetReplaceString())

        return TLWHandler.Save(self)


    def Restore(self):

        findDialog, obj = self._window, self._pObject

        flags = obj.RestoreValue(PERSIST_FINDREPLACE_FLAGS)
        search = obj.RestoreValue(PERSIST_FINDREPLACE_SEARCH)
        replace = obj.RestoreValue(PERSIST_FINDREPLACE_REPLACE)

        data = findDialog.GetData()
        if flags is not None:
            data.SetFlags(flags)
        if search is not None:
            data.SetFindString(search)
        if replace is not None:
            data.SetReplaceString(replace)

        retVal = TLWHandler.Restore(self)

        return (flags is not None and search is not None and replace is not None and retVal)


    def GetKind(self):

        return PERSIST_FINDREPLACE_KIND


# ----------------------------------------------------------------------------------- #

class FontDialogHandler(TLWHandler):
    """
    Supports saving/restoring a :class:`wx.FontDialog` data (effects, symbols, colour, font, help).

    This class handles the following wxPython widgets:

    - :class:`wx.FontDialog`.

    .. todo:: Find a way to properly save and restore dialog data (:class:`wx.ColourDialog`, :class:`wx.FontDialog` etc...).

    """

    def __init__(self, pObject):

        TLWHandler.__init__(self, pObject)


    def Save(self):

        fontDialog, obj = self._window, self._pObject
        data = fontDialog.GetFontData()

        obj.SaveValue(PERSIST_FONTDIALOG_EFFECTS, data.GetEnableEffects())
        obj.SaveValue(PERSIST_FONTDIALOG_SYMBOLS, data.GetAllowSymbols())
        obj.SaveValue(PERSIST_FONTDIALOG_COLOUR, data.GetColour().Get(includeAlpha=True))
        obj.SaveValue(PERSIST_FONTDIALOG_FONT, CreateFont(data.GetChosenFont()))
        obj.SaveValue(PERSIST_FONTDIALOG_HELP, data.GetShowHelp())

        return TLWHandler.Save(self)


    def Restore(self):

        fontDialog, obj = self._window, self._pObject
        data = fontDialog.GetFontData()

        effects = obj.RestoreValue(PERSIST_FONTDIALOG_EFFECTS)
        symbols = obj.RestoreValue(PERSIST_FONTDIALOG_SYMBOLS)
        colour = obj.RestoreValue(PERSIST_FONTDIALOG_COLOUR)
        font = obj.RestoreValue(PERSIST_FONTDIALOG_FONT)
        help = obj.RestoreValue(PERSIST_FONTDIALOG_HELP)

        if effects is not None:
            data.EnableEffects(effects)
        if symbols is not None:
            data.SetAllowSymbols(symbols)
        if colour is not None:
            data.SetColour(wx.Colour(*colour))
        if font is not None:
            data.SetInitialFont(wx.Font(*font))
        if help is not None:
            data.SetShowHelp(help)

        return (effects is not None and symbols is not None and colour is not None and \
                font is not None and help is not None and TLWHandler.Restore(self))


    def GetKind(self):

        return PERSIST_FONTDIALOG_KIND


# ----------------------------------------------------------------------------------- #

class ColourDialogHandler(TLWHandler):
    """
    Supports saving/restoring a :class:`wx.ColourDialog` data (colour, custom colours and full
    choice in the dialog).

    This class handles the following wxPython widgets:

    - :class:`wx.ColourDialog`;
    - :class:`lib.agw.cubecolourdialog.CubeColourDialog`.

    .. todo:: Find a way to properly save and restore dialog data (:class:`wx.ColourDialog`, :class:`wx.FontDialog` etc...).

    """

    def __init__(self, pObject):

        TLWHandler.__init__(self, pObject)


    def Save(self):

        colDialog, obj = self._window, self._pObject
        data = colDialog.GetColourData()

        obj.SaveValue(PERSIST_COLOURDIALOG_COLOUR, data.GetColour().Get(includeAlpha=True))
        obj.SaveValue(PERSIST_COLOURDIALOG_CHOOSEFULL, data.GetChooseFull())

        customColours = []
        for indx in range(15):
            colour = data.GetCustomColour(indx)
            if not colour.IsOk() or colour == wx.WHITE:
                break

            customColours.append(colour.Get(includeAlpha=True))

        obj.SaveValue(PERSIST_COLOURDIALOG_CUSTOMCOLOURS, customColours)

        return TLWHandler.Save(self)


    def Restore(self):

        colDialog, obj = self._window, self._pObject
        data = colDialog.GetColourData()

        colour = obj.RestoreValue(PERSIST_COLOURDIALOG_COLOUR)
        chooseFull = obj.RestoreValue(PERSIST_COLOURDIALOG_CHOOSEFULL)
        customColours = obj.RestoreValue(PERSIST_COLOURDIALOG_CUSTOMCOLOURS)

        if colour is not None:
            data.SetColour(wx.Colour(*colour))
        if chooseFull is not None:
            data.SetChooseFull(chooseFull)
        if customColours is not None:
            for indx, colour in enumerate(customColours):
                data.SetCustomColour(indx, colour)

        return (colour is not None and chooseFull is not None and customColours is not None \
                and TLWHandler.Restore(self))


    def GetKind(self):

        return PERSIST_COLOURDIALOG_KIND


# ----------------------------------------------------------------------------------- #

class ChoiceDialogHandler(TLWHandler):
    """
    Supports saving/restoring a :class:`MultiChoiceDialog` / :class:`SingleChoiceDialog` choices.

    This class handles the following wxPython widgets:

    - :class:`SingleChoiceDialog`;
    - :class:`MultiChoiceDialog`.
    """

    def __init__(self, pObject):

        TLWHandler.__init__(self, pObject)


    def Save(self):

        dialog, obj = self._window, self._pObject

        if issubclass(dialog.__class__, wx.SingleChoiceDialog):
            selections = dialog.GetSelection()
            selections = (selections >= 0 and [selections] or [[]])[0]
        else:
            selections = dialog.GetSelections()

        obj.SaveValue(PERSIST_CHOICEDIALOG_SELECTIONS, selections)
        return True


    def Restore(self):

        dialog, obj = self._window, self._pObject
        selections = obj.RestoreValue(PERSIST_CHOICEDIALOG_SELECTIONS)

        if selections is None:
            return False

        if issubclass(dialog.__class__, wx.SingleChoiceDialog):
            if selections:
                dialog.SetSelection(selections[-1])
        else:
            dialog.SetSelections(selections)

        return True


    def GetKind(self):

        return PERSIST_CHOICEDIALOG_KIND


# ----------------------------------------------------------------------------------- #

class TextEntryHandler(TLWHandler, TextCtrlHandler):
    """
    Supports saving/restoring a :class:`TextEntryDialog` string.

    This class handles the following wxPython widgets:

    - :class:`TextEntryDialog`;
    - :class:`PasswordEntryDialog`.
    """

    def __init__(self, pObject):

        TLWHandler.__init__(self, pObject)
        TextCtrlHandler.__init__(self, pObject)


    def Save(self):

        tlw = TLWHandler.Save(self)
        txt = TextCtrlHandler.Save(self)
        return (tlw and txt)


    def Restore(self):

        tlw = TLWHandler.Restore(self)
        txt = TextCtrlHandler.Restore(self)
        return (tlw and txt)


    def GetKind(self):

        return PERSIST_TLW_KIND


# ----------------------------------------------------------------------------------- #


HANDLERS = [
    ("BookHandler", (wx.BookCtrlBase, AUI.AuiNotebook, FNB.FlatNotebook,
                    LBK.LabelBook, LBK.FlatImageBook)),
    ("TLWHandler", (wx.TopLevelWindow, )),
    ("CheckBoxHandler", (wx.CheckBox, )),
    ("TreeCtrlHandler", (wx.TreeCtrl, wx.GenericDirCtrl, CT.CustomTreeCtrl, dv.TreeListCtrl)),
    ("MenuBarHandler", (wx.MenuBar, FM.FlatMenuBar)),
    ("ToolBarHandler", (AUI.AuiToolBar, )),
    ("ListBoxHandler", (wx.ListBox, wx.VListBox, wx.html.HtmlListBox, wx.html.SimpleHtmlListBox,
                        wx.adv.EditableListBox)),
    ("ListCtrlHandler", (wx.ListCtrl, wx.ListView)),  #ULC.UltimateListCtrl (later)
    ("ChoiceComboHandler", (wx.Choice, wx.ComboBox, wx.adv.OwnerDrawnComboBox)),
    ("RadioBoxHandler", (wx.RadioBox, )),
    ("RadioButtonHandler", (wx.RadioButton, )),
    ("ScrolledWindowHandler", (wx.ScrolledWindow, scrolled.ScrolledPanel)),
    ("SliderHandler", (wx.Slider, KC.KnobCtrl)),
    ("SpinHandler", (wx.SpinButton, wx.SpinCtrl, FS.FloatSpin)),
    ("SplitterHandler", (wx.SplitterWindow, )),
    ("TextCtrlHandler", (wx.TextCtrl, wx.SearchCtrl, expando.ExpandoTextCtrl, masked.TextCtrl,
                        masked.ComboBox, masked.IpAddrCtrl, masked.TimeCtrl, masked.NumCtrl)),
    ("TreeListCtrlHandler", (HTL.HyperTreeList, )),
    ("CalendarCtrlHandler", (wx.adv.CalendarCtrl, )),
    ("CollapsiblePaneHandler", (wx.CollapsiblePane, PCP.PyCollapsiblePane)),
    ("AUIHandler", (wx.Panel, )),
    ("DatePickerHandler", (wx.adv.DatePickerCtrl, )),
#    ("MediaCtrlHandler", (wx.media.MediaCtrl, )), not wrapped yet
    ("ColourPickerHandler", (wx.ColourPickerCtrl, csel.ColourSelect)),
    ("FileDirPickerHandler", (wx.FilePickerCtrl, wx.DirPickerCtrl)),
    ("FontPickerHandler", (wx.FontPickerCtrl, )),
    ("FileHistoryHandler", (wx.FileHistory, )),
    ("ToggleButtonHandler", (wx.ToggleButton, buttons.GenToggleButton,
                            buttons.GenBitmapToggleButton, buttons.GenBitmapTextToggleButton)),
    ]

STANDALONE_HANDLERS = [
    ("TreebookHandler", (wx.Treebook, )),
    ("CheckListBoxHandler", (wx.CheckListBox, )),
    ("FileDirDialogHandler", (wx.DirDialog, wx.FileDialog)),
    ("FindReplaceHandler", (wx.FindReplaceDialog, )),
    ("FontDialogHandler", (wx.FontDialog, )),
    ("ColourDialogHandler", (wx.ColourDialog, CCD.CubeColourDialog)),
    ("ChoiceDialogHandler", (wx.SingleChoiceDialog, wx.MultiChoiceDialog)),
    ("TextEntryHandler", (wx.TextEntryDialog, wx.PasswordEntryDialog)),
    ]

if hasSB:
    HANDLERS[-1] = ("ToggleButtonHandler", (wx.ToggleButton, buttons.GenToggleButton,
                                            buttons.GenBitmapToggleButton,
                                            buttons.GenBitmapTextToggleButton,
                                            SB.SToggleButton, SB.SBitmapToggleButton,
                                            SB.SBitmapTextToggleButton))

# ----------------------------------------------------------------------------------- #

def FindHandler(pObject):
    """
    Finds a suitable handler for the input `Persistent Object` depending on the
    widget kind.

    :param `pObject`: an instance of :class:`~wx.lib.agw.persist.persistencemanager.PersistentObject` class.
    """

    window = pObject.GetWindow()
    klass = window.__class__

    if hasattr(window, "_persistentHandler"):
        # if control has a handler, just return it
        return window._persistentHandler

    for handler, subclasses in STANDALONE_HANDLERS:
        for subclass in subclasses:
            if issubclass(klass, subclass):
                return eval(handler)(pObject)

    for handler, subclasses in HANDLERS:
        for subclass in subclasses:
            if issubclass(klass, subclass):
                return eval(handler)(pObject)

    raise Exception("Unsupported persistent handler (class=%s, name=%s)"%(klass, window.GetName()))

# ----------------------------------------------------------------------------------- #

def HasCtrlHandler(control):
    """
    Is there a suitable handler for this control

    :param `control`: the control instance to check if a handler for it exists.
    """

    klass = control.__class__

    if hasattr(control, "_persistentHandler"):
        # if control has a handler, just return it
        return True

    for handler, subclasses in STANDALONE_HANDLERS:
        for subclass in subclasses:
            if issubclass(klass, subclass):
                return True

    for handler, subclasses in HANDLERS:
        for subclass in subclasses:
            if issubclass(klass, subclass):
                return True

    return False
