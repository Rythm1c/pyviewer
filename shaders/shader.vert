#version 450

layout(location = 0) in vec3 a_position;
layout(location = 1) in vec3 a_normal;

out vec3 v_normal;
out vec3 v_position;

uniform mat4 u_projection;
uniform mat4 u_view;
uniform mat4 u_model;

void main() {
    // Apply the model-view-projection matrix to the vertex position
    // and pass the color to the fragment shader
    gl_Position = u_projection * u_view * u_model * vec4(a_position, 1.0);

    // Pass the normal to the fragment shader
    v_normal = mat3(transpose(inverse(u_model))) * normalize(a_normal);
    // Pass the position to the fragment shader
    v_position = (u_model * vec4(a_position, 1.0)).xyz;

}