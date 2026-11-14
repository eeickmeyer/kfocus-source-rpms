#!/bin/bash
set -eu

root="$(cd "$(dirname "$0")/.." && pwd)"
tmpdir="$(mktemp -d)"
trap 'rm -f "$tmpdir/busctl" "$tmpdir/calls" "$tmpdir/error"; rmdir "$tmpdir"' EXIT

cat > "$tmpdir/busctl" <<'EOF'
#!/bin/bash
printf '%s\n' "$*" >> "$CALL_LOG"
if [ "${MOCK_FAIL:-0}" = 1 ]; then
    echo "D-Bus call failed" >&2
    exit 1
fi
if [ "$2" = get-property ]; then
    printf '%s\n' "$MOCK_REPLY"
fi
EOF
chmod +x "$tmpdir/busctl"
export PATH="$tmpdir:$PATH"
export CALL_LOG="$tmpdir/calls"

for profile in power-saver balanced performance; do
    export MOCK_REPLY="s \"$profile\""
    [ "$(bash "$root/kfocus-power-profile" get)" = "$profile" ]
    bash "$root/kfocus-power-profile" set "$profile"
    grep -Fxq -- "--system set-property net.hadess.PowerProfiles /net/hadess/PowerProfiles net.hadess.PowerProfiles ActiveProfile s $profile" "$CALL_LOG"
done

export MOCK_REPLY='s "unexpected"'
if bash "$root/kfocus-power-profile" get 2>"$tmpdir/error"; then
    echo 'Unexpected profile was accepted' >&2
    exit 1
fi
grep -q 'Unexpected power profile response' "$tmpdir/error"

calls="$(wc -l < "$CALL_LOG")"
if bash "$root/kfocus-power-profile" set invalid 2>"$tmpdir/error"; then
    echo 'Invalid profile was accepted' >&2
    exit 1
fi
[ "$(wc -l < "$CALL_LOG")" = "$calls" ]

export MOCK_FAIL=1
if bash "$root/kfocus-power-profile" get 2>"$tmpdir/error"; then
    echo 'Failed D-Bus read was accepted' >&2
    exit 1
fi
if bash "$root/kfocus-power-profile" set balanced 2>"$tmpdir/error"; then
    echo 'Failed D-Bus write was accepted' >&2
    exit 1
fi

echo 'Power profile helper tests passed'
