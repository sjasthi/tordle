"""Author: Nalongsone Danddank, Final Project, begin on Feb 2 2022, end on April 27, 2022, ICS499 METRO STATE """
from collections import OrderedDict

# telugu.py primarily deals with splitting an input string
# into a series of logical characters
# contact Siva.Jasthi@metrostate.edu and
# nalongsone.danddank@my.metrostate.edu
# for any clarifications on
# telugu processing logic used in these functions.
def getTeluguLogicalChars(word):
    codeChars = parseToCodePoints(word)
    results = []
    for v in codeChars.values():
        l = list(v.values())
        temp = ""
        for code in l:
            temp += chr(code)
        results.append(temp)
    return results


def parseToCodePoints(word):
    word_array = explodeTelugu(word)
    i = 0
    logical_chars = OrderedDict([])
    ch_buffer = OrderedDict([])
    while i < len(word_array):
        current_ch = word_array[i]
        i += 1
        ch_buffer[len(ch_buffer)] = current_ch
        if i == len(word_array):
            logical_chars[len(logical_chars)] = ch_buffer
            continue
        next_ch = word_array[i]
        if isDependent(next_ch):
            ch_buffer[len(ch_buffer)] = next_ch
            i += 1
            logical_chars[len(logical_chars)] = ch_buffer
            ch_buffer = OrderedDict([])
            continue
        if isHalant(current_ch):
            if isConsonant(next_ch):
                if i < len(word_array):
                    continue
                ch_buffer[len(ch_buffer)] = current_ch
            logical_chars[len(logical_chars)] = ch_buffer
            ch_buffer = OrderedDict([])
            continue
        else:
            if isConsonant(current_ch):
                if isHalant(next_ch) or isDependentVowel(next_ch):
                    if i < len(word_array):
                        continue
                    ch_buffer[len(ch_buffer)] = current_ch
                logical_chars[len(logical_chars)] = ch_buffer
                ch_buffer = OrderedDict([])
                continue
            else:
                if isVowel(current_ch):
                    if isDependentVowel(next_ch):
                        ch_buffer[len(ch_buffer)] = next_ch
                        i += 1
                    logical_chars[len(logical_chars)] = ch_buffer
                    ch_buffer = OrderedDict([])
                    continue
        logical_chars[len(logical_chars)] = ch_buffer
        ch_buffer = OrderedDict([])
    return logical_chars


def explodeTelugu(word):
    result = []
    for w in word:
        result.append(ord(w))
    return result


def isConsonant(ch):
    return ch >= 0xC15 and ch <= 0xC39


def isDependentVowel(ch):
    return ch >= 0xC3E and ch <= 0xC4C


def isDependent(ch):
    return (ch == 0xC01 or ch == 0xC02) or ch == 0xC03


def isVowel(ch):
    return ch >= 0xC05 and ch <= 0xC14


def isHalant(ch):
    return ch == 0xC4D


def isTeluguNumber(ch):
    return ch >= 0xC66 and ch <= 0xC6F


def isTelugu(ch):
    return (ch >= 0x0C00 and ch <= 0xC7F) or (ch == 0x200C)


def isTeluguWord(word):
    for i in range(len(word)):
        if not isTelugu(ord(word[i])):
            return False
    return True


def is_blank_Telugu(hexVal):
    return hexVal in ["c00", "c01", "c02", "c03", "c0d", "c11", "c29", "c34"]


def isEnglish(s):
    try:
        s.encode(encoding="utf-8").decode("ascii")
    except UnicodeDecodeError:
        return False
    else:
        return True


if __name__ == "__main__":
    tlg = "అమెరికాఆస్ట్రేలియా"
    ghy = getTeluguLogicalChars(tlg)
    print(ghy)
    ind = ["అ", "మె", "రి", "కా", "ఆ", "స్ట్రే", "లి", "యా"]
    print(ind == ghy)
