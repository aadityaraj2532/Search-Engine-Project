import sys
import requests
from bs4 import BeautifulSoup

# this fuction for fetcheing text from the given url
def findText(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup.find_all(["script", "style"]):
        tag.decompose()
    return soup.get_text()

# this is for count the freq of each word in the text
def wordCount(text):
    words = text.lower().split()
    freqWord = {}
    for word in words:
        freqWord[word] = freqWord.get(word, 0) + 1
    return freqWord

# this function updateing polynomial hash adding one character at a time
def charAdd(currVal, currPow, ch):
    b = 53
    last = 1 << 64
    asciNum = ord(ch)
    newVal = (currVal + asciNum * currPow) & (last - 1)
    newPow = (currPow * b) & (last - 1)
    return newVal, newPow

# this function calculate the hash polynomial of a word
def polyHash(word):
    val = 0
    pow = 1
    for letter in word:
        val, pow = charAdd(val, pow, letter)
    return val

# it create bit array of 64 length
def BitArray(freqWord):
    bit = [0] * 64
    for word, freq in freqWord.items():
        Wordhash = polyHash(word)
        i = 0
        while i < 64:
            bitVal = Wordhash & (1 << i)
            if bitVal != 0:
                bit[i] = bit[i] + freq
            else:
                bit[i] = bit[i] - freq
            i = i + 1
    return bit

# this function convert the bit array to binary string
def hashConversion(bit):
    binStr = ""
    for i in range(63, -1, -1):
        if bit[i] > 0:
            binStr += "1"
        else:
            binStr += "0"
    return binStr

# this is for simhash conversion of the text
def simHashing(wordfreq):
    bits = BitArray(wordfreq)
    return hashConversion(bits)

def totCommonBit(a, b):
    count = 0
    for i in range(64):
        if a[i] == b[i]:
            count += 1
    return count

url1 = sys.argv[1]
url2 = sys.argv[2]

text1 = findText(url1)
text2 = findText(url2)

freq_1 = wordCount(text1)
freq_2 = wordCount(text2)

h1 = simHashing(freq_1)
h2 = simHashing(freq_2)

common = totCommonBit(h1, h2)

print("Simhash first:", h1)
print("Simhash Second:", h2)
print("Common bits:", common)