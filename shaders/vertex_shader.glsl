#version 330 core

in vec3 pos;
in vec3 inColor;
uniform mat4 projection_matrix;
uniform mat4 model_matrix;
uniform mat4 camera_transformation;

out vec3 outColor;

void main() {
    gl_Position = projection_matrix * camera_transformation * model_matrix * vec4(pos, 1);
    outColor = inColor;
}
