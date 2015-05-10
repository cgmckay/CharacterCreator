#version 440
#define NUM_INVOCATIONS 17
layout(lines, invocations=NUM_INVOCATIONS) in;
layout(triangle_strip, max_vertices=128) out;
out vec4 color;
out vec4 positionGeometry;
uniform mat4 mvpMatrix;
uniform vec3 pullPoints[10];
uniform vec3 bezier2;
#define RADIUS 3
#define IMPACT 2
#define PI 3.1415f
#define MAX_DIST 1.2f
#define RESOLUTION 16.0f

//draw a small triangle at the position to see where a point is
void drawPoint(vec4 position) {
    gl_Position = mvpMatrix * (position + vec4(0, .05, 0,0));
    EmitVertex();
    gl_Position = mvpMatrix * (position + vec4(0, -.05, 0,0));
    EmitVertex();
    gl_Position = mvpMatrix * (position + vec4(0, 0, .05,0));
    EmitVertex();
    EndPrimitive();
}

/**
* Distort the position of sourcePoint by moving it closer or farther from pullPoint
* @param sourcePoint current position of a point to move
* @param pullPoint position to pull or push sourcePoint towards
* @param pullAmount if <0, pull sourcePoint nearer to pullPoint.
         If >0, push sourcePoint farther from pullPoint.
         Value determines how much sourcePoint is pushed or pulled
*/
vec4 pullPoint(vec4 sourcePoint, vec4 pullPoint, float pullAmount) {
    float distance = length(pullPoint - sourcePoint);
    distance = clamp(distance/pullAmount, 0, MAX_DIST)/MAX_DIST;
    //color = distance * vec4(0,0,1,0);
    vec4 pulledPosition = mix(sourcePoint, pullPoint, 1-distance);
    return pulledPosition;
}

//pulls a position with pullPoints and emits a vertex
void emitPoint(vec4 position) {
    for(int i = 0; i < pullPoints.length; ++i) {
        if(length(pullPoints[i])>.05) {//Ignore all pull points at vec3(0,0,0), because that's the default value of pull points
            position = pullPoint(position, vec4(pullPoints[i], 1), IMPACT);
        }
    }
    gl_Position = mvpMatrix * position;
    positionGeometry = position;
    EmitVertex();
}

//Emit a vertex of a circle with the provided radius and center position
void emitCirclePoint(vec4 centerPosition, float radius, float angle) {
    vec4 circlePosition = vec4(0, radius*sin(angle), radius*cos(angle),0);
    vec4 position = centerPosition + circlePosition;
    emitPoint(position);
}

void drawCylinder(vec4 sourcePosition0, vec4 sourcePosition1) {
    float currentRatio = float(gl_InvocationID)/NUM_INVOCATIONS;
    float nextRatio = float(gl_InvocationID+1)/NUM_INVOCATIONS;
    vec4 currentLinePosition = mix(sourcePosition0, sourcePosition1, currentRatio);
    vec4 nextLinePosition = mix(sourcePosition0, sourcePosition1, nextRatio);
    for(int i = 0; i <= RESOLUTION; ++i) {
        float angle = 2*PI/RESOLUTION*i;
        color=vec4(i/RESOLUTION, 1, 1, 1);
        emitCirclePoint(currentLinePosition, RADIUS, angle);
        emitCirclePoint(nextLinePosition, RADIUS, angle);
    }
    EndPrimitive();
}

void drawCap(vec4 position) {
    float innerSliceRatius = RADIUS*float(gl_InvocationID)/NUM_INVOCATIONS;
    float outerSliceRatius = RADIUS*float(gl_InvocationID+1)/NUM_INVOCATIONS;
    for(int i = 0; i <= RESOLUTION; ++i) {
        float angle = 2*PI/RESOLUTION*i;
        color = vec4(1,i/RESOLUTION,0,1);
        emitCirclePoint(position, innerSliceRatius, angle);
        emitCirclePoint(position, outerSliceRatius, angle);
    }
    EndPrimitive();

}

void main() {
    vec4 sourcePosition0 = gl_in[0].gl_Position;
    vec4 sourcePosition1 = gl_in[1].gl_Position;
    drawPoint(vec4(pullPoints[0], 1));
    drawCylinder(sourcePosition0, sourcePosition1);
    drawCap(sourcePosition0);
    drawCap(sourcePosition1);
}

