# UsefulUtilities
a collection of useful tools I've discovered, and decided to make simpler  


## text utilities

[Color](#color)  
[typewrite](#typewrite)  
[slidetext](#slidetext)  
[TextArea](#textarea)  



### Color
`Color(...)`  
a flexible class that creates an ascii color-code  
- `Color(r, g, b[, state])`
- `Color(fr, fg, fb, br, bg, bb)`
- `Color(rgb[, state])`
- `Color(fg_rgb, bg_rgb)`
- `Color(hex[, state])`
- `Color(fg_bg_hex)`
- `Color(fg_hex, bg_hex)`

### typewrite
`typewrite(*values, sep:str=' ', end:str='\n', rate:float=0.05, dynamic_rate:bool=True, max_width:int=100, hidden_chars_take_time:bool=False)`  
this function prints text to look as if it is being typed.

* values : `tuple`  
values to output

* sep : `str` = `' '`  
string used to seperate multiple values

* end : `str` = `'\n'`  
string used for end of line

* rate : `float` = `0.05`  
time to wait for between printing chars

* dynamic_rate : `bool` = `False`  
controls whether or not to slightly alter the rate for different chars  
i.e: speeds up if repeating a char, punctuation takes slightly longer

* max_width : `int` = `100`  
max amount of chars to fit into a line before forcing a newline

* hidden_chars_take_time : `bool` = `False`  
controls whether invisble chars should have a delay after printing


### slidetext
`slidetext(*values, sep:str=' ', end:str='\n', block_slide:bool=False, rate:float=0.05, **slide_options)`  
* values : `tuple`  
values to output

* sep : `str` = `' '`  
string used to seperate multiple values

* end : `str` = `'\n'`  
string used for end of line

* block_slide : `bool` = `False`  
controls whether to slide every line onto screen at once (`True`), or 1 at a time from top to bottom (`False`)  

* rate : `callback`|`float` = `0.05`  
as a `float`, sleeps for `rate` seconds between refreshes  
as a `callback`, rate must take 1 argument of type `float`, between 0 and 1, and must return a `float` value that is slept for between refreshes  

* \*\*slide_options  
  - slide_start : `int` = `0`  
  what line an effect should originate from (for use with `slide_wave`)  

  - slide_wave  : `callable` = `slidetext.wave`
  `slide_wave` must be a callable function that returns a positive `int` (or `0`) and takes 1 argument of type `int` for what line is being affected  
  
  - align : `str` = `"left"`  
  controls how text is arranged
  options for align include: `left`, `right`, `center`, and `justify`, which arrange the text as you would expect these options to work in a word document  
  
  - start_side : `str` = `left`  
  controls where text slides from
  options include: `left` and `right`

### TextArea
`TextArea(*lines)`  

* `TextArea.write(self, line:int, text:str, print_method:callable=print, flash:bool=False, wait:float=0)`
* `TextArea.clear(self)`
* `TextArea.replace(self)`
* `TextArea.input(self)`
* `TextArea.add(self, *lines)`

a class that simplifies output on multiple lines







