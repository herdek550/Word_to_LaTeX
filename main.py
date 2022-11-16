"""
Word -> uložit kopii (uložit jako) -> vybrat prostý text (.txt):
-> Jiné kódování -> Unicode (utf-8)
-> Nemít zaškrtnuté "vložit konec řádků"
-> Ukončení řádků CR/LF

"""

import re # regex



INPUT = "text2.txt"

BULLETS = ["• ", "o ", "■ "]
MATH_SYMBOLS = ["*", "^", "_"]

with open(INPUT, "r", encoding="utf-8") as file:
    data = file.read()

print(repr(data))

a = data.split("\n")

print(len(a))

global_list = []

current_depth = None

def bullets(_string, _current_level):
    global global_list
    print("BULLET--------------------")
    print(repr(_string))
    print(f"current level: {_current_level}")
    #_string = _string.replace("\t", "")
    
    _string_depth = None
    for _index, _bullet in enumerate(BULLETS):
        _regex_pattern_s = r"^" + str(_bullet)
        _regex_pattern_o = re.compile(_regex_pattern_s)
        if _regex_pattern_o.search(_string):
            print(f"TRUE - string depth {_index}")
            #_string = _string.replace(_bullet, r"\item ")
            # use regex to only replace at begining of the strong r"^o "
            _string = re.sub(_regex_pattern_s, r"\\item ", _string)
            # Příkaz níže fungue, ale odrážka není proměnlivá
            # _string = re.sub(r"^o ", _string)
            _string_depth = _index
            break

    #print(_index)
    #print(_string_depth)
    #print(_current_level)

    # Adds dollar signs if the string is math equation
    # Not 100% correct
    for _math_symbol in MATH_SYMBOLS:
        if _math_symbol in _string:
            _string = _string.replace("\item ", "\item TODO%")
            break


    
    # Adds tabs for readibilyty
    _tabs_begin = ""
    if _string_depth != None:
        for i in range(_string_depth):
            _tabs_begin = _tabs_begin + "\t"
    _tabs_item = _tabs_begin + "\t"
    


    if _string_depth == None and _current_level != None:
        
        repeats = _current_level
        while repeats >= 0:
            global_list.append(r"\end{itemize}") # the last \end{itemize}
            repeats -= 1

        global_list.append("")
        print(_string)
        return _string_depth

    if _string_depth == None and _current_level == None:
        global_list.append("")
        print(_string)
        return _string_depth

    if _string_depth != None and _current_level == None:
        global_list.append("")
        global_list.append(_tabs_begin + r"\begin{itemize}")
        global_list.append(_tabs_item + _string)
        return _string_depth

    if _string_depth == _current_level:
        global_list.append(_tabs_item + _string)
        print(_string)
        return _string_depth

    if _string_depth > _current_level:
        global_list.append("")
        global_list.append(_tabs_begin + r"\begin{itemize}")
        global_list.append(_tabs_item + _string)
        print(_string)
        return _string_depth

    if _string_depth < _current_level:
        global_list.append(_tabs_item + r"\end{itemize}")
        global_list.append("")
        global_list.append(_tabs_item + _string)
        print(_string)
        return _string_depth
    
    
    print(_string)
    return _string_depth


current_depth = None
for i in a:
    
    current_depth = bullets(i, current_depth)

output = "\n".join(global_list)


with open("output.txt", "w", encoding="utf-8") as file:
    data = file.write(output)