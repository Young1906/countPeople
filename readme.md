# STORE TRAFFIC COUNTER

## I. SYSTEM ARCHITECTURE
[![](https://mermaid.ink/img/eyJjb2RlIjoiZ3JhcGggVERcblx0QShDYW1lcmEpIC0tPnx2aWRlbyBmZWVkfCBCKEVuZ2luZSlcblx0QiAtLT58dHJhZmZpYyBldmVudHwgQyhGcm9udCBFbmQpXG5cdEIgLS0-fHRyYWZmaWMgZXZlbnR8IEQoRGF0YWJhc2UpXHRcdFx0XHQiLCJtZXJtYWlkIjp7InRoZW1lIjoiZGVmYXVsdCJ9LCJ1cGRhdGVFZGl0b3IiOmZhbHNlfQ)](https://mermaid-js.github.io/mermaid-live-editor/#/edit/eyJjb2RlIjoiZ3JhcGggVERcblx0QShDYW1lcmEpIC0tPnx2aWRlbyBmZWVkfCBCKEVuZ2luZSlcblx0QiAtLT58dHJhZmZpYyBldmVudHwgQyhGcm9udCBFbmQpXG5cdEIgLS0-fHRyYWZmaWMgZXZlbnR8IEQoRGF0YWJhc2UpXHRcdFx0XHQiLCJtZXJtYWlkIjp7InRoZW1lIjoiZGVmYXVsdCJ9LCJ1cGRhdGVFZGl0b3IiOmZhbHNlfQ)

### I.1 Engine (video feed processing engine)
**Input/Output**:
- Input: video feed (20 FPS/s)
- Output: emitting traffic event to FrontEnd and Database
