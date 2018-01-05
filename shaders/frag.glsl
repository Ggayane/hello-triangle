#version 330 core

in vec3 colorV;
in vec2 tex_coords;

uniform sampler2D octo_texture;

out vec4 frag_color;

void main() {
    frag_color = mix(texture(octo_texture, tex_coords), vec4(colorV, 1), 0.5);    
}