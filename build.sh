#!/bin/bash
DOCKER_BUILDKIT=1 docker build -t bodypix:latest ./bodypix
DOCKER_BUILDKIT=1 docker build -t fakecam:latest ./fakecam
