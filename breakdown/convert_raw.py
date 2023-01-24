import rawpy
import imageio

img_src = f"IMG_{str(input('Enter image #: '))}"

with rawpy.imread(f"{img_src}.CR3") as raw:
    rgb = raw.postprocess()
    imageio.imsave(f"{img_src}.JPEG", rgb)
