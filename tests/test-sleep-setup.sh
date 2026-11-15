#!/bin/bash
set -eu

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 KFOCUS_SLEEP_SETUP" >&2
    exit 2
fi

setup="$1"
tmpdir="$(mktemp -d)"
trap 'rm -rf "$tmpdir"' EXIT

cat > "$tmpdir/common.source" <<'EOF'
_cm2EchoModelStrFn () { printf '%s\n' "$MOCK_CONFIG_CODE"; }
EOF
cat > "$tmpdir/source-hook" <<'EOF'
#!/bin/bash
_baseName='zsleep-kfocus';
EOF

export KFOCUS_COMMON_LIB="$tmpdir/common.source"
export KFOCUS_SLEEP_HOOK_SOURCE="$tmpdir/source-hook"
export KFOCUS_SLEEP_HOOK_FILE="$tmpdir/system-sleep/zsleep-kfocus"

for code in default xeg2 xeg3 arg1 m2g4 m2g5 zrg1 m2g6; do
    rm -rf "$tmpdir/system-sleep"
    MOCK_CONFIG_CODE="$code" "$setup"
    [ -x "$KFOCUS_SLEEP_HOOK_FILE" ]
    [ ! -L "$KFOCUS_SLEEP_HOOK_FILE" ]
    cmp -s "$tmpdir/source-hook" "$KFOCUS_SLEEP_HOOK_FILE"
done

# Models without the hook get nothing installed
for code in generic ir14g1 ir1Xg2 ir1Xg3 nxg1 other; do
    rm -rf "$tmpdir/system-sleep"
    MOCK_CONFIG_CODE="$code" "$setup"
    [ ! -e "$KFOCUS_SLEEP_HOOK_FILE" ]
done

# A hook installed by this package is removed on an unsupported model
MOCK_CONFIG_CODE=xeg3 "$setup"
MOCK_CONFIG_CODE=other "$setup"
[ ! -e "$KFOCUS_SLEEP_HOOK_FILE" ]

# An unrelated hook with the same name is left alone
mkdir -p "$tmpdir/system-sleep"
printf '#!/bin/sh\n' > "$KFOCUS_SLEEP_HOOK_FILE"
MOCK_CONFIG_CODE=other "$setup"
[ -f "$KFOCUS_SLEEP_HOOK_FILE" ]

# A missing hook source is an error on supported models
rm -f "$KFOCUS_SLEEP_HOOK_SOURCE"
if MOCK_CONFIG_CODE=xeg3 "$setup" 2>/dev/null; then
    echo 'Missing hook source was accepted' >&2
    exit 1
fi

echo 'Sleep hook setup tests passed'
