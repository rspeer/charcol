import unicodedata

category_set = set()
def get_category(ch):
    try:
        return unicodedata.name(ch).split()[0]
    except ValueError:
        return ''

for codept in range(2**16):
    cat = get_category(chr(codept))
    category_set.add(cat)

categories = sorted(list(category_set))

for codept in range(2**16):
    cat = get_category(chr(codept))
    idx = categories.index(cat)
    print('{}\t{}\t{}'.format(codept, idx, cat)) 

