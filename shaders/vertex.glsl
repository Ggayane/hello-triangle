#version 330 core

in vec2 coords;
in vec3 colors;

out vec3 colorV;

void main() {
    colorV = colors;
    gl_Position = vec4(coords, 1, 1);
}