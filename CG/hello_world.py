import moderngl
import numpy as np
from PIL import Image

def save_pic(fbo):
    image = Image.frombytes('RGB', fbo.size, fbo.read(components=3))
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    image.save('hello_world.png')

def main():
    ctx = moderngl.create_standalone_context()

    prog = ctx.program(vertex_shader="""
        #version 140
        in vec3 in_position;
        in vec3 in_color;
        out vec3 color;
        void main() {
            gl_Position = vec4(in_position, 1.0);
            color = in_color;
        }
        """,
        fragment_shader="""
        #version 140
        in vec3 color;
        out vec4 FragColor;
        void main() {
            FragColor = vec4(color, 1.0);
        }
    """)

    vertices = np.array([
        0.0, 1.0, 0.0,
        1.0, 0.0, 0.0,
        -1.0, -1.0, 0.0,
        0.0, 1.0, 0.0,
        1.0, -1.0, 0.0,
        0.0, 0.0, 1.0,
    ], dtype='f4')

    vbo = ctx.buffer(vertices)
    vao = ctx.simple_vertex_array(prog, vbo, 'in_position', 'in_color')
    fbo = ctx.framebuffer(color_attachments=[ctx.texture((1024, 1024), 4)])
    fbo.use()
    fbo.clear(1.0, 1.0, 1.0, 1.0)
    vao.render(moderngl.TRIANGLES)

    save_pic(fbo)

if __name__ == "__main__":
    main()
