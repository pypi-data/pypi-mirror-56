import glob
from PIL import Image
import click


def get_images(images):
    all_images = []
    for image in images:
        if "*" in image or "?" in image:
            all_images += glob.glob(image)
        else:
            all_images.append(image)
    return all_images

def get_ims(images):
    images = get_images(images)
    ims = []
    for image in images:
        im = Image.open(image)
        ims.append(im)
    return ims

def pack_pdf(images, output):
    ims = get_ims(images)
    ims[0].save(output, save_all=True, append_images=ims[1:])

def pack_gif(images, output, duration=1000, loop=0):
    ims = get_ims(images)
    ims[0].save(output, save_all=True, duration=duration, loop=loop, append_images=ims[1:])

def pack_tiff(images, output):
    ims = get_ims(images)
    ims[0].save(output, save_all=True, compression="tiff_deflate", append_images=ims[1:])


@click.command()
@click.option("-o", "--output", required=True, help="Result pdf filename.")
@click.option("-d", "--duration", type=float, default=1000, help="The time to display the current frame of the GIF, in milliseconds. Default to 1000.")
@click.option("-l", "--loop", type=int, default=0, help="The number of times the GIF should loop. 0 means that it will loop forever. Default to 0.")
@click.argument("images", nargs=-1, required=True)
def imagespack(output, duration, loop, images):
    """Package images into one PDF file or GIF file or TIFF file.
    """
    if output.lower().endswith(".gif"):
        pack_gif(images, output, duration, loop)
    elif output.lower().endswith(".tif") or output.lower().endswith(".tiff"):
        pack_tiff(images, output)
    else:
        pack_pdf(images, output)

if __name__ == "__main__":
    imagespack()
