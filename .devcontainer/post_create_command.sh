#!/bin/bash

# Install Dependencies
sudo apt-get update -y
sudo apt-get install -y libudev-dev pkg-config usbutils

# Install Dagger CLI
curl -fsSL https://dl.dagger.io/dagger/install.sh | DAGGER_VERSION=0.19.2 BIN_DIR=$HOME/.local/bin sh
mkdir -p /home/vscode/.local/share/bash-completion/completions
dagger completion bash > /home/vscode/.local/share/bash-completion/completions/dagger