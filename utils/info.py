from HTMLParser import HTMLParser
import urllib2, json

#-----------------THEYSAIDSO-----------------

# returns a quote from a specific category and its author from theysaidso API
# 8 total categories: inspire, management, sports, life, funny, love, art, students
def getCatQOD(category):
    # entire url = head + end
    head = "http://quotes.rest/qod.json?category="
    end = category
    newURL = head + end
    # returns the contents of the search
    page = urllib2.urlopen(newURL).read()
    # returns the article with the corresponding title
    d = json.loads(page)
    quote = d["contents"]["quotes"][0]["quote"]
    #print quote
    author = d["contents"]["quotes"][0]["author"]
    #print author
    return quote + " -" + author

#print getCatQOD("sports")

# returns a quote and its author from theysaidso API
def getQOD():
    newURL = "http://quotes.rest/qod.json"
    # returns the contents of the search
    page = urllib2.urlopen(newURL).read()
    # returns the article with the corresponding title
    d = json.loads(page)
    quote = d["contents"]["quotes"][0]["quote"]
    #print quote
    author = d["contents"]["quotes"][0]["author"]
    #print author
    return quote + " -" + author

#print getQOD()

#-----------------WIKIQUOTES-----------------

'''
https://en.wikiquote.org/w/api.php?format=json&action=opensearch&search=one_flew_over_the_cuckoos_nest&suggest=true&redirects=resolve
'''

# returns a string with all spaces replaced with an underscore
def convertTerm(term):
    return term.replace(" ", "_")

#print convertTerm("Marie Antoinette")

# returns a list of wikiquotes pages' urls for the search term
def getQuotePageBySearch(term):
    term = convertTerm(term)
    head = "https://en.wikiquote.org/w/api.php?format=json&action=opensearch&search="
    end = "&suggest=true&redirects=resolve"
    newURL = head + term + end
    page = urllib2.urlopen(newURL).read()
    d = json.loads(page)
    return d[-1]

#print getQuotePageBySearch("Marie Antoinette")

# returns a list of the wikiquotes page titles for the search term
# e.g. https://en.wikiquote.org/wiki/Ken_Kesey becomes Ken_Kesey
def getQuoteWikiPage(term):
    term = convertTerm(term)
    pages = getQuotePageBySearch(term) #list
    ctr = 0
    while ctr != len(pages):
        pages[ctr] = pages[ctr].split("https://en.wikiquote.org/wiki/")[-1]
        ctr +=1
    return pages

#print getQuoteWikiPage("One flew over the cuckoos nest")

'''
https://en.wikiquote.org/w/api.php?format=json&action=parse&page=Ken_Kesey&section=1
'''

# returns quotes section of the wikiquotes page
def getQuotesBySearch(term):
    pages = getQuoteWikiPage(term)
    quotes = []
    for wikipage in pages:
        head = "https://en.wikiquote.org/w/api.php?format=json&action=parse&page="
        end = "&section=1"
        newURL = head + wikipage + end
        page = urllib2.urlopen(newURL).read()
        d = json.loads(page)
        quotes.append(d["parse"]["text"]["*"])
    return quotes

#print getQuoteBySearch("marie antoinette")

# helper functions to remove anchor href tags
class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    parser = HTMLParser()
    html = parser.unescape(html)
    s = MLStripper()
    s.feed(html)
    return s.get_data()

# returns a single quote from each wikiquotes page
def firstQuote(term):
    pages = getQuotesBySearch(term)
    quotes = []
    for wikipage in pages:
        if "<strong>" in wikipage:
            quoteStart = wikipage.index("<strong>")
            quoteEnd = wikipage.index("</strong>")
            quote = strip_tags(wikipage[quoteStart+8:quoteEnd])
            #print quote
            quotes.append(quote)
        elif "<b>" in wikipage:
            quoteStart = wikipage.index("<b>")
            quoteEnd = wikipage.index("</b>")
            quote = strip_tags(wikipage[quoteStart+3:quoteEnd])
            #print quote
            quotes.append(quote)
        else:
            quotes.append("No important quotes for this search term")
    return quotes

#print firstQuote("one flew over the cuckoos nest")

# returns the next quote in wikiquotes page if it exists
def nextQuote(term):
    pages = getQuotesBySearch(term)
    quotes = []
    for wikipage in pages:
        if "<strong>" in wikipage:
            wikipage = wikipage[wikipage.index("</strong>")+9:]
            if "<strong>" in wikipage:
                quoteStart = wikipage.index("<strong>")
                quoteEnd = wikipage.index("</strong>")
                quote = strip_tags(wikipage[quoteStart+8:quoteEnd])
                #print quote
                quotes.append(quote)
        elif "<b>" in wikipage:
            wikipage = wikipage[wikipage.index("</b>")+4:]
            if "<b>" in wikipage:
                quoteStart = wikipage.index("<b>")
                quoteEnd = wikipage.index("</b>")
                quote = strip_tags(wikipage[quoteStart+3:quoteEnd])
                #print quote
                quotes.append(quote)
        else:
            quotes.append("No more important quotes for this search term")
    return quotes

#print nextQuote("one flew over the cuckoos nest")
