#oneline quicksort

quicks = lambda l: quicks([x for x in l[1:] if x <= l[0]]) + [l[0]] + quicks([x for x in l if x > l[0]]) if l else []
