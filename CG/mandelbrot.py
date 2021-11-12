import moderngl
import numpy as np
from PIL import Image

def save_pic(fbo):
    image = Image.frombytes('RGB', fbo.size, fbo.read(components=3))
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    image.save('mandelbrot.png')

def main():
    ctx = moderngl.create_standalone_context()

    prog = ctx.program(vertex_shader="""
        #version 140
        in vec2 in_position;
        out vec2 position;
        void main() {
            gl_Position = vec4(in_position, 0.0, 1.0);
            position = in_position;
        }
        """,
        fragment_shader="""
        #version 140
        in vec2 position;
        out vec4 FragColor;
        vec2 mult(vec2 z1, vec2 z2) {
            return vec2(z1.x * z2.x - z1.y * z2.y, z1.x * z2.y + z1.y * z2.x);
        }
        vec2 conj(vec2 z) {
            return vec2(z.x, -1.*z.y);
        }
        void main() {
            vec2 c = position * 2.;
            vec2 z = vec2(0., 0.);
            int n = 0;
            while (n < 20) {
                if (mult(z, conj(z)).x > 1000000.) {
                    break;
                }
                z = mult(z, z) + c;
                n += 1;
            }
            if (n == 20) {
                FragColor = vec4(0., 0., 0., 1.);
            }else {
                FragColor = vec4(n/20., 0., 0., 1.);
            }
        }
    """)

    vertices = np.array([
        0.0, 0.0,
        1.0, 1.0,
        -1.0, 1.0,
        -1.0, -1.0,
        1.0, -1.0,
        1.0, 1.0,
    ], dtype='f4')

    vbo = ctx.buffer(vertices)
    vao = ctx.simple_vertex_array(prog, vbo, 'in_position')
    w, h = 8092, 8092
    fbo = ctx.framebuffer(color_attachments=[ctx.texture((w, h), 4)])
    fbo.use()
    fbo.clear(1.0, 1.0, 1.0, 1.0)
    vao.render(moderngl.TRIANGLE_STRIP)

    save_pic(fbo)

if __name__ == "__main__":
    main()
