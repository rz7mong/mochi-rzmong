#pragma once
#include <Arduino.h>

bool mochiDfInit();
void mochiDfStop();
void mochiDfService();
void mochiDfSetVolume(int vol21, bool on);
bool mochiDfPlayReact(int reactIndex);
bool mochiDfPlayFace(int faceIndex);
bool mochiDfPlayGif(const char *gifPath);
