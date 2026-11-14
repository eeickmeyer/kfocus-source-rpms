#!/bin/bash
set -eu

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 PATCHED_MAIN_QML" >&2
    exit 2
fi

test_dir="$(cd "$(dirname "$0")/slider" && pwd)"
tmpdir="$(mktemp -d)"
trap 'rm -f "$tmpdir/Main.qml" "$tmpdir/ShellEngine.qml" "$tmpdir/tst_slider.qml"; rmdir "$tmpdir"' EXIT

sed -e '/id       : powerProfileSlider/a\        objectName : "testPowerSlider"' \
    -e '/id      : powerProfileMessage/a\        objectName : "testPowerMessage"' \
    -e '/id : setPowerProfileEngine/a\      objectName : "testSetEngine"' \
    -e '/id : readPowerProfileEngine/a\      objectName : "testReadEngine"' \
    "$1" > "$tmpdir/Main.qml"
cp "$test_dir/ShellEngine.qml" "$test_dir/tst_slider.qml" "$tmpdir/"

QT_QPA_PLATFORM=offscreen "${QMLTESTRUNNER:-qmltestrunner-qt6}" -input "$tmpdir"
