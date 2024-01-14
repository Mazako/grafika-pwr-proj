#version 330 core

in vec3 pos;
in vec3 inColor;
in vec3 inNormal;
in vec2 inUv;

uniform mat4 projection_matrix;
uniform mat4 model_matrix;
uniform mat4 camera_transformation;
uniform vec3 viewPosition;

out vec3 outColor;
out vec3 normal;
out vec3 fragmentPosition;
out vec3 lightPosition;
out vec3 vPos;
out vec2 uv;

void main() {
    lightPosition = vec3(0, 1, -5);
    gl_Position = projection_matrix * camera_transformation * model_matrix * vec4(pos, 1);
    normal = mat3(transpose(inverse(model_matrix))) * inNormal;
    fragmentPosition = vec3(model_matrix * vec4(pos, 1));
    vPos = viewPosition;
    outColor = inColor;
    uv = inUv;
}
