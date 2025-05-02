#version 450 

in vec3 v_normal;
in vec3 v_position;
out vec4 out_color;

//phong shader
uniform vec3 light_position;
uniform vec3 light_color;
uniform vec3 view_position;
uniform vec3 input_color;

void main() {
    // Calculate the normal vector

    vec3 normal = normalize(v_normal);
    vec3 light_dir = normalize(light_position - v_position);
    vec3 view_dir = normalize(view_position - v_position);
    vec3 reflect_dir = reflect(-light_dir, normal);

    // Ambient light
    vec3 ambient = 0.3 * light_color;

    // Diffuse light
    float diff = max(dot(normal, light_dir), 0.0);
    vec3 diffuse = diff * light_color;

    // Specular light
    float spec = pow(max(dot(view_dir, reflect_dir), 0.0), 32);
    vec3 specular = spec * light_color;

    // Combine results
    vec3 result = (ambient + diffuse + specular) * input_color;

    out_color = vec4(normal, 1.0);
}