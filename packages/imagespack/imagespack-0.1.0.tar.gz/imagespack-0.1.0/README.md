# image2pdf

Package images into one PDF file or GIF file or TIFF file.


## Install

```shell
pip install imagespack
```

## Usage

```shell
Usage: imagespack.py [OPTIONS] IMAGES...

  Package images into one PDF file or GIF file or TIFF file.

Options:
  -o, --output TEXT     Result pdf filename.  [required]
  -d, --duration FLOAT  The time to display the current frame of the GIF, in
                        milliseconds. Default to 1000.
  -l, --loop INTEGER    The number of times the GIF should loop. 0 means that
                        it will loop forever. Default to 0.
  --help                Show this message and exit.
```

## Example

*Convert all .jpg files into result.pdf file.*

```shell
imagespack -o result.pdf *.jpg
```


## Releases

### v0.1.0 2019/12/01

- First release.
- Allow pack into one pdf, one gif or one tiff file.
