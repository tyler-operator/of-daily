# render

Source for the slide images. This does NOT run in CI, on purpose.

Rendering is bespoke per subject and depends on fonts (Inter, Lora) and
cairosvg. Keeping it out of the Action means a font change can never cost
you a post.

Build locally, eyeball the JPEGs, commit them to posts/.

    pip install cairosvg pillow
    python social.py        # writes ig/*.jpg at 1080x1350

Hard rules for a carousel:
  - every slide exactly 1080 x 1350
  - JPEG, RGB, under 8MB
  - Instagram crops all slides to slide 1's ratio
