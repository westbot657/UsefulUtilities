
import time
import re


class Color:

    RED    = "\033[38;2;255;0;0m"
    ORANGE = "\033[38;2;255;127;0m"
    YELLOW = "\033[38;2;255;255;0m"
    GREEN  = "\033[38;2;0;255;0m"
    BLUE   = "\033[38;2;0;0;255m"
    PURPLE = "\033[38;2;255;0;255m"
    BLACK  = "\033[38;2;0;0;0m"
    WHITE  = "\033[38;2;255;255;255m"
    GREY = GRAY = "\033[38;2;127;127;127m"
    NONE = "\033[0m"

    @staticmethod
    def toHex(val):
        """
        val may be a tuple (r, g, b) or an int (0xff0000)
        """

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
            r = int(_hi.get(hex[0], hex[0]) * 16) + int(_hi.get(hex[1], hex[1]))
            g = int(_hi.get(hex[2], hex[2]) * 16) + int(_hi.get(hex[3], hex[3]))
            b = int(_hi.get(hex[4], hex[4]) * 16) + int(_hi.get(hex[5], hex[5]))

        elif isinstance(hex, str): # test = 16744192 : #ff7f00
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
                        if B == 0:
                            self.value = f"\033[38;2;{r};{g};{b}m"
                        elif B == 1:
                            self.value = f"\033[48;2;{r};{g};{b}m"
                        elif B == 2:
                            self.value = f"\033[38;2;{r};{g};{b}m\033[48;2;{r};{g};{b}m"
                        else:
                            self.value = Exception(f"Invalid state: '{B}'")

                elif isinstance(A, tuple):
                    # (r, g, b), state
                    # (fr, fg, fb), (br, bg, bb)

                    if isinstance(B, int):
                        # (r, g, b), state
                        r, g, b = A
                        if B == 0:
                            self.value = f"\033[38;2;{r};{g};{b}m"
                        elif B == 1:
                            self.value = f"\033[48;2;{r};{g};{b}m"
                        elif B == 2:
                            self.value = f"\033[38;2;{r};{g};{b}m\033[48;2;{r};{g};{b}m"
                        else:
                            raise Exception(f"Invalid state: {B}")

                    elif isinstance(B, tuple):
                        # (fr, fg, fb), (br, bg, bb)
                        fr, fg, fb = A
                        br, bg, bb = B

                        self.value = f"\033[38;2;{fr};{fg};{fb}m\033[48;2;{br};{bg};{bb}m"

                elif isinstance(A, int):
                    # 0xFFFFFF, state
                    r, g, b = Color.toRGB(A)

                    if B == 0:
                        self.value = f"\033[38;2;{r};{g};{b}m"
                    elif B == 1:
                        self.value = f"\033[48;2;{r};{g};{b}m"
                    elif B == 2:
                        self.value = f"\033[38;2;{r};{g};{b}m\033[48;2;{r};{g};{b}m"
                    else:
                        self.value = Exception(f"Invalid state: {B}")

            elif len(args) == 3:
                # r, g, b
                
                A, B, C = args

                if isinstance(A, int):
                    # r, g, b
                    self.value = f"\033[38;2;{A};{B};{C}m"

            elif len(args) == 4:
                # r, g, b, state
                r, g, b, B = args
                if B == 0:
                    self.value = f"\033[38;2;{r};{g};{b}m"
                elif B == 1:
                    self.value = f"\033[48;2;{r};{g};{b}m"
                elif B == 2:
                    self.value = f"\033[38;2;{r};{g};{b}m\033[48;2;{r};{g};{b}m"
                else:
                    raise Exception(f"Invalid state: {B}")

        self.fgRed, self.fgGreen, self.fgBlue = self.bgRed, self.bgGreen, self.bgBlue = self.fg = self.bg = (None, None, None)

        if self.value:
            match = re.findall(r"\033\[(\d)8;2;(\d{1,3});(\d{1,3});(\d{1,3})m", self.value)
            if len(match) == 1:
                t, r, g, b = match[0]
                if t == "3":
                    self.fgRed, self.fgGreen, self.fgBlue = self.fg = (r, g, b)

                elif t == "4":
                    self.bgRed, self.bgGreen, self.bgBlue = self.bg = (r, g, b)

            else:
                FG, BG = match
                _, fr, fg, fb = FG
                _, br, bg, bb = BG
                self.fgRed, self.fgGreen, self.fgBlue = self.fg = (fr, fg, fb)
                self.bgRed, self.bgGreen, self.bgBlue = self.bg = (br, bg, bb)

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
        #print(self.fg)
        return self.value

    def __str__(self):
        #print(self.fg)
        return self.value

def length(string):
    """
    get the visual length of a string, ignoring special ascii chars
    if multiple lines are given, returns the longest length,
    if carriage returns are given, returns the length as if it's 2 lines
    """

    if isinstance(string, str):
        lines = re.split(r"(\n|\r|\033\[-?\d*(f|F))", string)
    elif isinstance(string, (list, tuple)):
        lines = list(string)

    max_len = 0
    for line in lines:
        if "\033" in line:
            fline = ""
            while line != "":
                if m := re.match(r"\033\[[^a-zA-Z]*[a-zA-Z]", line):
                    m = m.group()
                    line = line.replace(m, "", 1)

                else:
                    fline = line[0]
                    line = line[1:]
                    
            max_len = max(len(fline), max_len)

        else:
            max_len = max(len(line), max_len)

    return max_len

def segment(text, start, end=None):
    """
    pass text to get segment of, and end position, or text, start pos, and end pos
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
            if start <= width:
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

def _slidetext_vslide(line): # slide_wave
    return abs(line) * 2

def _slidetext_easeinout(idx): # rate
    return (1-idx if idx <= 0.5 else idx)/10

def _slidetext_rate(): pass

def _slidetext_wave(ln):
    return 0

def slidetext(*values, sep=" ", end="\n", block_slide=False, rate=0.05, **slide_options):
    """
    block_slide: whether to slide multiple lines simultaneously, or one at a time  

    if rate is a `callback`, then when called, it will be passed a float between 0 and 1, representing the slide progress,
    and is expected to return a `float` for how long to wait

    slide_options:
    slide_start:`int` line that starts sliding first (no difference if no other setting is set)  
    slide_wave:`callback` function that returns a char-offset when passed a line number  
    (line number is relative to slide_start if given, or 0, the top line of text) (positive is below, negative is above)  
    align:`str`  "center", "left", "right", or "justify" (default is "left")  
    start_side:`str`  "left", "right" (which side of the screen should the text slid out from) (may add "top" and "bottom")
    """
    pass

    text = sep.join([str(v) for v in values]) + end

    lines = text.split("\n")
    disp_lines = ["" for l in range(len(lines))]

    align = slide_options.get("align", "left")
    start_side = slide_options.get("start_side", "left")
    slide_start = slide_options.get("slide_start", 0)
    slide_wave = slide_options.get("slide_wave", _slidetext_wave)

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
                return " " * (len(space) + cls.v)
            
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


slidetext.rate = _slidetext_rate
slidetext.wave = _slidetext_wave
slidetext.rate.ease_in_out = _slidetext_easeinout
slidetext.wave.vslide = _slidetext_vslide


class TextArea:

    def __init__(self, *lines):
        self.lines = lines

    def write(self, line, text, print_method=print, flash=False, wait=0):
        pass

    def clear(self, line, flash=False, wait=0):
        pass

    def replace(self, line, text, print_method=print, flash=False, wait=0):
        pass

    def input(self, line, prompt="", print_method=print, flash=False, clear_after=True):
        pass

    def addLine(self, line="", print_method=print, flash=False, wait=0):
        pass

    def addLines(self, *lines, print_method=print, flash=False, wait=0):
        pass

    def _update(self, lines=-1):
        pass


def main():
    typewrite("Hello, there!")

    typewrite(f"{Color('#ff0000')}Hello{Color()}, {Color.ORANGE}there{Color()}!")

    slidetext("This is a test!")

    slidetext("\n".join([
        "random block of text",
        "for the purpose of testing text alignment",
        "weeee!!"
    ]), start_side="left", block_slide=True, slide_start=0, rate=slidetext.rate.ease_in_out, align="center")

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
        



