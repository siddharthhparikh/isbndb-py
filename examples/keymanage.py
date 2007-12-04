import sys, optparse
# XXX
# For debug purposes only, remove when setup.py is incorporated
sys.path.insert(0,'..')
from isbndb import keys

def handleopts():
    usage = '''keytool [option] [keyfile]
No options defaults to list keys'''
    parser = optparse.OptionParser(usage)
    parser.add_option('-a', '--add', dest='add', default = '',
        help="Add a key to the keyfile")
    parser.add_option('-r', '--remove', dest='remove', default = '',
        help="Remove specified key from the keyfile")
    parser.add_option('-l', '--list', dest='list', action='store_true',
        default=True, help='List keys in the file')
    return parser.parse_args()

def main():
    options, args = handleopts()

    if args: kfname = args[0]
    else: kfname = None
    keys.loadKeys(kfname)

    if options.add:
        if keys.addKey(options.add):
            print "Successfully added key: %s" % (options.add)
            keys.saveKeys()
            sys.exit(0)
        else:
            print "Invalid key: %s, exiting" % (options.add)
            sys.exit(1)

    elif options.remove:
        # Note on implementation this will call keys.remove(key) in a try
        # block like above
        print "Option currently disabled, key removal is not yet implemented"
        sys.exit(1)

    else:
        i = 0
        for k in keys._KEYS:
            i += 1
            print '%s: %s' % (i, k)
        sys.exit(0)

if __name__ == '__main__':
    main()
