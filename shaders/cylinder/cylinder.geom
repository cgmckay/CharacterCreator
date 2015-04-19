#version 440
layout(lines) in;
layout(triangle_strip, max_vertices=120) out;
out vec4 color;
out vec4 positionGeometry;
uniform mat4 mvpMatrix;
#define PI 3.1415f
#define RESOLUTION 20.0f
void main() {
    for(float angle = 0; angle < 2*PI + 2*PI/RESOLUTION; angle += 2*PI/RESOLUTION) {
        for(int i=0; i<gl_in.length(); ++i) {
            vec4 vertexPosition = gl_in[i].gl_Position;
            vec4 position = vertexPosition + vec4(0, sin(angle), cos(angle),0);
            gl_Position = mvpMatrix * position;
            color = vec4(0,0,1,1);
            positionGeometry = position;
            EmitVertex();
        }
    }
    EndPrimitive();
}

