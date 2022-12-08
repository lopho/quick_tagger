# quick_tagger
Tag images using keyboard controls.
- Hit a letter key on your keyboard to add a tag, hit it again to remove it again.
- Saves tags as `<image_file_name>.txt` files in the same folder as the images.
- Loads already present text files with tags
- Tag files are instantly updated
- Tags and image file name are output to the terminal and in the window titlebar
```sh
python tagger.py path/to/dataset
```
Set tags by modifiying the following in tagger.py
```py
tags = {
    ord('a'): 'bla',
    ord('b'): 'something',
    ord('c'): 'lol',
    # and so on
}
```
Default Controls:
- `q` next image
- `w` previous image
- `e` clear tags
- `ESC` quit

Next, previous and clear can be user defined in tagger.py
```py
nav_next = ord('w')
nav_prev = ord('q')
nav_clear = ord('e')
```

Dependencies: `opencv-python`
