from OpenGL.GL import * 
import glfw
import numpy as np
from utils import load_image

def create_native_window():
    glfw.init()

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)  
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    
    window = glfw.create_window(800, 600, 'hello triangle', None, None)
    glfw.make_context_current(window)
    return window

window = create_native_window()

def setup_triangle():
    coords = np.array([
        0, 0.5,
        -0.5, -0.5,
        0.5, -0.5
    ], dtype=np.float32)

    colors = np.array([
        1, 0.5, 0.5,
        0.5, 1, 0.5,
        0.5, 0.5, 1
    ], dtype=np.float32)

    tex_coords = np.array([
        0.5, 0,
        0, 1,
        1, 1
    ], dtype=np.float32)

    itemsize = np.dtype('float32').itemsize

    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    vbo_id = glGenBuffers(3)

    glBindBuffer(GL_ARRAY_BUFFER, vbo_id[0])
    glBufferData(GL_ARRAY_BUFFER, itemsize * coords.size, coords, GL_STATIC_DRAW)
     # get vertex variable location: in this case coords location
    coords_attrib_location = glGetAttribLocation(program, 'coords')
    # tell how data should be read
    glVertexAttribPointer(coords_attrib_location, 2, GL_FLOAT, GL_FALSE, 0, None)
    # link variable with currently bound buffer on GL_ARRAY_BUFFER target (target=slot)
    glEnableVertexAttribArray(coords_attrib_location)

    # the same for colors
    glBindBuffer(GL_ARRAY_BUFFER, vbo_id[1])
    glBufferData(GL_ARRAY_BUFFER, itemsize * colors.size, colors, GL_STATIC_DRAW)
    colors_attrib_location = glGetAttribLocation(program, 'colors')
    glVertexAttribPointer(colors_attrib_location, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(colors_attrib_location)

    # the same for texture
    glBindBuffer(GL_ARRAY_BUFFER, vbo_id[2])
    glBufferData(GL_ARRAY_BUFFER, itemsize * tex_coords.size, tex_coords, GL_STATIC_DRAW)
    tex_coords_attrib_location = glGetAttribLocation(program, 'a_tex_coords')
    glVertexAttribPointer(tex_coords_attrib_location, 2, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(tex_coords_attrib_location)

def load_textures():
    texture_data, width, height = load_image('./assets/femalecodercat.jpg')

    print(texture_data, width, height)

    texture = glGenTextures(1)

    glBindTexture(GL_TEXTURE_2D, texture)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)
    glBindTexture(GL_TEXTURE_2D, 0)

    texture_loc = glGetUniformLocation(program, 'octo_texture')

    return texture, texture_loc

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

def handle_texture():
    glUniform1i(texture_loc, 0)
    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, texture)

program = load_shaders()
setup_triangle()

glUseProgram(program)
texture, texture_loc = load_textures()

def draw():
    glClear(GL_COLOR_BUFFER_BIT)

    handle_texture()

    glDrawArrays(GL_TRIANGLES, 0, 3)

def main_loop():
    while not glfw.window_should_close(window):
        draw()
        glfw.swap_buffers(window)
        glfw.poll_events()
    
    glfw.terminate()


main_loop()