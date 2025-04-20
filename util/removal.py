import sys
from PIL import Image, ImageSequence
from rembg import remove
from io import BytesIO

def remove_background_animation(input_path, output_path):
    original_gif = Image.open(input_path)
    frames = []

    for frame in ImageSequence.Iterator(original_gif):
        frame = frame.convert("RGBA")

        buf = BytesIO()
        frame.save(buf, format='PNG')
        img_bytes = buf.getvalue()

        removed_bytes = remove(img_bytes)

        removed_image = Image.open(BytesIO(removed_bytes)).convert("RGBA")

        transparent_frame = Image.new("RGBA", removed_image.size, (0, 0, 0, 0))
        transparent_frame.paste(removed_image, (0, 0), removed_image)
        frames.append(transparent_frame)

    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=original_gif.info.get("duration", 100),
        loop=0,
        disposal=2
    )

    print("完了")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("使い方: python gifRemoval.py input.gif output.gif")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    remove_background_animation(input_path, output_path)
