# (c) 2022 lopho
import os
import sys
import cv2
# python tagger.py path/to/dataset
hardcoded_path = ''
path = hardcoded_path or sys.argv[1]
assert os.path.isdir(path), f'{path} is not a path'
# set your keys as you want
nav_next = ord('w')
nav_prev = ord('q')
nav_clear = ord('e')
# if the tag is already set, pressing again removes it
tags = {
    ord('a'): 'bla',
    ord('b'): 'something',
    ord('c'): 'lol',
    # and so on
}
def tagger(path, tags):
    window = 'image'
    files = [ f for f in os.listdir(path) if not f.endswith('.txt') ]
    files.sort()
    num_files = len(files)
    img_tags = []
    img_tag_files = []
    tag_map = { tags[t]: t for t in tags }
    for i,im in enumerate(files):
        img_tags.append(set())
        tagfile = os.path.join(path, os.path.splitext(im)[0]+'.txt')
        img_tag_files.append(tagfile)
        if os.path.isfile(tagfile):
            with open(tagfile, 'r') as f:
                img_tags[i] = {
                        tag_map[t] for t in f.read().strip().split(' ') if t in tag_map
                }
    i = 0
    cv2.namedWindow(window, cv2.WINDOW_NORMAL)
    while True:
        file = files[i]
        img_tag_file = img_tag_files[i]
        img_tag = img_tags[i]
        img = cv2.imread(os.path.join(path, file))
        cv2.imshow(window, img)
        while True:
            info_str = file + ' ' + str([tags[t] for t in img_tag])
            print(info_str)
            cv2.setWindowTitle(window, info_str)
            k = -1
            while k == -1:
                k = cv2.waitKey(50)
                if cv2.getWindowProperty(window,cv2.WND_PROP_VISIBLE) < 1:
                    return
            if k in tags:
                if k in img_tag:
                    img_tag.remove(k)
                else:
                    img_tag.add(k)
            elif k == nav_clear:
                img_tag.clear()
            # always keeps text files in sync
            with open(img_tag_file, 'w') as f:
                for t in img_tag:
                    f.write(tags[t] + ' ')
            if k == 27: # ESC # 8 <- # 13 enter
                return
            if k == nav_next:
                i = min(i+1, num_files)
                break
            if k == nav_prev:
                i = max(i-1, 0)
                break
tagger(path, tags)
