from .tag import Tag

TAGTYPE = 'DATATYPE'
VALUES = 'VALUES'

def encodeJSON(tag):
        if isinstance(tag, Tag):
                return toJSONString(tag, True)
        else:
                return __formatJSON(tag)

def toJSONString(tag, format=False):
	if not isinstance(tag, Tag):
		raise ValueError("tag must be an instance of Tag")
	keys = tag.getKeys()
	JSONSTRING = "{"
	for i,key in enumerate(keys):
                data = tag.getData(key)
                if isinstance(data, Tag):
                        data = toJSONString(data)
                        JSONSTRING += '"'+str(key)+'": '+str(data)
                elif type(data) is list:
                        JSONSTRING += '"'+str(key)+'": ['
                        for j,d in enumerate(data):
                                JSONSTRING +=str(d)
                                if j is not len(data)-1:
                                        JSONSTRING += ','
                        JSONSTRING +=']'
                elif type(data) in (frozenset, set, tuple):
                        t = Tag()
                        t.addData(TAGTYPE, type(data).__name__)
                        t.addData(VALUES, list(data))
                        t = toJSONString(t)
                        JSONSTRING += '"'+str(key)+'": '+str(t)
                elif type(data) is dict:
                        t = Tag()
                        t.addData(TAGTYPE, type(data).__name__)
                        for k, value in data.items():
                                t.addData(k, value)
                        t = toJSONString(t)
                        JSONSTRING += '"'+str(key)+'": '+str(t)
                else:
                        if type(data) is complex:
                                data = str(data)
                                data = data.replace('(',"")
                                data = data.replace(')',"")
                        JSONSTRING += '"'+str(key)+'": "'+str(data)+'"'
                if i is not len(keys)-1:
                        JSONSTRING += ','


	JSONSTRING += '}'
	if format:
		return __formatJSON(JSONSTRING)
	return JSONSTRING

def __formatJSON(JSONSTRING):
	fJSON = ''
	tabs = 0
	running = True
	i = 0
	while i < len(JSONSTRING):
		char = JSONSTRING[i]
		if char is '{':
			fJSON += char
			fJSON +='\n'
			tabs+=1
			fJSON = insertTabs(fJSON, tabs)
		elif char is '}':
			fJSON += '\n'
			tabs-=1
			fJSON = insertTabs(fJSON, tabs)+char
		elif char is '[':
			fJSON += char
			fJSON +='\n'
			tabs+=1
			fJSON = insertTabs(fJSON, tabs)
		elif char is ']':
			fJSON += '\n'
			tabs-=1
			fJSON = insertTabs(fJSON, tabs)+char
		elif char is ',':
			fJSON += char+'\n'
			fJSON = insertTabs(fJSON, tabs)
		elif char is '"':
			nextpos = __charPos('"', JSONSTRING, i+1)
			fJSON += __substring(JSONSTRING, i, nextpos+1)
			i = nextpos
		else:
			fJSON += char
		i += 1

	return fJSON

def insertTabs(STRING, tabnum):
	for i in range(0, tabnum):
		STRING += '    '
	return STRING

def decodeJSON(JSON):
        tag=Tag()
        nextpos=0
        dataName = None
        i=0
        while i < len(JSON):
                char = JSON[i]
                if i < nextpos:
                        continue
                elif char is '"':
                        if dataName is None:
                                nextpos = __charPos('"', JSON, i+1)
                                dataName = __substring(JSON, i+1, nextpos)
                                i = nextpos
                        else:
                                nextpos = __charPos('"', JSON, i+1)
                                tag.addData(dataName, parseData(__substring(JSON, i+1, nextpos)))
                                i=nextpos
                                dataName = None
                elif char is '[':
                        if dataName is not None:
                                lst, i = parseList(JSON,i)
                                tag.addData(dataName, lst)
                                dataName = None
                elif char is '{':
                        if dataName is not None:
                                j, i = parseTag(JSON, i)
                                t = decodeJSON(j)
                                if t.keyExists(TAGTYPE):
                                        d=[]
                                        ttype = t.getData(TAGTYPE)
                                        if ttype == dict.__name__:
                                                d = {}
                                                for k in t.getKeys():
                                                        if k != TAGTYPE:
                                                                d[k] = t.getData(k)
                                        else:
                                                if ttype == set.__name__:
                                                        d= set(t.getData(VALUES))
                                                elif ttype == frozenset.__name__:
                                                        d= frozenset(t.getData(VALUES))
                                                elif ttype == tuple.__name__:
                                                        d= tuple(t.getData(VALUES))
                                        tag.addData(dataName, d)
                                else:
                                        tag.addData(dataName, t)
                                dataName = None
                i+=1
        return tag

def parseTag(JSON, index):
        i=index+1
        count=1
        while count > 0:
                c = JSON[i]
                if c is '{':
                        count += 1
                elif c is '}':
                        count -= 1
                i += 1
        return __substring(JSON, index, i),i

def parseList(JSON, index):
        lst = []
        skip=0
        nextpos = __charPos(']', JSON, index)
        i = index
        while i < nextpos:
                c=JSON[i]
                if ( c == "[" ):
                        i+=1
                        continue
                if c == ']':
                        break
                if c not in (' ',',','\n','\t','"',"'"):
                        a = __charPos(',', JSON, i)
                        b = __charPos('\n', JSON, i)
                        if a < b and a is not -1 or b is -1:
                                skip = a
                        else:
                                skip = b
                        lst.append(parseData(__substring(JSON, i, skip)))
                        i = skip
                elif c in ('"',):
                        skip = __charPos('"', JSON, i)
                        lst.append(parseData(__substring(JSON, i, skip)))
                        i=skip
                elif c in ("'",):
                        skip = __charPos("'", JSON, i)
                        lst.append(parseData(__substring(JSON, i, skip)))
                        i=skip
                else:
                        i+=1
        return (lst,i)

def parseData(s):
        if __isNumeric(s):
                return __toNumeric(s)
        else:
                return s
####################################################################
# String helper section
###################################################################
#Find the next instance of character
def __charPos(char, string, pos=0):
        for i in range(pos+1, len(string)):
                if string[i] is char:
                        return i
        return -1

def __substring(string, startpos=0, endpos=None):
        if endpos is None:
                endpos = len(string)
        return string[startpos : endpos]

def __toNumeric(s, noError=False):
        if not isinstance(s, str) or not __isNumeric(s):
                if noError:
                        return None
                else:
                       raise ValueError("Passed value is not a String or is not Numeric")
        if __isInteger(s):
                return int(s)
        elif __isFloat(s):
                return float(s)
        elif __isComplex(s):
                return complex(s)

def __isNumeric(s):
        return __isInteger(s) or __isFloat(s) or __isComplex(s)

def __isInteger(s):
        try:
                int(s)
                return True
        except ValueError:
                return False

def __isFloat(s):
        try:
                float(s)
                return True
        except ValueError:
                return False

def __isComplex(s):
        try:
                complex(s)
                return True
        except ValueError:
                return False
