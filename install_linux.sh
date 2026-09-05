#!/usr/bin/env bash
# Installs the "pong" command on Linux / macOS and adds it to PATH
# automatically - no manual steps, no sudo required.
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="$HOME/.local/bin"
TARGET="$INSTALL_DIR/pong"

mkdir -p "$INSTALL_DIR"
cp "$SCRIPT_DIR/pong.py" "$TARGET"
chmod +x "$TARGET"
echo "Installed to $TARGET"

add_path_line() {
    local rc_file="$1"
    local line='export PATH="$HOME/.local/bin:$PATH"'
    touch "$rc_file"
    if grep -Fq "$line" "$rc_file"; then
        return 0
    fi
    {
        echo ""
        echo "# Added by the PyPong installer"
        echo "$line"
    } >> "$rc_file"
    echo "Added $INSTALL_DIR to PATH in $rc_file"
}

case ":$PATH:" in
    *":$INSTALL_DIR:"*)
        echo "$INSTALL_DIR is already in PATH."
        echo "Done! Type: pong"
        ;;
    *)
        SHELL_NAME="$(basename "${SHELL:-bash}")"
        case "$SHELL_NAME" in
            zsh)
                add_path_line "$HOME/.zshrc"
                ;;
            bash)
                add_path_line "$HOME/.bashrc"
                # macOS Terminal opens login shells that read .bash_profile
                [ -f "$HOME/.bash_profile" ] && add_path_line "$HOME/.bash_profile"
                ;;
            *)
                add_path_line "$HOME/.profile"
                ;;
        esac
        echo "Done! Open a new terminal window (or run: exec \$SHELL) and type: pong"
        ;;
esac