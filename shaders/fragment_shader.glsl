#version 330 core

in vec3 outColor;
in vec3 normal;
in vec3 fragmentPosition;
in vec3 lightPosition;
in vec3 vPos;
in vec2 uv;

uniform sampler2D tex;
uniform bool showTex;

out vec4 frag_color;
void main() {
    // diffuse
    vec3 lightColor = vec3(1, 1, 1);
    vec3 normalizedNormal = normalize(normal);
    vec3 lightDirection = normalize(lightPosition - fragmentPosition);
    float difference = max(dot(normalizedNormal, lightDirection), 0);
    vec3 diffuse = difference * lightColor;

    // specular
    float strength = 10;
    vec3 viewDirection = normalize(vPos - fragmentPosition);
    vec3 reflectDirection = reflect(-lightDirection, normalizedNormal);
    float spec = pow(max(dot(viewDirection, reflectDirection), 0), 16);
    vec3 specular = strength * spec * lightColor;

    vec4 color = vec4(outColor * (0.1 + diffuse + specular), 1);
    if (showTex) {
        frag_color = color * texture(tex, uv);
    } else {
        frag_color = color;
    }
}