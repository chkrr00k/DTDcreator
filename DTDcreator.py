import xml.etree.ElementTree as ET
import sys
import getopt
import collections

LICENSE_MESSAGE="""
    #############################################################
    #                                                           #
    #   This program is relased in the GNU GPL v3.0 license     #
    #   you can modify/use this program as you wish. Please     #
    #   link the original distribution of this software. If     #
    #   you plan to redistribute your modified/copied copy      #
    #   you need to relased the in GNU GPL v3.0 licence too     #
    #   according to the overmentioned licence.                 #
    #                                                           #
    #   "PROUDLY" MADE BY chkrr00k (i'm not THAT proud tbh)     #
    #                                                           #
    #############################################################
    #                                                           #
    #                                                           #
    #                            YEE                            #
    #                                                           #
    #                                                           #
    #############################################################
    """
HELP_MESSAGE = """Help:
Create .DTD grammar file for a given .XML file.
-i, --ifile <file>            the input file. MUST be specified
-o, --ofile <file>            the output file. Is overriden by the field 
                              in the XML 
                              file if specified. Defaults to schema.dtd
-c, --console                 write on stdout instead than on 
                              the specified file.
--force-ofile-name            Avoid the override of the output file name by
                              the field on the XML.
                              A file output must be present for this
--force-dtd-type <type>        force the use of a specific type for 
                              the type attribute
                              Defaults at "CDATA".
                              BE CAREFUL no type check is done on this
-s, --hide-suggestion         hide the suggestion for the header to link
                              the DTD file to the XML
-h, --help                    display this useful help
-l                            Shows the license
"""
class StringBuffer:
    def __init__(self, input=""):
        self.storage = []
        if input != "":
            self.storage.append(input)
    def append(self, input):
        self.storage.append(input)
    def toString(self):
        return "\n".join(self.storage)

class Node:
    def __init__(self, name):
        self.name = name
        self.times = 0
        self.attrib = dict()
        self.hasText = False
        self.children = list()
        
    def __str__(self):
        return self.name + " " + str(self.times) + " " + str(self.attrib) + " " + str(self.hasText) + " " + str(self.children)
    def __unicode__(self):
        return self.name + " " + str(self.times) + " " + str(self.attrib) + " " + str(self.hasText) + " " + str(self.children)
    def __repr__(self):
        return self.name + " " + str(self.times) + " " + str(self.attrib) + " " + str(self.hasText) + " " + str(self.children)
        
def scanNode(name, inner):
    if name.tag in tree:
        t = tree[name.tag]
    else:
        t = Node(name.tag)
        tree[name.tag] = t

    t.times += 1
    t.children = list(inner)

    if name.text == None or name.text.strip() == "":
        t.hasText = t.hasText or False
    else:
        t.hasText = True 
    if len(name.attrib) > 0:
        for a in name.attrib:
            if a in t.attrib:
                t.attrib[a] += 1
            else:
                t.attrib[a] = 1

def printTree(tree, type):
    global sb
    for el, node in tree.items():
        if len(node.children) > 0:
            children = []
            if node.hasText:
                chil = "#PCDATA | " + " | ".join(list(set(node.children)))
            else:
                for c in node.children:
                    if c not in children:
                        children.append(c)
                    else:
                        children[children.index(c)] = c + "*"
                chil = ", ".join(children)
                
            sb.append("<!ELEMENT {} ({}{}>".format(node.name, chil, ")*" if node.hasText or node.times > 1 else ")"))
        else:
            sb.append("<!ELEMENT {} {}>".format(node.name, "(#PCDATA)" if node.hasText else "EMPTY"))
        if len(node.attrib) > 0:
            sb.append("<!ATTLIST {}".format(node.name))
            for a, n in node.attrib.items():
                sb.append("{} {} {}".format(a, type, "#IMPLIED" if n < node.times else "#REQUIRED"))
            sb.append(">")
    
def explore(r):
    scanNode(r, [c.tag for c in list(r)])
    for c in r:
        explore(c)

def getArguments(argv):
    ofile = False
    result = {
        "inputFile" : None,
        "outputFile" : "schema.dtd",
        "console" : False,
        "type" : "CDATA",
        "fileOverride" : False,
        "verbose" : True
        }

    try:
        opts, args = getopt.getopt(argv, "hi:o:cls", ["help", "ifile=", "ofile=", "console", "force-dtd-type=", "force-ofile-name", "hide-suggestion"])
    except getopt.GetoptError:
        print("Error in arguments\n")
        print(HELP_MESSAGE)
        sys.exit(1)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(HELP_MESSAGE)
            sys.exit(0)
        elif opt in ("-l"):
            print(LICENSE_MESSAGE)
            sys.exit(0)
        elif opt in ("-i", "--ifile"):
            if arg.lower().endswith(".xml"):
                result["inputFile"] = arg
            else:
                sys.stderr.write("File must be a .xml file")
        elif opt in ("-o", "--ofile"):
            if arg.lower().endswith(".dtd"):
                result["outputFile"] = arg
                ofile = True
            else:
                sys.stderr.write("File must be a .dtd file")
        elif opt in ("-c", "--console"):
            result["console"] = True
        elif opt in ("--force-dtd-type"):
            result["type"] = arg
        elif opt in ("--force-ofile-name"):
            result["fileOverride"] = True
        elif opt in ("--hide-suggestion", "-s"):
            result["verbose"] = False

    if result["fileOverride"]:
        if not ofile:
            print(result["fileOverride"] , ofile)
            print("Error, you must specify the output file (option -o) with the --force-ofile-name\n")
            print(HELP_MESSAGE)
            sys.exit(3)
    if not result["inputFile"]:
        print("Needs an input file")
        print(HELP_MESSAGE)
        sys.exit(4)
    return result

args = getArguments(sys.argv[1:])
tree = collections.OrderedDict()
sb = StringBuffer()
try:
    t = ET.parse(args["inputFile"]).getroot()
except FileNotFoundError as err:
    sys.stderr.write("The inserted file doesn't exist or have problems: " + str(err))
    sys.exit(2)

explore(t)
printTree(tree, args["type"])

linkString = "<!DOCTYPE {} SYSTEM \"{}\">".format(t.tag, args["outputFile"])
if args["verbose"]:
    print("Add at the start of your XML file:\n",linkString)

if args["console"]:
    if args["verbose"]:
        print("Output:")
    print(sb.toString())
else:
    with(open(args["outputFile"], "w+")) as f:
        f.write(sb.toString())

