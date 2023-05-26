from support.aopen_ai_controller import OpenAIGenerator
from support.camera_controller import Camera

# ------------------------------------------------------------------------------

key = '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'

generator = OpenAIGenerator(key)
camera = Camera(generator, key='c')
camera.continuous_read()
