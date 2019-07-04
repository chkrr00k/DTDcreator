# DTDautosyntax
This program create a DTD grammar from an XML file.
Simply call this program with proper arguments and it will generate a new file with the appropriate syntax.
Keep in mind that it *can't* understand the type of each tag. Defaults are CDATA, so you could have to manually modify those.

## Usage


### Examples:  
`DTDautosyntax -i filein.xml -o fileout.dtd` to convert filein.xml into fileout.xsd if a field is not specified  
`DTDautosyntax -i filein.xml -o fileout.dtd --force-ofile-name` to force the name  
`DTDautosyntax -i filein.xml` to convert filein.xml into schema.xsd  
`DTDautosyntax -i filein.xml -c` to convert filein.xml to stdout  
`DTDautosyntax -i filein.xml -o fileout.dtd -s` to convert filein.xml into fileout.xsd if a field is not specified and hide the suggestion for the linking to the xml file  

### Help:  
`-i, --ifile <file>`            the input file. MUST be specified  
`-o, --ofile <file>`            the output file. Is overriden by the field in the XML file if specified. Defaults to schema.dtd  
`-c, --console`                 write on stdout instead than on the specified file.  
`--force-ofile-name`            Avoid the override of the output file name by the field on the XML. A file output must be present for this  
`--force-dtd-type <type>`       force the use of a specific type for the type attribute. Defaults at "CDATA". **BE CAREFUL** no type check is done on this  
`-s, --hide-suggestion`         hide the suggestion for the header to link the DTD file to the XML
`-h, --help`                    display this useful help  
`-l`                            Shows the license  

## License
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
