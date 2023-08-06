# s3imageresizer

A python module to import and resize pictures into amazon S3 storage.

## Synopsis

Typical usecase: fetch a bunch of image and generate thumbnails of various
sizes for each of them, stored in S3.

```
from s3imageresizer import S3ImageResizer

from boto import s3
s3_conn = s3.connect_to_region(...)

# Initialize an S3ImageResizer:
i = S3ImageResizer(s3_conn)

urls = [
    'http://www.gokqsw.com/images/picture/picture-3.jpg',
    'http://www.gokqsw.com/images/picture/picture-4.jpg'
]

for url in urls:

    # Fetch image into memory
    i.fetch(url)

    # Apply the image EXIF rotation, if any
    i.orientate()

    # Resize this image, store it to S3 and return its url
    url1 = i.resize(
        width=200
    ).store(
        in_bucket='my-images',
        key_name='image-w200-jpg'
    )

    # Do it again, with a different size
    url2 = i.resize(
        height=400
    ).store(
        in_bucket='my-images',
        key_name='image-h200-jpg'
    )
```

## More explanation

For method parameters, see the code (there isn't much of it ;-)

S3ImageResizer does all image operations in-memory, without writing images to
disk.

S3ImageResizer uses PIL, has reasonable defaults for downsizing images and
handle images with alpha channels nicely.

## Installation

s3imageresizer requires Pillow, which in turn needs external libraries.
On ubuntu, you would for example need:

```
sudo apt-get install libjpeg8 libjpeg8-dev libopenjpeg-dev
```

Then

```
pip install s3imageresizer
```

## Author

erwan at lemonnier dot se