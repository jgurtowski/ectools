
from collections import namedtuple
from textwrap import wrap

from operator import add, attrgetter
from itertools import repeat

ParsedArgs = namedtuple("ParsedArgs", ["argmap",
                                       "remaining"])

CLArgument = namedtuple("CLArgument", ["name",
                                       "internal_name",
                                       "type",
                                       "default",
                                       "description"])

def parseArgs(cllist, arg_proto, arg_proto_map={}, argmap = {}):
    '''Parse args from commandline
    Usually takes sys.argv[1:] as cllist
    arg_proto is a list of type CLArgument
    '''

    def etoi(a):
        '''Maps argument's external (cli name) to internal name'''
        return arg_proto_map[a].internal_name

    ##starting out, init argmap and arg_proto_map
    if not bool(argmap):
        argmap = dict(map(attrgetter("internal_name","default"), arg_proto))
        arg_proto_map = dict(zip(map(attrgetter("name"),arg_proto),arg_proto))

    if not cllist:
        cllist = []
        
    if len(cllist) == 0  or not cllist[0].startswith("-"):
        return ParsedArgs(argmap,cllist)

    #remove the "-"
    cur = cllist[0][1:]
    
    if not cur in arg_proto_map:
        raise Exception, "Unknown argument '%s'\n" % cur

    if arg_proto_map[cur].type == argflag:
        argmap[etoi(cur)] = True
        return parseArgs(cllist[1:], arg_proto, arg_proto_map, argmap)

    if "=" in cur:
        k,v = cur.split("=")
        argmap[etoi(k)] = arg_proto_map[k].type(v)
        return parseArgs(cllist[1:],arg_proto,arg_proto_map, argmap)

    if not len(cllist) > 1:
        raise Exception, "Dangling arg '%s'\n" % cur

    argmap[etoi(cur)] = arg_proto_map[cur].type(cllist[1])
    return parseArgs(cllist[2:], arg_proto, arg_proto_map, argmap)


def getHelpStr(description, arguments):
    '''description should just be a string
    
    arguments should be a list of type CLArgument
    '''
    
    LEFT_COL_PADDING=25
    WRAP_SIZE = 50

    ostring = description + "\n\n"

    #descriptions can span multiple rows,
    #the first row contains the argument name
    #the next just and empty string
    def once(param, times=0):
        while True:
            if times == 0:
                times += 1
                yield param
            else:
                yield ""

    #add an empty string to the beginning of multiline descriptions
    #that are returned by 'wrap'
    wrap_s = WRAP_SIZE
    d =  reduce( add, map(lambda x: zip(once("-"+x.name),
                                        wrap(x.description, wrap_s)),arguments))

    pad = LEFT_COL_PADDING
    ostring += "\n".join(map(lambda (left,right): "".join((left.ljust(pad),right)), d))
    
    return ostring
    

def argrange(a):
    if ":" in a:
        arr = map(int,a.split(":"))
        if not len(arr) == 3:
            raise Exception, "Invalid range, must be in format start:stop:step"
        return range(*arr)
    elif "," in a:
        arr = map(int,a.split(","))
        return arr
    
    return [int(a)]

def arglist(a):
    delim = None
    if "," in a:
        delim = ","
    return a.split(delim)

def argflag():
    pass
