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
def recursive_dir(path, ext):
    r = []
    for f in os.listdir(path):
        jf = os.path.join(path, f)
        if os.path.isdir(jf):
            r += recursive_dir(jf, ext)
        elif os.path.isfile(jf) and not jf.lower().endswith(ext):
            r.append(jf)
    return r
def tagger(path, tags):
    window = 'image'
    files = recursive_dir(path, '.txt')
    files.sort()
    num_files = len(files)
    img_tags = []
    img_tag_files = []
    for i,im in enumerate(files):
        img_tags.append(set())
        tagfile = os.path.splitext(im)[0]+'.txt'
        img_tag_files.append(tagfile)
        if os.path.isfile(tagfile):
            with open(tagfile, 'r') as f:
                img_tags[i] = {
                        t for t in f.read().strip().split(' ') if len(t) > 0
                }
    i = 0
    cv2.namedWindow(window, cv2.WINDOW_NORMAL)
    while True:
        file = files[i]
        img_tag_file = img_tag_files[i]
        img_tag = img_tags[i]
        img = cv2.imdecode(cv2.numpy.fromfile(file), cv2.IMREAD_UNCHANGED)
        cv2.imshow(window, img)
        while True:
            info_str = file + ' ' + str(img_tag)
            print(info_str)
            cv2.setWindowTitle(window, info_str)
            k = -1
            while k == -1:
                k = cv2.waitKey(50)
                if cv2.getWindowProperty(window,cv2.WND_PROP_VISIBLE) < 1:
                    return
            if k in tags:
                if tags[k] in img_tag:
                    img_tag.remove(tags[k])
                else:
                    img_tag.add(tags[k])
            elif k == nav_clear:
                img_tag.clear()
            elif k == 27: # ESC # 8 <- # 13 enter
                return
            elif k == nav_next:
                i += 1
                if i >= num_files:
                    i = 0
                break
            elif k == nav_prev:
                i -= 1
                if i < 0:
                    i = num_files-1
                break
            # always keeps text files in sync
            with open(img_tag_file, 'w') as f:
                for t in img_tag:
                    f.write(t + ' ')
tagger(path, tags)
