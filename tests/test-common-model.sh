#!/bin/bash
set -eu

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 PATCHED_COMMON_LIBRARY" >&2
    exit 2
fi

tmpdir="$(mktemp -d)"
trap 'rm -f "$tmpdir/dmi" "$tmpdir/error" "$tmpdir/find" "$tmpdir/edid-decode" "$tmpdir/bc"; rmdir "$tmpdir"' EXIT

source "$1"
printf 'V54x_6x_TU\n' > "$tmpdir/dmi"
_cm2DmiProductNameFile="$tmpdir/dmi"

_cm2CalcEdpScreenSizeFn() {
    if [ "$screen_size" = fail ]; then return 1; fi
    printf '%s\n' "$screen_size"
}

for case_data in '380:14xeg3' '381:16xeg3'; do
    screen_size="${case_data%%:*}"
    expected="${case_data#*:}"
    _cm2ModelCode=''
    [ "$(_cm2CalcModelCodeFn 2>"$tmpdir/error")" = "$expected" ]
    [ ! -s "$tmpdir/error" ]
done

screen_size=fail
_cm2ModelCode=''
[ "$(_cm2CalcModelCodeFn 2>"$tmpdir/error")" = other ]
grep -q 'Cannot determine screen size; using generic hardware model' "$tmpdir/error"
if grep -q 'command not found' "$tmpdir/error"; then
    echo 'Screen-size fallback attempted to run a command' >&2
    exit 1
fi
[ "$(set +eu; _cm2EchoModelStrFn config_code 2>"$tmpdir/error")" = other ]
[ "$(set +eu; _cm2EchoModelStrFn label 2>"$tmpdir/error")" = other ]

printf 'Unknown model\n' > "$tmpdir/dmi"
_cm2ModelCode=''
[ "$(_cm2CalcModelCodeFn 2>"$tmpdir/error")" = other ]
[ ! -s "$tmpdir/error" ]

source "$1"
cat > "$tmpdir/find" <<'EOF'
#!/bin/bash
echo /mock-eDP
EOF
cat > "$tmpdir/edid-decode" <<'EOF'
#!/bin/bash
printf 'Detailed Timing Descriptors:\n DTD 1: sample (340 mm x 190 mm)\n'
EOF
cat > "$tmpdir/bc" <<'EOF'
#!/bin/bash
if [ "${MOCK_BC_FAIL:-0}" = 1 ]; then exit 1; fi
printf '%s\n' "${MOCK_BC_RESULT:-389}"
EOF
chmod +x "$tmpdir/find" "$tmpdir/edid-decode" "$tmpdir/bc"
export PATH="$tmpdir:$PATH"

[ "$(_cm2CalcEdpScreenSizeFn)" = 389 ]
export MOCK_BC_FAIL=1
if _cm2CalcEdpScreenSizeFn > /dev/null; then
    echo 'Failed screen-size calculation was accepted' >&2
    exit 1
fi
export MOCK_BC_FAIL=0 MOCK_BC_RESULT=invalid
if _cm2CalcEdpScreenSizeFn > /dev/null; then
    echo 'Invalid screen-size calculation was accepted' >&2
    exit 1
fi

echo 'Hardware model detection tests passed'
