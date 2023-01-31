# Drafts

def drafts(files, hana):
    for filename, f in files:
        if 'draft' in f:
            hana.files.remove(filename)



