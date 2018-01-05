#version 330 core

in vec2 coords;
in vec3 colors;
in vec2 a_tex_coords;

out vec3 colorV;
out vec2 tex_coords;

void main() {
    colorV = colors;
    tex_coords = a_tex_coords;
    gl_Position = vec4(coords, 1, 1);
}