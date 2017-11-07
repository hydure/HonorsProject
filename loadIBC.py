import cPickle
import csv, string

if __name__ == '__main__':
    [lib, con, neutral] = cPickle.load(open('ibcData.pkl', 'rb'))

    # how to access sentence text
    print 'Liberal examples (out of ', len(lib), ' sentences): '
    #for tree in lib[0:5]:
        #print tree.get_words()

    print '\nConservative examples (out of ', len(con), ' sentences): '
    #for tree in con[0:5]:
        #print tree.get_words()

    print '\nNeutral examples (out of ', len(neutral), ' sentences): '
    #for tree in neutral[0:5]:
        #print tree.label
        #print tree.get_words()

    # how to access phrase labels for a particular tree
    #ex_tree = lib[0]

    #print '\nPhrase labels for one tree: '

    # see treeUtil.py for the tree class definition
    #for node in ex_tree:

        # remember, only certain nodes have labels (see paper for details)
        #if hasattr(node, 'label'):
            #print node.label, ': ', node.get_words()
    
    f = open('ibcData.csv', 'w')
    #for data in [lib, con, neutral]:
    for data in [lib, con]:
        for tree in data:
            f.write(tree.label + ',' + tree.get_words().translate(None, string.punctuation) + '\n')
            #f.write(tree.label + '\t' + tree.get_words() + '\n')
    f.close()