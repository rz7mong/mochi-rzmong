#pragma once
#include <Arduino.h>
#include "MochiRzmong.h"

void dfAudioInit();
void dfStop();
void dfSetVolume(int vol21, bool on);
bool dfPlayReact(int reactIndex);
bool dfPlayFace(int faceIndex);
bool dfPlayGif(const char *gifPath);
