
class Color:

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
            if len(args) == 1:
                a = args[0]
                if isinstance(a, str):
                    # "#______"
                    # "#______ #______"
                    # "___, ___, ___"
                    if a.startswith("#"):
                        # "#______"
                        # "#______ #______"
                        if len(a) == 7:
                            # "#______"
                            pass
                        else:
                            # "#______ #______"
                            pass

                    else:
                        # "___, ___, ___"
                        pass
                elif isinstance(a, tuple):
                    # (fghex, bghex)
                    # (r, g, b)
                    # (fr, fg, fb, br, bg, bb)
                    
                    if len(a) == 2:
                        # (fghex, bghex)
                        pass
                    elif len(a) == 3:
                        # (r, g, b)
                        pass

                    elif len(a) == 6:
                        # (fr, fg, fb, br, bg, bb)
                        pass
            
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
                        pass

                    elif isinstance(B, int):
                        # "#FFFFFF", state
                        pass

                elif isinstance(A, tuple):
                    # (r, g, b), state
                    # (fr, fg, fb), (br, bg, bb)

                    if isinstance(B, int):
                        # (r, g, b), state
                        r, g, b = A
                        if B == 0:
                            return f"\033[38;2;{r};{g};{b}m"
                        elif B == 1:
                            return f"\033[48;2;{r};{g};{b}m"
                        elif B == 2:
                            return f"\033[38;2;{r};{g};{b}m\033[48;2;{r};{g};{b}m"
                        else:
                            raise Exception(f"Invalid state: {B}")

                    elif isinstance(B, tuple):
                        # (fr, fg, fb), (br, bg, bb)
                        fr, fg, fb = A
                        br, bg, bb = B

                        return f"\033[38;2;{fr};{fg};{fb}m\033[48;2;{br};{bg};{bb}m"

                elif isinstance(A, int):
                    # 0xFFFFFF, state
                    pass

            elif len(args) == 3:
                # r, g, b
                # (fr, fg, fb), (br, bg, bb)
                # "#FFFFFF", "#FFFFFF"

                A, B, C = args

                if isinstance(A, int):
                    # r, g, b
                    pass


            elif len(args) == 4:
                # r, g, b, state
                # 





x = Color()


if __name__ == "__main__":
    pass



