#version 330 core
in vec2 vertex;
in vec2 screen_coords;
out vec2 uvs;

void main() {
    uvs = screen_coords;
    gl_Position = vec4(vertex, 0.0, 1.0);
}
