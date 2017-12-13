#!/usr/bin/env bash

sudo nvidia-docker run -dit --restart unless-stopped -p 50054:50054 bluelens/bl-search-vector:dev