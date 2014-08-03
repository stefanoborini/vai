import os

import logging
import curses

class FocusPolicy:
    NoFocus = 0
    StrongFocus = 11

class Orientation:
    Horizontal = 1
    Vertical = 2

class LineStyle:
    NoLine = 0
    Full   = 1

class CornerCapStyle:
    NoCap = 0
    Plus = 1

class LineCapStyle:
    NoCap = 0
    Plus  = 1

class Alignment:
    AlignLeft    =  0x1
    AlignRight   =  0x2
    AlignHCenter =  0x4
    AlignTop     = 0x20
    AlignBottom  = 0x40
    AlignVCenter = 0x80
    AlignCenter  = AlignHCenter|AlignVCenter

class Key:
    Key_Escape    = 0x01000000
    Key_Tab       = 0x01000001
    Key_Backtab   = 0x01000002
    Key_Backspace = 0x01000003
    Key_Return    = 0x01000004
    Key_Enter     = 0x01000005
    Key_Insert    = 0x01000006
    Key_Delete    = 0x01000007
    Key_Pause     = 0x01000008
    Key_Print     = 0x01000009
    Key_SysReq    = 0x0100000a
    Key_Clear     = 0x0100000b
    Key_Home      = 0x01000010
    Key_End       = 0x01000011
    Key_Left      = 0x01000012
    Key_Up        =  0x01000013
    Key_Right     =  0x01000014
    Key_Down      =  0x01000015
    Key_PageUp    =  0x01000016
    Key_PageDown  =  0x01000017
    Key_Shift     =  0x01000020
    Key_Control   =0x01000021
    Key_Meta      =0x01000022
    Key_Alt       =0x01000023
    Key_AltGr     =0x01001103
    Key_CapsLock  =   0x01000024
    Key_NumLock   =0x01000025
    Key_ScrollLock=  0x01000026
    Key_F1        =0x01000030
    Key_F2        =0x01000031
    Key_F3        = 0x01000032
    Key_F4        = 0x01000033
    Key_F5        = 0x01000034
    Key_F6        = 0x01000035
    Key_F7        = 0x01000036
    Key_F8        = 0x01000037
    Key_F9        = 0x01000038
    Key_F10       = 0x01000039
    Key_F11       = 0x0100003a
    Key_F12       = 0x0100003b
    Key_F13       = 0x0100003c
    Key_F14       = 0x0100003d
    Key_F15       = 0x0100003e
    Key_F16       = 0x0100003f
    Key_F17       = 0x01000040
    Key_F18       = 0x01000041
    Key_F19       = 0x01000042
    Key_F20       = 0x01000043
    Key_F21       = 0x01000044
    Key_F22       = 0x01000045
    Key_F23       = 0x01000046
    Key_F24       = 0x01000047
    Key_F25       = 0x01000048
    Key_F26       = 0x01000049
    Key_F27       = 0x0100004a
    Key_F28       = 0x0100004b
    Key_F29       = 0x0100004c
    Key_F30       = 0x0100004d
    Key_F31       = 0x0100004e
    Key_F32       = 0x0100004f
    Key_F33       = 0x01000050
    Key_F34       = 0x01000051
    Key_F35       = 0x01000052
    Key_Super_L   =0x01000053
    Key_Super_R   =0x01000054
    Key_Menu      =0x01000055
    Key_Hyper_L   =0x01000056
    Key_Hyper_R   =0x01000057
    Key_Help      =0x01000058
    Key_Direction_L =0x01000059
    Key_Direction_R =0x01000060
    Key_Space     =0x20
    Key_Any       = Key_Space
    Key_Exclam    = 0x21
    Key_QuoteDbl  =    0x22
    Key_NumberSign = 0x23
    Key_Dollar     =0x24
    Key_Percent    =0x25
    Key_Ampersand  = 0x26
    Key_Apostrophe = 0x27
    Key_ParenLeft  = 0x28
    Key_ParenRight = 0x29
    Key_Asterisk   = 0x2a
    Key_Plus       =0x2b
    Key_Comma      =0x2c
    Key_Minus      =0x2d
    Key_Period     =0x2e
    Key_Slash      =0x2f
    Key_0          =0x30
    Key_1          =0x31
    Key_2          =0x32
    Key_3          =0x33
    Key_4          =0x34
    Key_5          =0x35
    Key_6          =0x36
    Key_7          =0x37
    Key_8          =0x38
    Key_9          =0x39
    Key_Colon      = 0x3a
    Key_Semicolon  = 0x3b
    Key_Less       =0x3c
    Key_Equal      =0x3d
    Key_Greater    =0x3e
    Key_Question   =    0x3f
    Key_At         =0x40
    Key_A          =0x41
    Key_B          =0x42
    Key_C          =0x43
    Key_D          =0x44
    Key_E          =0x45
    Key_F          =0x46
    Key_G          =0x47
    Key_H          =0x48
    Key_I          =0x49
    Key_J          =0x4a
    Key_K          =0x4b
    Key_L          =0x4c
    Key_M          =0x4d
    Key_N          =0x4e
    Key_O          =0x4f
    Key_P          =0x50
    Key_Q          =0x51
    Key_R          =0x52
    Key_S          =0x53
    Key_T          =0x54
    Key_U          =0x55
    Key_V          =0x56
    Key_W          =0x57
    Key_X          =0x58
    Key_Y          =0x59
    Key_Z          =0x5a
    Key_BracketLeft =0x5b
    Key_Backslash   =0x5c
    Key_BracketRight =   0x5d
    Key_AsciiCircum =0x5e
    Key_Underscore  =0x5f
    Key_QuoteLeft   =0x60
    Key_BraceLeft   =0x7b
    Key_Bar         =0x7c
    Key_BraceRight  =0x7d
    Key_AsciiTilde  =0x7e
    Key_unknown     = 0x01FFFFFF

    NonPrintableMask = 0x01000000
    Mask             = 0x01FFFFFF

class KeyModifier:
    NoModifier      = 0x00000000
    ShiftModifier   = 0x02000000
    ControlModifier = 0x04000000
    AltModifier     = 0x08000000
    MetaModifier    = 0x10000000
    KeypadModifier  = 0x20000000

    Mask            = 0x3F000000

def nativeToVaiKeyCode(native_key_code):
    key_mapper = {
      1                    : Key.Key_A | KeyModifier.ControlModifier,
      2                    : Key.Key_B | KeyModifier.ControlModifier,
      3                    : Key.Key_C | KeyModifier.ControlModifier,
      4                    : Key.Key_D | KeyModifier.ControlModifier,
      5                    : Key.Key_E | KeyModifier.ControlModifier,
      6                    : Key.Key_F | KeyModifier.ControlModifier,
      7                    : Key.Key_G | KeyModifier.ControlModifier,
      8                    : Key.Key_Backspace,
      9                    : Key.Key_Tab,
      10                   : Key.Key_Return,
      11                   : Key.Key_K | KeyModifier.ControlModifier,
      12                   : Key.Key_L | KeyModifier.ControlModifier,
      13                   : Key.Key_M | KeyModifier.ControlModifier,
      14                   : Key.Key_N | KeyModifier.ControlModifier,
      15                   : Key.Key_O | KeyModifier.ControlModifier,
      16                   : Key.Key_P | KeyModifier.ControlModifier,
      17                   : Key.Key_Q | KeyModifier.ControlModifier,
      18                   : Key.Key_R | KeyModifier.ControlModifier,
      19                   : Key.Key_S | KeyModifier.ControlModifier,
      20                   : Key.Key_T | KeyModifier.ControlModifier,
      21                   : Key.Key_U | KeyModifier.ControlModifier,
      22                   : Key.Key_V | KeyModifier.ControlModifier,
      23                   : Key.Key_W | KeyModifier.ControlModifier,
      24                   : Key.Key_X | KeyModifier.ControlModifier,
      25                   : Key.Key_Y | KeyModifier.ControlModifier,
      26                   : Key.Key_Z | KeyModifier.ControlModifier,
      27                   : Key.Key_Escape,
      32                   : Key.Key_Space,
      33                   : Key.Key_Exclam,
      34                   : Key.Key_QuoteDbl,
      35                   : Key.Key_NumberSign,
      36                   : Key.Key_Dollar,
      37                   : Key.Key_Percent,
      38                   : Key.Key_Ampersand,
      39                   : Key.Key_Apostrophe,
      40                   : Key.Key_ParenLeft,
      41                   : Key.Key_ParenRight,
      42                   : Key.Key_Asterisk,
      43                   : Key.Key_Plus,
      44                   : Key.Key_Comma,
      45                   : Key.Key_Minus,
      46                   : Key.Key_Period,
      47                   : Key.Key_Slash,
      48                   : Key.Key_0,
      49                   : Key.Key_1,
      50                   : Key.Key_2,
      51                   : Key.Key_3,
      52                   : Key.Key_4,
      53                   : Key.Key_5,
      54                   : Key.Key_6,
      55                   : Key.Key_7,
      56                   : Key.Key_8,
      57                   : Key.Key_9,
      58                   : Key.Key_Colon,
      59                   : Key.Key_Semicolon,
      60                   : Key.Key_Less,
      61                   : Key.Key_Equal,
      62                   : Key.Key_Greater,
      63                   : Key.Key_Question,
      64                   : Key.Key_At,
      65                   : Key.Key_A | KeyModifier.ShiftModifier,
      66                   : Key.Key_B | KeyModifier.ShiftModifier,
      67                   : Key.Key_C | KeyModifier.ShiftModifier,
      68                   : Key.Key_D | KeyModifier.ShiftModifier,
      69                   : Key.Key_E | KeyModifier.ShiftModifier,
      70                   : Key.Key_F | KeyModifier.ShiftModifier,
      71                   : Key.Key_G | KeyModifier.ShiftModifier,
      72                   : Key.Key_H | KeyModifier.ShiftModifier,
      73                   : Key.Key_I | KeyModifier.ShiftModifier,
      74                   : Key.Key_J | KeyModifier.ShiftModifier,
      75                   : Key.Key_K | KeyModifier.ShiftModifier,
      76                   : Key.Key_L | KeyModifier.ShiftModifier,
      77                   : Key.Key_M | KeyModifier.ShiftModifier,
      78                   : Key.Key_N | KeyModifier.ShiftModifier,
      79                   : Key.Key_O | KeyModifier.ShiftModifier,
      80                   : Key.Key_P | KeyModifier.ShiftModifier,
      81                   : Key.Key_Q | KeyModifier.ShiftModifier,
      82                   : Key.Key_R | KeyModifier.ShiftModifier,
      83                   : Key.Key_S | KeyModifier.ShiftModifier,
      84                   : Key.Key_T | KeyModifier.ShiftModifier,
      85                   : Key.Key_U | KeyModifier.ShiftModifier,
      86                   : Key.Key_V | KeyModifier.ShiftModifier,
      87                   : Key.Key_W | KeyModifier.ShiftModifier,
      88                   : Key.Key_X | KeyModifier.ShiftModifier,
      89                   : Key.Key_Y | KeyModifier.ShiftModifier,
      90                   : Key.Key_Z | KeyModifier.ShiftModifier,
      91                   : Key.Key_BracketLeft,
      92                   : Key.Key_Backslash,
      93                   : Key.Key_BracketRight,
      94                   : Key.Key_AsciiCircum,
      95                   : Key.Key_Underscore,
      96                   : Key.Key_QuoteLeft,
      97                   : Key.Key_A,
      98                   : Key.Key_B,
      99                   : Key.Key_C,
      100                  : Key.Key_D,
      101                  : Key.Key_E,
      102                  : Key.Key_F,
      103                  : Key.Key_G,
      104                  : Key.Key_H,
      105                  : Key.Key_I,
      106                  : Key.Key_J,
      107                  : Key.Key_K,
      108                  : Key.Key_L,
      109                  : Key.Key_M,
      110                  : Key.Key_N,
      111                  : Key.Key_O,
      112                  : Key.Key_P,
      113                  : Key.Key_Q,
      114                  : Key.Key_R,
      115                  : Key.Key_S,
      116                  : Key.Key_T,
      117                  : Key.Key_U,
      118                  : Key.Key_V,
      119                  : Key.Key_W,
      120                  : Key.Key_X,
      121                  : Key.Key_Y,
      122                  : Key.Key_Z,
      123                  : Key.Key_BraceLeft,
      124                  : Key.Key_Bar,
      125                  : Key.Key_BraceRight,
      126                  : Key.Key_AsciiTilde,
      127                  : Key.Key_Backspace,
      curses.KEY_DOWN      : Key.Key_Down,
      curses.KEY_UP        : Key.Key_Up,
      curses.KEY_LEFT      : Key.Key_Left,
      curses.KEY_RIGHT     : Key.Key_Right,
      curses.KEY_BACKSPACE : Key.Key_Backspace,
      curses.KEY_NPAGE     : Key.Key_PageDown,
      curses.KEY_PPAGE     : Key.Key_PageUp,
      curses.KEY_DC        : Key.Key_Delete,
    }
    return key_mapper.get(native_key_code)

def isKeyCodePrintable(key_code):
    return ((key_code & Key.NonPrintableMask) == 0)

def vaiKeyCodeToText(key_code):
    if not isKeyCodePrintable(key_code):
        return ''

    key_map = {
        Key.Key_Space        : ' ',
        Key.Key_Exclam       : '!',
        Key.Key_QuoteDbl     : '"',
        Key.Key_NumberSign   : '#',
        Key.Key_Dollar       : '$',
        Key.Key_Percent      : '%',
        Key.Key_Ampersand    : '&',
        Key.Key_Apostrophe   : "'",
        Key.Key_ParenLeft    : '(',
        Key.Key_ParenRight   : ')',
        Key.Key_Asterisk     : '*',
        Key.Key_Plus         : '+',
        Key.Key_Comma        : ',',
        Key.Key_Minus        : '-',
        Key.Key_Period       : '.',
        Key.Key_Slash        : '/',
        Key.Key_0            : '0',
        Key.Key_1            : '1',
        Key.Key_2            : '2',
        Key.Key_3            : '3',
        Key.Key_4            : '4',
        Key.Key_5            : '5',
        Key.Key_6            : '6',
        Key.Key_7            : '7',
        Key.Key_8            : '8',
        Key.Key_9            : '9',
        Key.Key_Colon        : ':',
        Key.Key_Semicolon    : ';',
        Key.Key_Less         : '<',
        Key.Key_Equal        : '=',
        Key.Key_Greater      : '>',
        Key.Key_Question     : '?',
        Key.Key_At           : '@',
        Key.Key_A            : 'a',
        Key.Key_B            : 'b',
        Key.Key_C            : 'c',
        Key.Key_D            : 'd',
        Key.Key_E            : 'e',
        Key.Key_F            : 'f',
        Key.Key_G            : 'g',
        Key.Key_H            : 'h',
        Key.Key_I            : 'i',
        Key.Key_J            : 'j',
        Key.Key_K            : 'k',
        Key.Key_L            : 'l',
        Key.Key_M            : 'm',
        Key.Key_N            : 'n',
        Key.Key_O            : 'o',
        Key.Key_P            : 'p',
        Key.Key_Q            : 'q',
        Key.Key_R            : 'r',
        Key.Key_S            : 's',
        Key.Key_T            : 't',
        Key.Key_U            : 'u',
        Key.Key_V            : 'v',
        Key.Key_W            : 'w',
        Key.Key_X            : 'x',
        Key.Key_Y            : 'y',
        Key.Key_Z            : 'z',
        Key.Key_BracketLeft  : '[',
        Key.Key_Backslash    : '\\',
        Key.Key_BracketRight : ']',
        Key.Key_AsciiCircum  : '^',
        Key.Key_Underscore   : '_',
        Key.Key_QuoteLeft    : '`',
        Key.Key_BraceLeft    : '{',
        Key.Key_Bar          : '|',
        Key.Key_BraceRight   : '}',
        Key.Key_AsciiTilde   : '~',

        Key.Key_A | KeyModifier.ShiftModifier : 'A',
        Key.Key_B | KeyModifier.ShiftModifier : 'B',
        Key.Key_C | KeyModifier.ShiftModifier : 'C',
        Key.Key_D | KeyModifier.ShiftModifier : 'D',
        Key.Key_E | KeyModifier.ShiftModifier : 'E',
        Key.Key_F | KeyModifier.ShiftModifier : 'F',
        Key.Key_G | KeyModifier.ShiftModifier : 'G',
        Key.Key_H | KeyModifier.ShiftModifier : 'H',
        Key.Key_I | KeyModifier.ShiftModifier : 'I',
        Key.Key_J | KeyModifier.ShiftModifier : 'J',
        Key.Key_K | KeyModifier.ShiftModifier : 'K',
        Key.Key_L | KeyModifier.ShiftModifier : 'L',
        Key.Key_M | KeyModifier.ShiftModifier : 'M',
        Key.Key_N | KeyModifier.ShiftModifier : 'N',
        Key.Key_O | KeyModifier.ShiftModifier : 'O',
        Key.Key_P | KeyModifier.ShiftModifier : 'P',
        Key.Key_Q | KeyModifier.ShiftModifier : 'Q',
        Key.Key_R | KeyModifier.ShiftModifier : 'R',
        Key.Key_S | KeyModifier.ShiftModifier : 'S',
        Key.Key_T | KeyModifier.ShiftModifier : 'T',
        Key.Key_U | KeyModifier.ShiftModifier : 'U',
        Key.Key_V | KeyModifier.ShiftModifier : 'V',
        Key.Key_W | KeyModifier.ShiftModifier : 'W',
        Key.Key_X | KeyModifier.ShiftModifier : 'X',
        Key.Key_Y | KeyModifier.ShiftModifier : 'Y',
        Key.Key_Z | KeyModifier.ShiftModifier : 'Z',
    }

    return key_map.get(key_code, '')


