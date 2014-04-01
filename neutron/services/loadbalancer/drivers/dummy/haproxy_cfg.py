# This file will read in the contents of an haproxy.cfg file
# and split it into blocks.

def createfrontend(frontendname, backendname, vip_ip, vip_port, vip_mode):
    """ We create a default frontend, and it will include
        a backend name in it.
    """
    list = []
    list.append(['option', 'tcplog'])
    list.append(['bind', vip_ip + ":" + vip_port])
    list.append(['mode', str(vip_mode).lower()])
    list.append(['default_backend', backendname])
    list.append(['option', 'forwardfor'])
    return list

def createbackend(backendname, vip_mode, balance):
    """ Create a backend with specified name and default options"""
    list = []
    list.append(['mode', str(vip_mode).lower()])
    list.append(['balance', str(balance)])
    list.append(['option', 'forwardfor'])
    list.append(['option', 'httpchk GET /'])
    return list


def iscomment(line):
    if (line.startswith("#")):
        return True
    else:
        return False
    
def isnewblock(line):
    if (line.startswith("global") or
         line.startswith("defaults") or
         line.startswith("frontend ") or
         line.startswith("backend ")):
        return True
    else:
        return False

def getblocktype(line):
    if (line.startswith("global")):
        return "global"
    elif (line.startswith("defaults")):
        return "defaults"
    elif (line.startswith("frontend")):
        return "frontend"
    elif (line.startswith("backend")):
        return "backend"
    return None

def isvalidblocktype(blocktype):
    print "in isvalidblocktype! blocktype is --> " + blocktype
    if not (blocktype == "global" or
            blocktype == "defaults" or
            blocktype == "frontend" or
            blocktype == "backend"):
        return False
    else:
        return True 

def getblockname(line):
    print line
    return line.split()[1]


def writeline(fp, line):
    fp.write(line+"\n")

def writelinewithprependtabs(fp, sectionline, tablength=1):
    line = "\t"*tablength + sectionline + "\n"
    fp.write(line)



def writehaproxycfgfile(filepath, block_name_content_map, block_name_type_map):
    fp = open(filepath, 'w+')
    for section in block_name_content_map:
        if (section == "global" or section == "defaults"):
            line = section
        else:
            line = block_name_type_map[section] + " " + section

        writeline(fp, line)
        # Then write out all new lines in this block.
        for sectionline in block_name_content_map[section]:
            secline = " ".join(sectionline)
            writelinewithprependtabs(fp, secline, 1)

        # At the end of a section, add an empty line
        writeline(fp, "")
    fp.close()




def loadhaproxycfgfile(haproxyfilepath):

    # This dict will have <blockname>:<blocktype> entries.
    # blockname will be the key and blocktype is the value.
    block_name_type_map = {}
    block_name_content_map = {}

    fp = open(haproxyfilepath)
    inblock = False
    while True:
        line = fp.readline()
        if not line:
            break   # EOF
        if iscomment(line):
            continue
        if line == "\n":
            print "blank line detected!"
            continue
        if isnewblock(line):
            inblock = True
            # Create a new block.
            blocktype = getblocktype(line)
            print "blocktype is " + blocktype
            if not isvalidblocktype(blocktype):
                msg = "Invalid blocktype " + blocktype + " encountered!"
                raise Exception(msg)
            if (blocktype is not "global" and blocktype is not "defaults"):
                blockname = getblockname(line)
                if blockname is None:
                    # Raise an exception
                    msg = "No blockname specified for " + blocktype + " block!"
                    raise Exception(msg)
                else:
                    # Add this to a dictionary/map.
                    if block_name_type_map.has_key(blockname):
                        msg = "Duplicate name " + blockname + " detected!"
                        raise Exception(msg)
                    else:
                        block_name_type_map[blockname] = blocktype  
                        block_name_content_map[blockname] = []     
            else: #blocktype is global or defaults - and has no name.
                blockname = blocktype
                if block_name_type_map.has_key(blockname):
                    msg = "Duplicate block " + blockname + " detected!"
                    raise Exception(msg)
                else:
                    block_name_type_map[blockname] = blocktype
                    block_name_content_map[blockname] = []
            # Add this to the map.
        else: # This line isn't the start of a new block.
            # If we are not already in a block, raise exception.
            if not inblock:
                msg = "Out of block entry detected!"
                raise Exception(msg)
            # Else, add this to current block.
            print "adding line to map.. blocktype is " + blocktype + " and blockname is " + blockname
            print "line is --> " + line
            block_name_content_map[blockname].append(line.split())
            continue

    # At the end, return a list of two dictionaries.
    rlist = [block_name_type_map, block_name_content_map]
    fp.close()
    return rlist


#blk_name_t_map, blk_name_c_map = loadhaproxycfgfile("./haproxy.cfg")


# Let's print out both maps at the end.
#print blk_name_c_map
#print blk_name_t_map


# Finally, let's write out the sections to a file!
#writehaproxycfgfile("./haproxy.cfg.out", blk_name_c_map, blk_name_t_map)
