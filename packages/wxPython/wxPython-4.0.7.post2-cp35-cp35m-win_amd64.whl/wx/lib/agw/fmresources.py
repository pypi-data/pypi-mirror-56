import wx

# Overall menu styles
StyleDefault = 0
StyleXP      = 1
Style2007    = 2
StyleVista   = 3

# Menu shadows
RightShadow             = 1 # Right side shadow
BottomShadow            = 2 # Not full bottom shadow
BottomShadowFull        = 4 # Full bottom shadow

# Button styles
BU_EXT_XP_STYLE = 1
BU_EXT_2007_STYLE = 2
BU_EXT_LEFT_ALIGN_STYLE = 4
BU_EXT_CENTER_ALIGN_STYLE = 8
BU_EXT_RIGHT_ALIGN_STYLE = 16
BU_EXT_RIGHT_TO_LEFT_STYLE = 32

# Control state
ControlPressed = 0
ControlFocus = 1
ControlDisabled = 2
ControlNormal = 3

# FlatMenu styles
FM_OPT_IS_LCD = 1
""" Use this style if your computer uses a LCD screen. """
FM_OPT_MINIBAR = 2
""" Use this if you plan to use the toolbar only. """
FM_OPT_SHOW_CUSTOMIZE = 4
""" Show "customize link" in the `More` menu, you will need to write your own handler. See demo. """
FM_OPT_SHOW_TOOLBAR = 8
""" Set this option is you are planning to use the toolbar. """

# Control status
ControlStatusNoFocus = 0
ControlStatusFocus = 1
ControlStatusPressed = 2

# HitTest constants
NoWhere = 0
MenuItem = 1
ToolbarItem = 2
DropDownArrowButton = 3

FTB_ITEM_TOOL = 0
FTB_ITEM_SEPARATOR = 1
FTB_ITEM_CHECK = 2
FTB_ITEM_RADIO = 3

FTB_ITEM_RADIO_MENU = 4
FTB_ITEM_CUSTOM = 5

LargeIcons = 32
SmallIcons = 16

MENU_HT_NONE = 0
MENU_HT_ITEM = 1
MENU_HT_SCROLL_UP = 2
MENU_HT_SCROLL_DOWN = 3

MENU_DEC_TOP = 0
MENU_DEC_BOTTOM = 1
MENU_DEC_LEFT = 2
MENU_DEC_RIGHT = 3

DROP_DOWN_ARROW_WIDTH = 16
SPACER = 12
MARGIN = 3
TOOLBAR_SPACER = 4
TOOLBAR_MARGIN = 4
SEPARATOR_WIDTH = 12
SCROLL_BTN_HEIGHT = 20

CS_DROPSHADOW = 0x00020000

INB_BOTTOM = 1
INB_LEFT = 2
INB_RIGHT = 4
INB_TOP = 8
INB_BORDER = 16
INB_SHOW_ONLY_TEXT = 32
INB_SHOW_ONLY_IMAGES = 64
INB_FIT_BUTTON = 128
INB_DRAW_SHADOW = 256
INB_USE_PIN_BUTTON = 512
INB_GRADIENT_BACKGROUND = 1024
INB_WEB_HILITE = 2048
INB_NO_RESIZE = 4096
INB_FIT_LABELTEXT = 8192
INB_BOLD_TAB_SELECTION = 16384

INB_DEFAULT_STYLE = INB_BORDER | INB_TOP | INB_USE_PIN_BUTTON

INB_TAB_AREA_BACKGROUND_COLOUR = 100
INB_ACTIVE_TAB_COLOUR = 101
INB_TABS_BORDER_COLOUR = 102
INB_TEXT_COLOUR = 103
INB_ACTIVE_TEXT_COLOUR = 104
INB_HILITE_TAB_COLOUR = 105

INB_LABEL_BOOK_DEFAULT = INB_DRAW_SHADOW | INB_BORDER | INB_USE_PIN_BUTTON | INB_LEFT

# HitTest results
IMG_OVER_IMG = 0
IMG_OVER_PIN = 1
IMG_OVER_EW_BORDER = 2
IMG_NONE = 3

# Pin button states
INB_PIN_NONE = 0
INB_PIN_HOVER = 200
INB_PIN_PRESSED = 201

# Windows Vista Colours
rgbSelectOuter = wx.Colour(170, 200, 245)
rgbSelectInner = wx.Colour(230, 250, 250)
rgbSelectTop = wx.Colour(210, 240, 250)
rgbSelectBottom = wx.Colour(185, 215, 250)

check_mark_xpm = [b"    16    16       16            1",
                  b"` c #000000",
                  b". c #800000",
                  b"# c #008000",
                  b"a c #808000",
                  b"b c #000080",
                  b"c c #800080",
                  b"d c #008080",
                  b"e c #808080",
                  b"f c #c0c0c0",
                  b"g c #ff0000",
                  b"h c #00ff00",
                  b"i c #ffff00",
                  b"j c #0000ff",
                  b"k c #ff00ff",
                  b"l c #00ffff",
                  b"m c #ffffff",
                  b"mmmmmmmmmmmmmmmm",
                  b"mmmmmmmmmmmmmmmm",
                  b"mmmmmmmmmmmmmmmm",
                  b"mmmmmmmmmmmmmmmm",
                  b"mmmmmmmmmmmmmmmm",
                  b"mmmmmmmmmm`mmmmm",
                  b"mmmmmmmmm``mmmmm",
                  b"mmmm`mmm```mmmmm",
                  b"mmmm``m```mmmmmm",
                  b"mmmm`````mmmmmmm",
                  b"mmmmm```mmmmmmmm",
                  b"mmmmmm`mmmmmmmmm",
                  b"mmmmmmmmmmmmmmmm",
                  b"mmmmmmmmmmmmmmmm",
                  b"mmmmmmmmmmmmmmmm",
                  b"mmmmmmmmmmmmmmmm"
                  ]

radio_item_xpm = [b"    16    16       16            1",
                  b"` c #000000",
                  b". c #800000",
                  b"# c #008000",
                  b"a c #808000",
                  b"b c #000080",
                  b"c c #800080",
                  b"d c #008080",
                  b"e c #808080",
                  b"f c #c0c0c0",
                  b"g c #ff0000",
                  b"h c #00ff00",
                  b"i c #ffff00",
                  b"j c #0000ff",
                  b"k c #ff00ff",
                  b"l c #00ffff",
                  b"m c #ffffff",
                  b"mmmmmmmmmmmmmmmm",
                  b"mmmmmmmmmmmmmmmm",
                  b"mmmmmmmmmmmmmmmm",
                  b"mmmmmmmmmmmmmmmm",
                  b"mmmmmmmmmmmmmmmm",
                  b"mmmmmmmmmmmmmmmm",
                  b"mmmmmm```mmmmmmm",
                  b"mmmmm`````mmmmmm",
                  b"mmmmm`````mmmmmm",
                  b"mmmmmm```mmmmmmm",
                  b"mmmmmmmmmmmmmmmm",
                  b"mmmmmmmmmmmmmmmm",
                  b"mmmmmmmmmmmmmmmm",
                  b"mmmmmmmmmmmmmmmm",
                  b"mmmmmmmmmmmmmmmm",
                  b"mmmmmmmmmmmmmmmm"]


menu_right_arrow_xpm = [
    b"    16    16        8            1",
    b"` c #ffffff",
    b". c #000000",
    b"# c #000000",
    b"a c #000000",
    b"b c #000000",
    b"c c #000000",
    b"d c #000000",
    b"e c #000000",
    b"````````````````",
    b"````````````````",
    b"````````````````",
    b"````````````````",
    b"````````````````",
    b"``````.`````````",
    b"``````..````````",
    b"``````...```````",
    b"``````....``````",
    b"``````...```````",
    b"``````..````````",
    b"``````.`````````",
    b"````````````````",
    b"````````````````",
    b"````````````````",
    b"````````````````"
    ]

#----------------------------------
# Shadow images
#----------------------------------

shadow_right_xpm = [b"5 5 1 1", b"  c Black", b"     ", b"     ", b"     ", b"     ", b"     "]

# shadow_right.xpm 5x5
shadow_right_alpha = [168, 145, 115,  76,  46, 168, 145, 115,  76,  46, 168, 145, 115,  76,  46,
                      168, 145, 115,  76,  46, 168, 145, 115,  76,  46]

shadow_right_top_xpm = [b"5 10 1 1", b"  c Black", b"     ", b"     ", b"     ", b"     ",
                        b"     ", b"     ", b"     ", b"     ", b"     ", b"     "]

shadow_right_top_alpha = [40,  35,  28,  18,  11, 67,  58,  46,  31,  18, 101,  87,  69,  46,  28,
                          128, 110,  87,  58,  35, 148, 128, 101,  67,  40, 161, 139, 110,  73,  44,
                          168, 145, 115,  76,  46, 168, 145, 115,  76,  46, 168, 145, 115,  76,  46,
                          168, 145, 115,  76,  46]

# shadow_bottom.xpm 5x5
shadow_bottom_alpha = [184, 184, 184, 184, 184, 168, 168, 168, 168, 168, 145, 145, 145, 145, 145,
                       115, 115, 115, 115, 115, 76,  76,  76,  76,  76]

shadow_bottom_left_xpm = [b"10 5 1 1", b"  c Black", b"          ", b"          ",
                          b"          ", b"          ", b"          "]

shadow_bottom_left_alpha = [22,  44,  73, 110, 139, 161, 176, 184, 184, 184,
                            20,  40,  67, 101, 128, 148, 161, 168, 168, 168,
                            17,  35,  58,  87, 110, 128, 139, 145, 145, 145,
                            13,  28,  46,  69,  87, 101, 110, 115, 115, 115,
                            9,  18,  31,  46,  58,  67,  73,  76,  76,  76]

shadow_center_xpm = [b"5 5 1 1", b"  c Black", b"     ", b"     ", b"     ", b"     ", b"     "]

shadow_center_alpha = [161, 139, 110,  73,  44, 148, 128, 101,  67,  40,
                       128, 110,  87,  58,  35, 101,  87,  69,  46,  28,
                       67,  58,  46,  31,  18]

shadow_bottom_xpm = [b"5 5 1 1", b"  c Black", b"     ", b"     ", b"     ", b"     ", b"     "]

arrow_down_xpm = [b"16 16 3 1",
                  b". c Black",
                  b"X c #FFFFFF",
                  b"  c #008080",
                  b"                ",
                  b"                ",
                  b"                ",
                  b"                ",
                  b"    .......     ",
                  b"    XXXXXXX     ",
                  b"                ",
                  b"    .......     ",
                  b"    X.....X     ",
                  b"     X...X      ",
                  b"      X.X       ",
                  b"       X        ",
                  b"                ",
                  b"                ",
                  b"                ",
                  b"                "]

#---------------------------------------------
# Pin images
#---------------------------------------------
pin_left_xpm = [b"    16    16        8            1",
                b"` c #ffffff",
                b". c #000000",
                b"# c #808080",
                b"a c #000000",
                b"b c #000000",
                b"c c #000000",
                b"d c #000000",
                b"e c #000000",
                b"````````````````",
                b"````````````````",
                b"```````.````````",
                b"```````.````````",
                b"```````.......``",
                b"```````.`````.``",
                b"`````...`````.``",
                b"``......#####.``",
                b"`````...#####.``",
                b"```````.......``",
                b"```````.......``",
                b"```````.````````",
                b"```````.````````",
                b"````````````````",
                b"````````````````",
                b"````````````````"]

pin_down_xpm = [b"    16    16        8            1",
                b"` c #ffffff",
                b". c #000000",
                b"# c #808080",
                b"a c #000000",
                b"b c #000000",
                b"c c #000000",
                b"d c #000000",
                b"e c #000000",
                b"````````````````",
                b"````````````````",
                b"````.......`````",
                b"````.``##..`````",
                b"````.``##..`````",
                b"````.``##..`````",
                b"````.``##..`````",
                b"````.``##..`````",
                b"``...........```",
                b"``````...```````",
                b"``````...```````",
                b"```````.````````",
                b"```````.````````",
                b"```````.````````",
                b"````````````````",
                b"````````````````"]


arrow_up = b'BM\xf6\x00\x00\x00\x00\x00\x00\x00v\x00\x00\x00(\x00\x00\x00\x10\x00\x00\
\x00\x10\x00\x00\x00\x01\x00\x04\x00\x00\x00\x00\x00\x80\x00\x00\x00\x12\x0b\x00\x00\x12\
\x0b\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\x00\x80\x80\x00\
\x00w\xfcM\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00""""""""""""""""""""""""""""""""""\x00\x00\x00\x02""""\x11\x11\
\x11\x12""""""""""""\x00\x00\x00\x02""""\x10\x00\x00\x12""""!\x00\x01""""""\x10\x12""""""!\
""""""""""""""""""""""""""""""""""""'


arrow_down = b'BM\xf6\x00\x00\x00\x00\x00\x00\x00v\x00\x00\x00(\x00\x00\x00\x10\x00\x00\x00\
\x10\x00\x00\x00\x01\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x12\x0b\x00\x00\x12\x0b\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\x00\x80\x80\x00\x00w\
\xfcM\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00"""""""""""""""""""""""""""""""""""!"""""""\x10\x12"""""!\x00\x01\
"""""\x10\x00\x00\x12""""\x00\x00\x00\x02""""""""""""\x11\x11\x11\x12""""\x00\x00\x00\x02\
""""""""""""""""""""""""""""""""""'

menu_up_arrow_xpm = [b"16 16 2 1",
                  b". c Black",
                  b"  c White",
                  b"                ",
                  b"                ",
                  b"                ",
                  b"                ",
                  b"                ",
                  b"                ",
                  b"       .        ",
                  b"      ...       ",
                  b"     .....      ",
                  b"                ",
                  b"                ",
                  b"                ",
                  b"                ",
                  b"                ",
                  b"                ",
                  b"                "]


menu_down_arrow_xpm = [b"16 16 2 1",
                  b". c Black",
                  b"  c White",
                  b"                ",
                  b"                ",
                  b"                ",
                  b"                ",
                  b"                ",
                  b"                ",
                  b"     .....      ",
                  b"      ...       ",
                  b"       .        ",
                  b"                ",
                  b"                ",
                  b"                ",
                  b"                ",
                  b"                ",
                  b"                ",
                  b"                "]


def getMenuUpArrowBitmap():
    bmp = wx.Bitmap(menu_up_arrow_xpm)
    bmp.SetMask(wx.Mask(bmp, wx.WHITE))
    return bmp

def getMenuDownArrowBitmap():
    bmp = wx.Bitmap(menu_down_arrow_xpm)
    bmp.SetMask(wx.Mask(bmp, wx.WHITE))
    return bmp
