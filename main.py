from OpenGL.GL import * 
import glfw
import numpy as np

def create_native_window():
    glfw.init()

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)  
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    
    window = glfw.create_window(800, 600, 'yay', None, None)
    glfw.make_context_current(window)
    return window

window = create_native_window()

def setup_triangle():
    coords = [
        0, 0.5,
        -0.5, -0.5,
        0.5, -0.5
    ]

    itemsize = np.dtype('float32').itemsize

    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    coords_buffer = glGenBuffers(1)
    typed_coords = np.array(coords, dtype='float32')

    glBindBuffer(GL_ARRAY_BUFFER, coords_buffer)
    glBufferData(GL_ARRAY_BUFFER, itemsize * typed_coords.size, typed_coords, GL_STATIC_DRAW)
    # tell how data should be read
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, None)
    # get vertex variable location: in this case coords location
    coords_attrib_location = glGetAttribLocation(program, 'coords')
    # link variable with currently bound buffer on GL_ARRAY_BUFFER target (target=slot)
    glEnableVertexAttribArray(coords_attrib_location)


def load_shaders():
    with open('./shaders/vertex.glsl') as vertex_shader:
        vertex_src = vertex_shader.read()
    with open('./shaders/frag.glsl') as frag_shader:
        frag_src = frag_shader.read()

    vert_shader = glCreateShader(GL_VERTEX_SHADER)
    glShaderSource(vert_shader, vertex_src)
    glCompileShader(vert_shader)

    frag_shader = glCreateShader(GL_FRAGMENT_SHADER)
    glShaderSource(frag_shader, frag_src)
    glCompileShader(frag_shader)

    print(glGetShaderInfoLog(vert_shader))
    print(glGetShaderInfoLog(frag_shader))

    program = glCreateProgram()

    glAttachShader(program, vert_shader)
    glAttachShader(program, frag_shader)

    glLinkProgram(program)

    return program

program = load_shaders()
setup_triangle()

glUseProgram(program)

def draw():
    glClear(GL_COLOR_BUFFER_BIT)

    glDrawArrays(GL_TRIANGLES, 0, 3)


def main_loop():
    while not glfw.window_should_close(window):
        draw()
        glfw.swap_buffers(window)
        glfw.poll_events()
    
    glfw.terminate()


main_loop()