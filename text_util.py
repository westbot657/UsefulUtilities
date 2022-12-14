
from threading import Thread

import math
import time
import re

# Things I want to add:
# Progress bar (Text Area compatible only)
# Debug print (cuz it's a good class and I need it)
# more text display methods (ideally compatible with TextArea)

def get_kwargs(kwargs:dict, *allowed_keys):
    for key in allowed_keys:
        val = kwargs.get(key, None)
        if val:
            return val

    return None

class Color:

    NONE = "\033[0m"

    class FG:
        RED    = "\033[38;2;255;0;0m"
        ORANGE = "\033[38;2;255;127;0m"
        YELLOW = "\033[38;2;255;255;0m"
        GREEN  = "\033[38;2;0;255;0m"
        CYAN   = "\033[38;2;0;255;255m"
        BLUE   = "\033[38;2;0;0;255m"
        PURPLE = "\033[38;2;255;0;255m"
        BLACK  = "\033[38;2;0;0;0m"
        WHITE  = "\033[38;2;255;255;255m"
        GREY = GRAY = "\033[38;2;127;127;127m"
        NONE = "\033[0m"

    class BG:
        RED    = "\033[48;2;255;0;0m"
        ORANGE = "\033[48;2;255;127;0m"
        YELLOW = "\033[48;2;255;255;0m"
        GREEN  = "\033[48;2;0;255;0m"
        CYAN   = "\03[48;2;0;255;255m"
        BLUE   = "\033[48;2;0;0;255m"
        PURPLE = "\033[48;2;255;0;255m"
        BLACK  = "\033[48;2;0;0;0m"
        WHITE  = "\033[48;2;255;255;255m"
        GREY = GRAY = "\033[48;2;127;127;127m"
        NONE = "\033[0m"

    @staticmethod
    def rainbow(text, start=0, end=None, repeat=1):
        """
        if end is None, the rainbow will go back to purple/red at the end of the text,
        if end is negative, rainbow will shift backwards

        setting start to None will create a reversed rainbow from leaving both start and end as their default value

        repeat effects how many times the rainbow shifts between the start and end

        start and end do not have to be valid indeces of the string, must must be integers
        """

        if start == None:
            start = length(text)
            end = 0

        if end == None:
            end = length(text)

        width = int((end - start) / repeat)
        
        def _get(percent):
            while percent > 1:
                percent -= 1
            while percent < 0:
                percent += 1

            red = max(int(((math.cos(math.radians(percent * 360)) / 2) + 0.5) * 255), 0)
            green = max(int(((math.cos(math.radians((percent * 360) - 120)) / 2) + 0.5) * 255), 0)
            blue = max(int(((math.cos(math.radians((percent * 360) + 120)) / 2) + 0.5) * 255), 0)

            # print(f"\033[38;2;{red};{green};{blue}m", red, green, blue, "\033[0m")
            return f"\033[38;2;{red};{green};{blue}m"

        colored = ""
        for i in range(len(text)):
            c = text[i]
            d = i
            while d < min(start, end):
                d += abs(width)

            while d > max(start, end):
                d -= abs(width)

            col = _get(d/width)
            colored += col + c
        colored += "\033[0m"
        return colored

    @staticmethod
    def fill_color(string:str) -> str:
        """
        This function spreads any existing colors through the string, fixing coloring issues when
        getting a segment of the string
        """

        curr_color = "\033[0m"
        new_string = ""

        while string != "":
            if m := re.match(r"\033\[([^a-zA-Z]*)m", string):
                m = m.group()
                string = string.replace(m, "", 1)
                curr_color = m
            
            else:
                c = string[0]
                string = string[1:]
                new_string += curr_color + c

                

    @staticmethod
    def toHex(*val) -> str:
        """
        val may be a tuple (r, g, b) or an int (0xff0000)
        """

        if len(val) == 1:
            val = val[0]

        _ih = {
            10: "a",
            11: "b",
            12: "c",
            13: "d",
            14: "e",
            15: "f"
        }

        if isinstance(val, tuple):
            r, g, b = val

        elif isinstance(val, int):
            r, g, b = Color.toRGB(val)

        return f"#{_ih.get(r//16, r//16)}{_ih.get(r%16, r%16)}{_ih.get(g//16, g//16)}{_ih.get(g%16, g%16)}{_ih.get(b//16, b//16)}{_ih.get(b%16, b%16)}"

    @staticmethod
    def toRGB(val):
        """
        pass either `str`: "#ff7f00"  
        or `int`: 0xff0000
        """
        _hi = {
            "a": 10,
            "b": 11,
            "c": 12,
            "d": 13,
            "e": 14,
            "f": 15,
            "A": 10,
            "B": 11,
            "C": 12,
            "D": 13,
            "E": 14,
            "F": 15
        }
        hex = val

        #print(f"toRGB: {hex}")

        if isinstance(hex, str):
            hex = hex.replace("#", "")
            r = (int(_hi.get(hex[0], hex[0])) * 16) + int(_hi.get(hex[1], hex[1]))
            g = (int(_hi.get(hex[2], hex[2])) * 16) + int(_hi.get(hex[3], hex[3]))
            b = (int(_hi.get(hex[4], hex[4])) * 16) + int(_hi.get(hex[5], hex[5]))

        elif isinstance(hex, int): # test = 16744192 : #ff7f00
            r = hex // 65536
            hex %= 65536
            g = hex // 256
            b = hex % 256

        return r, g, b

    def __init__(self, *args, **kwargs):
        """
        Color(r:`int`, g:`int`, b:`int`, state:`int`=0) # r/red, g/green, b/blue[, s/state] # 255, 255, 255[, 2]  
        Color(hex:`str`, state:`int`=0) # h/hex[, s/state] # "#FFFFFF"[, 2]  
        Color(fghex:`str`, bghex:`str`, state:`int`=0) # fh/fhex/fghex, bh/bhex/bghex[, s/state] # "#FFFFFF", "#FFFFFF"[, 2]  
        Color(hex:`str`, state:`int`=0) # h/hex[, s/state] # "#FFFFFF #FFFFFF"[, 2]  

        pass any of the following:  
        `string`: containing color hex code  
        ex: Color("#FF0000") or Color("#ff0000")  

        `string`: containing rgb seperated by any non-digit sequence  
        ex: Color("255,0,0") or Color("255 - 0 - 0") or Color("255, 0, 0")  
        
        `tuple`: containing r:`int`, g:`int`, b:`int`  
        ex: Color((255, 0, 0))  

        `int`: prefixed with `0x`  
        ex: Color(0xff0000)  

        `int`:  
        ex: Color(16711680) # (#ff0000)  

        `int`s: r, g, and b  
        ex: Color(255, 0, 0)  

        `int`s: r, g, and b, as kwargs  
        ex: Color(r=255, g=0, b=0)  

        `string`: hex with additional `state` seperated by any non-digit seperator  
        ex: Color("#ff0000 1")

        `tuple`: r, g, b, and `state`  
        ex: Color((255, 0, 0, 1))  

        `string`: containing 2 hex values, for fg and bg  
        ex: Color("#ff0000 #ffff00")  

        `tuple`: containing rgb for fg, and rgb for bg  
        ex: Color((255, 0, 0, 255, 255, 0))  

        `int`s: fr, fg, fb, br, bg, bb (foreground rgb and background rgb)  
        ex: Color(255, 0, 0, 255, 255, 0)

        `int`s: fr, fg, fb, br, bg, bb, `state`  
        ex: Color(255, 0, 0, 255, 255, 0, 1)  

        `int`s: fr, fg, fb, br, bg, bb, as kwargs
        ex: Color(fr=255, fg=0, fb=0, br=255, bg=255, bb=0)  

        `int`s: fr, fg, fb, br, bg, bb, state as kwargs:

        ---
        `state`:  
        controls whether the color is foreground, background, or both
        state == 0 => background (default)
        state == 1 => foreground
        state == 2 => both
        """

        keys = kwargs.keys()

        if len(keys) == 0:
            if len(args) == 0:
                self.value = "\033[0m"
                self.fgRed, self.fgGreen, self.fgBlue = self.bgRed, self.bgGreen, self.bgBlue = self.fg = self.bg = (None, None, None)
                return
            if len(args) == 1:
                A = args[0]
                if isinstance(A, str):
                    # "#______"
                    # "#______ #______"
                    # "___, ___, ___"
                    if A.startswith("#"):
                        # "#______"
                        # "#______ #______"
                        if len(A) == 7:
                            r, g, b = Color.toRGB(A)
                            self.value = f"\033[38;2;{r};{g};{b}m"

                        else:
                            # "#______ #______"
                            fh, bh = A.strip().split(" ")
                            fr, fg, fb = Color.toRGB(fh.strip())
                            br, bg, bb = Color.toRGB(bh.strip())
                            self.value = f"\033[38;2;{fr};{fg};{fb}m\033[48;2;{br};{bg};{bb}m"

                    else:
                        # "___, ___, ___"
                        r = re.match(r"\d{1,3}", A)
                        if not r: raise Exception(f"Invalid rgb-string: '{A}'")
                        r = r.group()
                        A = re.sub(r + r"[^\d]+", "", A, 1)
                        g = re.match(r"\d{1,3}", A)
                        if not g: raise Exception(f"Invalid rgb-string: '{r+A}'")
                        g = g.group()
                        A = re.sub(g + r"[^\d]+", "", A, 1)
                        b = re.match(r"\d{1,3}", A)
                        if not b: raise Exception(f"Invalid rgb-string: '{r+g+A}'")
                        b = b.group()
                        self.value = f"\033[38;2;{r};{g};{b}m"

                elif isinstance(A, tuple):
                    # (fghex, bghex)
                    # (r, g, b)
                    # (fr, fg, fb, br, bg, bb)
                    
                    if len(A) == 2:
                        fh, bh = A
                        fr, fg, fb = Color.toRGB(fh)
                        br, bg, bb = Color.toRGB(bh)
                        self.value = f"\033[38;2;{fr};{fg};{fb}m\033[48;2;{br};{bg};{bb}m"
                    elif len(A) == 3:
                        # (r, g, b)
                        r, g, b = A
                        self.value = f"\033[38;2;{r};{g};{b}m"

                    elif len(A) == 6:
                        # (fr, fg, fb, br, bg, bb)
                        fr, fg, fb, br, bg, bb = A
                        self.value = f"\033[38;2;{fr};{fg};{fb}m\033[48;2;{br};{bg};{bb}m"
            
            elif len(args) == 2:
                A, B = args
                # "#FFFFFF", "#FFFFFF"
                # "#FFFFFF", state
                # (r, g, b), state
                # (fr, fg, fb), (br, bg, bb)
                # 0xFFFFFF, state

                if isinstance(A, str):
                    # "#FFFFFF", "#FFFFFF"
                    # "#FFFFFF", state

                    if isinstance(B, str):
                        # "#FFFFFF", "#FFFFFF"
                        fr, fg, fb = Color.toRGB(A)
                        br, bg, bb = Color.toRGB(B)
                        self.value = f"\033[38;2;{fr};{fg};{fb}m\033[48;2;{br};{bg};{bb}m"

                    elif isinstance(B, int):
                        r, g, b = Color.toRGB(A)
                        if B == 0: self.value = f"\033[38;2;{r};{g};{b}m"
                        elif B == 1: self.value = f"\033[48;2;{r};{g};{b}m"
                        elif B == 2: self.value = f"\033[38;2;{r};{g};{b}m\033[48;2;{r};{g};{b}m"
                        else: self.value = Exception(f"Invalid state: '{B}'")

                elif isinstance(A, tuple):
                    # (r, g, b), state
                    # (fr, fg, fb), (br, bg, bb)

                    if isinstance(B, int):
                        # (r, g, b), state
                        r, g, b = A
                        if B == 0: self.value = f"\033[38;2;{r};{g};{b}m"
                        elif B == 1: self.value = f"\033[48;2;{r};{g};{b}m"
                        elif B == 2: self.value = f"\033[38;2;{r};{g};{b}m\033[48;2;{r};{g};{b}m"
                        else: raise Exception(f"Invalid state: {B}")

                    elif isinstance(B, tuple):
                        # (fr, fg, fb), (br, bg, bb)
                        fr, fg, fb = A
                        br, bg, bb = B

                        self.value = f"\033[38;2;{fr};{fg};{fb}m\033[48;2;{br};{bg};{bb}m"

                elif isinstance(A, int):
                    # 0xFFFFFF, state
                    r, g, b = Color.toRGB(A)

                    if B == 0: self.value = f"\033[38;2;{r};{g};{b}m"
                    elif B == 1: self.value = f"\033[48;2;{r};{g};{b}m"
                    elif B == 2: self.value = f"\033[38;2;{r};{g};{b}m\033[48;2;{r};{g};{b}m"
                    else: raise Exception(f"Invalid state: {B}")

            elif len(args) == 3:
                # r, g, b
                
                A, B, C = args

                if isinstance(A, int):
                    # r, g, b
                    self.value = f"\033[38;2;{A};{B};{C}m"

            elif len(args) == 4:
                # r, g, b, state
                r, g, b, B = args
                if B == 0: self.value = f"\033[38;2;{r};{g};{b}m"
                elif B == 1: self.value = f"\033[48;2;{r};{g};{b}m"
                elif B == 2: self.value = f"\033[38;2;{r};{g};{b}m\033[48;2;{r};{g};{b}m"
                else: raise Exception(f"Invalid state: {B}")

        else:
            new = {}
            keys = []
            for key in kwargs.keys():
                val = kwargs[key]
                keys.append(key.lower())
                new.update({key.lower(): val})

            kwargs = new

            # Color(r:`int`, g:`int`, b:`int`, state:`int`=0) # r/red, g/green, b/blue[, s/state] # 255, 255, 255[, 2]
            # Color(hex:`str`, state:`int`=0) # h/hex[, s/state] # "#FFFFFF"[, 2]
            # Color(fghex:`str`, bghex:`str`, state:`int`=0) # fh/fhex/fghex, bh/bhex/bghex[, s/state] # "#FFFFFF", "#FFFFFF"[, 2]
            # Color(hex:`str`, state:`int`=0) # h/hex[, s/state] # "#FFFFFF #FFFFFF"[, 2]
            # Color(fr, fg, fb, br, bg, bb)

            state = get_kwargs(kwargs, "state", "s")

            red   = get_kwargs(kwargs, "red", "r", "fr", "fgr", "fg_r", "fg_red")
            green = get_kwargs(kwargs, "green", "g", "fg", "fgg", "fg_g", "fg_green")
            blue  = get_kwargs(kwargs, "blue", "b", "fb", "fgb", "fg_b", "fg_blue")

            red2   = get_kwargs(kwargs, "br", "bg_r", "bg_red", "bgred", "bgr")
            green2 = get_kwargs(kwargs, "bg", "bg_g", "bg_green", "bggreen", "bgg")
            blue2  = get_kwargs(kwargs, "bb", "bg_b", "bg_blue", "bgblue", "bgb")

            hex  = get_kwargs(kwargs, "h", "hex", "fghex", "fg_hex", "fh", "fgh")
            hex2 = get_kwargs(kwargs, "bghex", "bg_hex", "bh", "bgh")

            rgb  = get_kwargs(kwargs, "rgb", "fgrgb", "fg_rgb", "frgb")
            rgb2 = get_kwargs(kwargs, "bgrgb", "bg_rgb", "brgb")

            if state:
                if not 0 <= state <= 2:
                    raise Exception("Invalid state value")

            if (red or green or blue) and (not (red2 or green2 or blue2)):
                r = red or 0
                g = green or 0
                b = blue or 0

                s = state or 0

                if s == 0: self.value = f"\033[38;2;{r};{g};{b}m"
                elif s == 1: self.value = f"\033[48;2;{r};{g};{b}m"
                elif s == 2: self.value = f"\033[38;2;{r};{g};{b}m\033[48;2;{r};{g};{b}m"

            elif (not (red or green or blue) and (red2 or green2 or blue2)):
                r = red2 or 0
                g = green2 or 0
                b = blue2 or 0

                self.value = f"\033[48;2;{r};{g};{b}m"

            elif (red or green or blue) and (red2 or green2 or blue2):
                fr = red or 0
                fg = green or 0
                fb = blue or 0
                br = red2 or 0
                bg = green2 or 0
                bb = blue2 or 0

                self.value = f"\033[38;2;{fr};{fg};{fb}m\033[48;2;{br};{bg};{bb}m"

            elif rgb or rgb2:
                if rgb and (not rgb2): self.value = Color(rgb, state or 0).value
                elif (not rgb) and rgb2: self.value = Color(rgb2, 1).value
                else: self.value = Color(rgb, rgb2).value

            elif hex or hex2:
                if hex and (not hex2):
                    if " " in hex:
                        h1, h2 = hex.split(" ")
                        fr, fg, fb = Color.getRGB(h1)
                        br, bg, bb = Color.getRGB(h2)
                        self.value = f"\033[38;2;{fr};{fg};{fb}m\033[48;2;{br};{bg};{bb}m"
                    else:
                        r, g, b = Color.getRGB(hex)
                        s = state or 0

                        if s == 0: self.value = f"\033[38;2;{r};{g};{b}m"
                        if s == 1: self.value = f"\033[48;2;{r};{g};{b}m"
                        if s == 2: self.value = f"\033[38;2;{r};{g};{b}m\033[48;2;{r};{g};{b}m"

                elif (not hex) and hex2:
                    r, g, b = Color.getRGB(hex2)
                    
                    self.value = f"\033[48;2;{r};{g};{b}m"
                
                else:
                    fr, fg, fb = Color.getRGB(hex)
                    br, bg, bb = Color.getRGB(hex2)
                    self.value = f"\033[38;2;{fr};{fg};{fb}m\033[48;2;{br};{bg};{bb}m"


        self.fgRed, self.fgGreen, self.fgBlue = self.bgRed, self.bgGreen, self.bgBlue = self.fg = self.bg = (None, None, None)

        if self.value:
            match = re.findall(r"\033\[(\d)8;2;(\d{1,3});(\d{1,3});(\d{1,3})m", self.value)
            if len(match) == 1:
                t, r, g, b = match[0]
                if t == "3":
                    self.fgRed, self.fgGreen, self.fgBlue = self.fg = (r, g, b)

                elif t == "4":
                    self.bgRed, self.bgGreen, self.bgBlue = self.bg = (r, g, b)

            elif len(match) == 2:
                FG, BG = match
                _, fr, fg, fb = FG
                _, br, bg, bb = BG
                self.fgRed, self.fgGreen, self.fgBlue = self.fg = (fr, fg, fb)
                self.bgRed, self.bgGreen, self.bgBlue = self.bg = (br, bg, bb)

            else:
                print(f"Color: {repr(self.value)}, {match=}")

    def getFgHex(self):
        if any(self.fg):
            return Color.toHex(self.fg)
        return None

    def getBgHex(self):
        if any(self.bg):
            return Color.toHex(self.bg)
        return None

    def getHex(self):
        f = self.getFgHex()
        b = self.getBgHex()
        return ((f"fg:{f}" if f else "") + " " + (f"bg:{b}" if b else "")).strip()

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value

class DebugPrint:

    class __disabled:
        def __init__(self):
            return
        def __call__(self, *_, **__):
            return self
        def __getitem__(self, *_, **__):
            return self

    _disabled = __disabled()

    def __init__(self, name, color=Color.FG.NONE):
        self.name = name
        self.color = color
        self._tags = []
        self._active = False
        self._disabled = []
        self._tag_colors = {}

    def toggle(self, *tags):
        if not tags:
            self._active = not self._active
            return self

        for tag in tags:
            if tag in self._disabled:
                self._disabled.remove(tag)
            else:
                self._disabled.append(tag)
        return self

    def config_tags(self, color_map):
        self._tag_colors.update(color_map)
        return self

    def __getitem__(self, tag):
        if tag in self._disabled or not self._active:
            self._tags.clear()
            return DebugPrint._disabled

        self._tags.append(tag)
        return self
    
    def __call__(self, *values, sep=' '):
        if not self._active:
            self._tags.clear()
            return DebugPrint._disabled
        out = f"[{self.color}{self.name}\033[0m] "
        out += " ".join([f"{self._tag_colors.get(tag, Color.FG.NONE)}[{tag}]\033[0m" for tag in self._tags])
        out = out.strip()
        out += f": {sep.join([str(v) for v in values])}\033[0m"
        self._tags.clear()
        print(out)
        return self


_length_debug = DebugPrint("length", Color.FG.GREEN)
def length(string):
    """
    get the visual length of a string, ignoring special ascii codes
    if multiple lines are given, returns the length of the longest line,
    carriage returns are counted as newlines
    """

    if isinstance(string, str):
        lines = re.split(r"(\n|\r|\033\[-?\d*(f|F))", string)

    elif isinstance(string, (list, tuple)):
        lines = list(string)

    else:
        lines = list(str(string))

    max_len = 0

    for line in lines:
        _length_debug(f"line = {repr(line)}")

        if "\033" in line or "\b" in line:
            fline = ""

            while line != "":

                if m := re.match(r"\033\[[^a-zA-Z]*[a-zA-Z]", line):
                    m = m.group()
                    _length_debug(f"contains ascii: {repr(m)}")
                    line = line.replace(m, "", 1)

                elif line[0] == "\b":
                    _length_debug("contains backspace")
                    line = line[1:]
                    fline += fline[:-1]

                else:
                    _length_debug(f"char s: {repr(line[0])}")
                    fline += line[0]
                    line = line[1:]
                    
            _length_debug(f"len & max: {len(fline)}, {max_len}")
            max_len = max(len(fline), max_len)

        else:

            max_len = max(len(line), max_len)

    return max_len

def segment(text, start, end=None):
    """
    pass text to get segment of, and end position; or text, start pos, and end pos
    segment(text:`str`, end:`int`)
    segment(text:`str`, start:`int`, end:`end`)
    """

    if end == None:
        end = start
        start = 0

    while end < 0:
        end = length(text) + end

    seg = ""

    width = 0
    while text != "":
        if m := re.match(r"\033\[[^a-zA-Z]*[a-zA-Z]", text):
            m = m.group()
            if start-1 <= width:
                seg += m
            text = text.replace(m, "", 1)

        else:
            if width > end: break
            width += 1
            if start <= width:
                seg += text[0]
            text = text[1:]

        if width > end: break

    return seg

class TextArea:

    _compatible_print_methods = [print]
    _incompatible_print_methods = []

    @classmethod
    def _compatible(cls, func):
        cls._compatible_print_methods.append(func)
        return func

    @classmethod
    def _incompatible(cls, func):
        """
        mark an output method as incompatible with TextArea
        """
        cls._incompatible_print_methods.append(func)
        return func

    def __init__(self, *lines, print_method=print, flash:bool=False, wait:float=0, override_print_compatibility=False):
        """
        * lines : `tuple`  
        lines to add when TextArea is created  
        * print_method : `callable` = `print`  !! `slidetext` is NOT fully compatible !!  
        method used to display new lines  !! this method must accept the keyword argument: 'end' !!  
        * flash : `bool` = `False`  
        whether to flash the new lines white  
        * wait : `float` = 0  
        time to wait after displaying all lines  
        """

        if print_method in TextArea._incompatible_print_methods and not override_print_compatibility:
            raise Exception(f"output method: '{print_method}' is labeled as Incompatible")

        if print_method not in TextArea._compatible_print_methods and not override_print_compatibility:
            raise Warning(f"output method: '{print_method}' is not labeled as Compatible")

        self.lines = []
        self._thread_lock = False

        if lines:
            self.add(*lines, print_method=print_method, flash=flash, wait=wait)

    def write(self, line:int, text:str, print_method=print, flash:bool=False, wait:float=0, override_print_compatibility=False):
        """
        * line : `int`  
        line to write text on  
        * text : `str`  
        text to write at end of specified line  
        * print_method : `callable` = `print  !! `slidetext` is NOT fully compatible !!  
        method used to display text  !! this method must accept the keyword argument: 'end' !!  
        * flash : `bool` = `False`  
        whether to make the written text flash white  
        * wait : `int` = `0`  
        how long to wait after writing  
        """

        while self._thread_lock: pass
        self._thread_lock = True

        if print_method in TextArea._incompatible_print_methods and not override_print_compatibility:
            self._thread_lock = False
            raise Exception(f"output method: '{print_method}' is labeled as Incompatible")

        if print_method not in TextArea._compatible_print_methods and not override_print_compatibility:
            self._thread_lock = False
            raise Warning(f"output method: '{print_method}' is not labeled as Compatible")

        while line + 1 > len(self.lines):
            self.lines.append("")
            print()

        text_height = len(self.lines)
        curr_line = self.lines[line]
        print(f"\033[{text_height - line}F", end=curr_line, flush=False)

        if flash:
            print("\033[48;2;255;255;255m" + (" " * length(text)) + "\033[0m", end="", flush=True)
            time.sleep(0.05)
            print(("\b" * length(text)) + "\033[0m", end=(" " * length(text)) + ("\b" * length(text)), flush=True)
        
        print_method(text)
        self.lines[line] += text
        print("\n" * (text_height - line - 2), flush=True)

        self._thread_lock = False

        if wait > 0:
            time.sleep(wait)

        


    def clear(self, *lines, flash:bool=False, wait:float=0):
        """
        * lines : `int`  
        lines to clear  
        * flash : `bool` = `False`  
        whether to make each line flash white  
        * wait : `float` = `0`  
        time to wait after clearing all lines  
        """

        while self._thread_lock: pass
        self._thread_lock = True

        for line in lines:

            while line + 1 > len(self.lines):
                self.lines.append("")
                print()

            curr = self.lines[line]
            text_height = len(self.lines)
            print(f"\033[{text_height - line}F", end="", flush=False)

            if flash:
                print("\033[48;2;255;255;255m" + (" " * length(curr)) + "\033[0m", end="\r", flush=True)
                time.sleep(0.05)
            
            print("\033[0m" + (" " * length(curr)), flush=True)
            print("\n" * (text_height - line - 2), flush=True)
            self.lines[line] = ""

            if wait > 0:
                time.sleep(wait)
        
        self._thread_lock = False


    def replace(self, line:int, text:str, print_method=print, flash:bool=False, wait:float=0, override_print_compatibility=False):
        """
        * line : `int`  
        line to replace  
        * text : `str`  
        text to replace line with  
        * print_method : `callable` = `print`  !! `slidetext` is NOT fully compatible !!  
        method used to display new text  !! this method must accept the keyword argument: 'end' !!  
        * flash : `bool` = `False`  
        whether to make the line flash white  
        * wait : `float` = `0`  
        time to wait after replacing line  
        """

        while self._thread_lock: pass
        self._thread_lock = True

        if print_method in TextArea._incompatible_print_methods and not override_print_compatibility:
            self._thread_lock = False
            raise Exception(f"output method: '{print_method}' is labeled as Incompatible")

        if print_method not in TextArea._compatible_print_methods and not override_print_compatibility:
            self._thread_lock = False
            raise Warning(f"output method: '{print_method}' is not labeled as Compatible")

        while line + 1 > len(self.lines):
            self.lines.append("")
            print()

        text_height = len(self.lines)
        curr = self.lines[line]
        print(f"\033[{text_height - line}F", end=(" " * length(curr)) + "\033[0m\r\033[0m", flush=True)

        if flash:
            print("\033[48;2;255;255;255m" + (" " * length(text)) + "\033[0m", end="\r", flush=True)
            time.sleep(0.05)
            print("\033[0m" + (" " * length(text)), end="\r", flush=True)
        
        print_method(text)
        print("\n" * (text_height - line - 2), flush=True)
        self.lines[line] = text

        self._thread_lock = False
        if wait > 0:
            time.sleep(wait)


    def input(self, line:int, prompt:str="", print_method=print, flash:bool=False, clear_after:bool=False, override_print_compatibility=False):
        """
        * line : `int`  
        line to get input on  
        * prompt : `str` = `""`  
        input prompt  
        * print_method : `callable` = `print`  !! `slidetext` is NOT fully compatible !!  
        method used to display prompt  !! this method must accept the keyword argument: 'end' !!  
        * flash : `bool` = `False`  
        whether to flash the prompt white  
        * clear_after : `bool` = `False`  
        whether to erase the prompt and input afterwards  
        """

        while self._thread_lock: pass
        self._thread_lock = True

        if print_method in TextArea._incompatible_print_methods and not override_print_compatibility:
            self._thread_lock = False
            raise Exception(f"output method: '{print_method}' is labeled as Incompatible")

        if print_method not in TextArea._compatible_print_methods and not override_print_compatibility:
            self._thread_lock = False
            raise Warning(f"output method: '{print_method}' is not labeled as Compatible")

        while line + 1 > len(self.lines):
            self.lines.append("")
            print()

        text_height = len(self.lines)
        curr = self.lines[line]
        print(f"\033[{text_height - line}F", end=curr, flush=False)

        if flash:
            print("\033[48;2;255;255;255m" + (" " * length(prompt)) + "\033[0m", end=("\b" * length(prompt)), flush=True)
            time.sleep(0.05)
            print("\033[0m" + (" " * length(prompt)), end=("\b" * length(prompt)), flush=True)
        
        print_method(prompt, end="")
        self._thread_lock = False
        inp = input("")
        self._thread_lock = True

        if clear_after:
            print("\033[F" + curr + (" " * (length(prompt) + length(inp))), flush=True)

        else:
            self.lines[line] += prompt + inp

        print("\n" * (text_height - line - 2), flush=True)
        self._thread_lock = False
        return inp


    def add(self, *lines, print_method=print, flash:bool=False, wait:float=0, override_print_compatibility=False):
        """
        * lines : `tuple`  
        text to add to end of TextArea  
        * print_method : `callable` = `print`  !! `slidetext` is NOT fully compatible !!  
        method used to display new lines  
        * flash : `bool` = `False`  
        whether to flash the new lines white  
        * wait : `float` = `0`  
        time to wait after adding all lines  
        """

        while self._thread_lock: pass
        self._thread_lock = True

        if print_method in TextArea._incompatible_print_methods and not override_print_compatibility:
            self._thread_lock = False
            raise Exception(f"output method: '{print_method}' is labeled as Incompatible")

        if print_method not in TextArea._compatible_print_methods and not override_print_compatibility:
            self._thread_lock = False
            raise Warning(f"output method: '{print_method}' is not labeled as Compatible")

        for line in lines:
            self.lines.append(line)

            if flash:
                print("\033[48;2;255;255;255m" + (" " * length(line)) + "\033[0m", end="\r", flush=True)
                time.sleep(0.05)
                print(" " * length(line), end="\r", flush=True)

            print_method(line)

        self._thread_lock = False

        if wait:
            time.sleep(wait)


    def slide(self, line:int, text:str, rate=0.05, wait:int=0):
        """
        text must be a single line (no newlines, carriage returns, etc...)  

        rate can be a `float` or,  
        a `callable` that takes 1 argument of type `float` (between 0 and 1) and returns a `float` for sleep time
        """

        while self._thread_lock: pass
        self._thread_lock = True

        if re.findall(r"(\033\[-?\d*(F|f|G)|\n|\r)", text):
            self._thread_lock = False
            raise Exception("line control characters are not allowed in TextArea.slide()")
        
        while line + 1 > len(self.lines):
            self.lines.append("")
            print()

        text_height = len(self.lines)
        curr = self.lines[line]
        print(f"\033[{text_height - line}F", end=curr, flush=False)

        l = length(text)

        for i in range(l):
            s = segment(text, l-i, l)
            print(s, end="", flush=True)
            if isinstance(rate, (int, float)):
                time.sleep(rate)
            else:
                time.sleep(rate(length(s) / l))
            print("\b" * length(s), end="", flush=False)

        print(text, flush=False)
        self.lines[line] += text
        print("\n" * (text_height - line - 2), flush=True)

        self._thread_lock = False

        if wait > 0:
            time.sleep(wait)


@TextArea._compatible
def typewrite(*values, sep=" ", end="\n", rate=0.05, dynamic_rate=True, max_width=100, hidden_chars_take_time=False):
    """
    rate: time between chars
    dynamic_rate: whether to adjust rate as if text was being typed by a person
    hidden_chars_take_time: whether chars with no width should have a delay after printing
    """

    to_write = sep.join([str(v) for v in values]) + end

    capitalize_rate            = round(rate * 0.8 , 2) if dynamic_rate else rate
    repeated_char_initial_rate = round(rate * 1.25, 2) if dynamic_rate else rate
    repeated_char_rate         = round(rate * 0.5 , 2) if dynamic_rate else rate
    hidden_char_rate           = round(rate * 0.2 , 2) if dynamic_rate else rate
    whitespace_rate            = round(rate * 0.35, 2) if dynamic_rate else rate
    punctation_rate            = round(rate * 1.2 , 2) if dynamic_rate else rate

    prev_char = ""
    repeats = 0
    width = 0
    while to_write != "":
        if to_write[0] in ["\n", "\r"]:
            if hidden_chars_take_time:
                time.sleep(hidden_char_rate)
            width = 0
            print(to_write[0], end="", flush=True)
            prev_char = to_write[0]
            to_write = to_write[1:]
        
        elif m := re.match(r"\033\[([^a-zA-Z]*)([a-zA-Z])", to_write):
            val, code = m.groups()
            m = m.group()
            if hidden_chars_take_time:
                time.sleep(hidden_char_rate)
            print(m, end="", flush=True)
            to_write = to_write.replace(m, "", 1)
        
        else:
            c = to_write[0]
            to_write = to_write[1:]
            width += 1

            if width > max_width:
                if hidden_chars_take_time:
                    time.sleep(hidden_char_rate)
                print()

            if c == prev_char:
                if repeats == 0:
                    time.sleep(repeated_char_initial_rate)
                    print(c, end="", flush=True)
                    repeats = 1
                elif repeats == 1:
                    time.sleep(repeated_char_rate)
                    print(c, end="", flush=True)
                    if to_write[0] != c:
                        repeats = 0

            elif prev_char.islower() and c.isupper():
                time.sleep(capitalize_rate)
                print(c, end="", flush=True)
                
            else:

                if c in "~!@#$%^&*()`{}|[]\\:;'\"<>?,./":
                    time.sleep(punctation_rate)
                    print(c, end="", flush=True)
                    prev_char = c
                    
                    continue

                if c == " " and width + len(re.sub(r"\033\[[^a-zA-Z]*[a-zA-Z]", "", re.split(r"\s", to_write, 1)[0])) >= max_width:
                    if hidden_chars_take_time:
                        time.sleep(hidden_char_rate)
                    print("\n", end="", flush=True)
                    width = 0
                    prev_char = "\n"
                    continue

                time.sleep(rate)
                print(c, end="", flush=True)

            prev_char = c

def _slidetext_vslide(mod:int=2): # wave
    """
    `mod` controls the char offset for each line in an effect  
    Ex:  
    ```python
    >> slidetext("Example text\\nwith multiple lines", slide_wave=slidetext.wave.vwave(2))
    |
    |s

    |ext
    |e lines

    |mple text
    |ultiple lines

    |Example text
    |with multiple lines

    >> slidetext("Example text\\nwith multiple lines", slide_wave=slidetext.wave.vwave(4))
    |
    |s

    |e text
    |e lines

    |Example text
    |ultiple lines

    |Example text
    |with multiple lines
    ```  

    """
    def _wave(line:int):
        return abs(line) * mod
    return _wave

def _slidetext_uslide(mod:int=2): # wave
    if mod < 0: raise Exception("mod must be greater or equal to zero")
    def _wave(line:int):
        return abs(line) ** mod
    return _wave

def _slidetext_easeinout(mod:float=10): # rate
    """
    lower mod => faster effect  
    higher mod => slower effect
    """
    if mod <= 0: raise Exception("mod must be positive and non-zero")
    def _rate(percent:float):
        return (1 - percent if percent <= 0.5 else percent) / mod
    return _rate

def _slidetext_ease_out(mod:float=10): # rate
    """
    lower mod => faster effect  
    higher mod => slower effect
    """
    if mod <= 0: raise Exception("mod must be positive and non-zero")
    def _rate(percent:float):
        return (1 - percent) / mod
    return _rate

def _slidetext_ease_in(mod:float=10): #rate
    """
    lower mod => faster effect  
    higher mod => slower effect
    """
    if mod <= 0: raise Exception("mod must be positive and non-zero")
    def _rate(percent:float):
        return (percent) / mod
    return _rate

def _slidetext_rate(mod:float=1):
    """
    This function itself mimics the effect of using a `float` as the rate. (returns `mod` directly with no changes to the value)  
    However, it contains the builtin rates available  
    
    Example of using a builtin rate:  
    `slidetext("...", rate=slidetext.rate.ease_in())`  
    note that the rate is being called, that is because all builtin rates are wrappers to allow for configurable rates  

    Ex:  
    ```python
    >> slidetext("Example text", rate=slidetext.rate.ease_in())
    |t
    |xt
    |text
    |ple text
    |Example text
    >> slidetext("Example text", rate=slidetext.rate.ease_in(5))
    |t
    |ext
    |ple text
    |Example text
    ```  
    """
    return mod

def _slidetext_wave(*_):
    """
    This function is the default block-slide effect.  
    It also contains more builtin rates
    """
    return 0

@TextArea._incompatible
def slidetext(*values, sep=" ", end="\n", block_slide=False, rate=0.05, **slide_options):
    """
    !! NOT fully compatible with `TextArea` !!  

    block_slide: whether to slide multiple lines simultaneously, or one at a time  

    if rate is a `callback`, then when called, it will be passed a float between 0 and 1, representing the slide progress,  
    and is expected to return a `float` for how long to wait  

    slide_options:  
    slide_start:`int` line that starts sliding first (no difference if no other setting is set)  
    slide_wave:`callback` function that returns a char-offset when passed a line number  
    (line number is relative to slide_start if given, or 0, the top line of text) (positive is below, negative is above)  
    align:`str`  "center", "left", "right", or "justify" (default is "left")  
    start_side:`str`  "left", "right" (which side of the screen should the text slid out from) (may add "top" and "bottom")  
    
    ---
    builtin dynamic rates can be found in: `slidetext.rate`
    builtin wave effects can be found in: `slidetext.wave`
    
    """
    pass

    text = sep.join([str(v) for v in values]) + end

    lines = text.split("\n")
    disp_lines = ["" for l in range(len(lines))]

    align = slide_options.get("align", "left")
    start_side = slide_options.get("start_side", "left")
    slide_start = slide_options.get("slide_start", 0)
    slide_wave = slide_options.get("slide_wave", _slidetext_wave())

    width = length(lines)

    new_lines = []
    if align == "left":
        for line in lines:
            new_lines.append(line + (" " * (width - length(line))))

    elif align == "right":
        for line in lines:
            new_lines.append((" " * (width - length(line))) + line)

    elif align == "center":
        w1 = width // 2
        w2 = width - w1
        for line in lines:
            new_lines.append(
                (" " * ( w1 - ( length(line) // 2 ) ))\
                + line\
                + (" " * ( w2 - ( length(line) - (length(line) // 2) ) ))
            )

    elif align == "justify":
        class n:
            v = 0
            @classmethod
            def alt(cls, space):
                cls.v = 0 if cls.v == 1 else 1
                return " " * (len(space.group()) + cls.v)
            
            @classmethod
            def add(cls, space):
                return " " * (len(space.group()) + 1)
        for line in lines:
            fline = line

            if " " not in line:
                w1 = width // 2
                w2 = width - w1
                new_lines.append(line + (" " * (width - length(line))))
                continue

            while length(fline) < width:
                if length(f := re.sub(r" +", n.add, fline)) <= width:
                    fline = f
                elif length(f := re.sub(r" +", n.alt, fline)) <= width:
                    fline = f
                else:
                    diff = width - length(fline)
                    fline = re.sub(r" +", n.add, fline, diff)

            new_lines.append(fline)

    if block_slide:
        if start_side == "left":

            idx = 0
            midx = 0
            while idx < width - midx:
                idx += 1
                for i in range(len(new_lines)):
                    line = new_lines[i]
                    offset = slide_wave(i - slide_start)
                    midx = min(midx, idx - offset)
                    if offset >= 0:
                        print(segment(line, max(width-idx+offset, 0), width), flush=False)
                    else:
                        print(flush=False)

                print(f"\033[{len(new_lines)}F", end="", flush=True)
                if isinstance(rate, (int, float)):
                    time.sleep(rate)

                else:
                    time.sleep(rate(min(max(midx, idx), width)/width))
                
            print("\n" * len(new_lines), end="", flush=True)

        elif start_side == "right":
            idx = 0
            midx = 0
            x = 100

            while idx < width - midx + x:
                idx += 1
                for i in range(len(new_lines)):
                    line = new_lines[i]
                    offset = slide_wave(i - slide_start)
                    midx = min(midx, idx - offset)
                    if offset >= 0:
                        print(f"\033[{x - (idx - offset)}G" + segment(line, 0, max(0, idx - offset)), end="\033[0m \n", flush=False)
                    else:
                        print(flush=False)

                print(f"\033[{len(new_lines)}F", end="", flush=True)
                if isinstance(rate, (int, float)):
                    time.sleep(rate)
                else:
                    time.sleep(rate(min(max(midx, idx), x)/x))
                
            print("\n" * len(new_lines), end="", flush=True)

    else:
        if start_side == "left":

            for line in new_lines:
                i = 0
                while i < width:
                    i += 1
                    print(segment(line, width-i, width), end="\r", flush=True)
                    if isinstance(rate, (float, int)):
                        time.sleep(rate)
                    else:
                        time.sleep(rate((width-i)/width))
                print()

        elif start_side == "right":
            x = 100 # rough estimate of screen width in chars

            for line in new_lines:
                i = 0
                while i < x:
                    i += 1
                    print(f"\033[{x-i}G" + segment(line, i) + " \033[0m", end="\r", flush=True)
                    if isinstance(rate, (float, int)):
                        time.sleep(rate)
                    else:
                        time.sleep(rate((width-i)/width))
                print()

class ProgressBar:

    class Style:

        def __init__(self, left_end, loaded_area, unloaded_area, right_end):
            self.left_end = left_end
            self.loaded_area = loaded_area
            self.unloaded_area = unloaded_area
            self.right_end = right_end

        def get(self, bar_width:int=10, progress:float=0, left_color=Color.FG.NONE, loaded_color=Color.FG.NONE, unloaded_color=Color.FG.NONE, right_color=None):
            """
            progress should be a float between 0 and 1
            width does not include the end chars
            """
            right_color = right_color or left_color

            loaded = int(progress * bar_width)
            unloaded = bar_width - loaded

            return f"{left_color}{self.left_end}{loaded_color}{self.loaded_area * loaded}{unloaded_color}{self.unloaded_area * unloaded}{right_color}{self.right_end}\033[0m"

    Style.solid = Style("???", "???", "???", "???")
    Style.ascii_1 = Style("[", "|", "|", "]")
    Style.ascii_2 = Style("<", "=", "-", ">")

    def __init__(self, width=10, style=Style.ascii_1, left_end_color=Color.NONE, loaded_area_color=Color.NONE, unloaded_area_color=Color.NONE, right_end_color=None):
        self.style = style
        self.left_end_color = left_end_color
        self.loaded_area_color = loaded_area_color
        self.unloaded_area_color = unloaded_area_color
        self.right_end_color = right_end_color or left_end_color

        self.width = width
        self.progress = 0

    def set_progress(self, value):
        self.progress = value

    def __repr__(self):
        return self.style.get(self.width, self.progress, self.left_end_color, self.loaded_area_color, self.unloaded_area_color, self.right_end_color)

    def with_percentage(self, side="right", accuracy=2):
        
        percent = str(float(round(self.progress * 100, accuracy)))
        while len(percent.split(".")[1]) < accuracy:
            percent += "0"
        if accuracy == 0:
            percent = percent.split(".")[0]

        if side == "right":
            return f"{repr(self)} {percent}%"
        elif side == "left":
            return f"{percent}% {repr(self)}"

slidetext.rate = _slidetext_rate
slidetext.wave = _slidetext_wave

slidetext.rate.ease_in_out = _slidetext_easeinout
slidetext.rate.ease_in = _slidetext_ease_in
slidetext.rate.ease_out = _slidetext_ease_out

slidetext.wave.vslide = _slidetext_vslide
slidetext.wave.uslide = _slidetext_uslide


def slidetext_test():
    return
def typewrite_test():
    return
def TextArea_test():
    area = TextArea(
        "",
        " 01 | ",
        " 02 | ",
        " 03 | ",
        " 04 | ",
        " 05 | ",
        " 06 | ",
        " 07 | ",
        " 08 | ",
        " 09 | ",
        " 10 | ",
        "",
        ""
    )

    area.write(1, f"{Color.FG.ORANGE}@Lexer{Color.NONE}", flash=True, wait=0.3)
    area.write(2, f"{Color.FG.YELLOW}#!literals{Color.NONE}", flash=True, wait=0.3)


def ProgressBar_test():

    test_bar = ProgressBar(15, ProgressBar.Style.solid, Color.FG.BLACK, Color.FG.GREEN, Color.FG.RED)

    area = TextArea(
        "",
        "",
        ""
    )

    def _bar_update():
        for i in range(200):
            test_bar.set_progress((i + 1) / 200)
            area.replace(0, test_bar)
            time.sleep(0.01)

    bar_update = Thread(target=_bar_update)
    bar_update.start()

    time.sleep(0.4)
    area.write(1, "How well does this work?", typewrite, wait=0.3)

    while test_bar.progress < 1: pass

    return

def main():
    
    #slidetext_test()
    #typewrite_test()
    #TextArea_test()
    ProgressBar_test()

    return

if __name__ == "__main__":

    main()

    while True:
        cmd = input("> ").strip()
        if cmd == "": continue
        if cmd == "exit()": break

        try:
            exec(cmd)
        except Exception as e:
            print(e)
        



