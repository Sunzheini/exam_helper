from support.aopen_ai_controller import OpenAIGenerator
from support.camera_controller import Camera

# ------------------------------------------------------------------------------

key = None

generator = OpenAIGenerator(key)
camera = Camera(generator, key='c')
camera.continuous_read()
