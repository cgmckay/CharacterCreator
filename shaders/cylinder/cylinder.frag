#version 440
in vec4 color;
in vec4 positionGeometry;
out vec4 fragmentColor;
void main() {
    fragmentColor = positionGeometry;
}
