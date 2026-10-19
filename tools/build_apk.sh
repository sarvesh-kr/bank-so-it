#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
: "${ANDROID_HOME:=/workspace/android-tools/sdk}"
if [ -z "${JAVA_HOME:-}" ]; then
  if command -v javac >/dev/null; then JAVA_HOME="$(dirname "$(dirname "$(readlink -f "$(command -v javac)")")")";
  elif [ -d /workspace/android-tools ]; then JAVA_HOME="$(find /workspace/android-tools -maxdepth 1 -type d -name 'jdk-*' | head -1)";
  else echo 'Set JAVA_HOME to your JDK directory.' >&2; exit 1; fi
fi
export JAVA_HOME
export PATH="$JAVA_HOME/bin:$PATH"
BT="$ANDROID_HOME/build-tools/35.0.0"
PLATFORM="$ANDROID_HOME/platforms/android-35/android.jar"
BUILD="$ROOT_DIR/build"
mkdir -p "$BUILD/classes" "$BUILD/dex" "$ROOT_DIR/dist" "$ROOT_DIR/signing"
python3 "$ROOT_DIR/tools/build_bank.py"
"$BT/aapt" package -f -m -M "$ROOT_DIR/app/src/main/AndroidManifest.xml" -S "$ROOT_DIR/app/src/main/res" -A "$ROOT_DIR/app/src/main/assets" -I "$PLATFORM" -F "$BUILD/resources.apk"
if command -v javac >/dev/null; then
  javac --release 8 -encoding UTF-8 -classpath "$PLATFORM" -d "$BUILD/classes" "$ROOT_DIR/app/src/main/java/in/rrbpractice/lite/MainActivity.java"
elif [ -n "${ECJ_JAR:-}" ] && [ -f "$ECJ_JAR" ]; then
  # Optional compiler for environments with a JRE and Eclipse compiler only.
  java -jar "$ECJ_JAR" -source 8 -target 8 -proc:none -encoding UTF-8 -classpath "$PLATFORM" -d "$BUILD/classes" "$ROOT_DIR/app/src/main/java/in/rrbpractice/lite/MainActivity.java"
else
  echo 'Install a JDK with javac, or set JAVA_HOME and ECJ_JAR for a JRE/Eclipse compiler build.' >&2
  exit 1
fi
find "$BUILD/classes" -name '*.class' -print > "$BUILD/classes.list"
"$BT/d8" --release --min-api 24 --lib "$PLATFORM" --output "$BUILD/dex" @"$BUILD/classes.list"
cp "$BUILD/resources.apk" "$BUILD/unsigned.apk"
(cd "$BUILD/dex" && zip -q -9 "$BUILD/unsigned.apk" classes.dex)
"$BT/zipalign" -f -p 4 "$BUILD/unsigned.apk" "$BUILD/aligned.apk"
# A local personal-distribution key is generated once and reused for future upgrades.
# Keep signing/ private. This is not the Android SDK's shared debug key.
if [ ! -f "$ROOT_DIR/signing/release.jks" ]; then
  python3 -c 'import secrets,sys; open(sys.argv[1],"w").write(secrets.token_urlsafe(32))' "$ROOT_DIR/signing/password.txt"
  chmod 600 "$ROOT_DIR/signing/password.txt"
  keytool -genkeypair -keystore "$ROOT_DIR/signing/release.jks" -storepass:file "$ROOT_DIR/signing/password.txt" -keypass:file "$ROOT_DIR/signing/password.txt" -alias rrb-it-personal -keyalg RSA -keysize 2048 -validity 10000 -dname "CN=RRB IT Practice Personal Build"
  chmod 600 "$ROOT_DIR/signing/release.jks"
fi
"$BT/apksigner" sign --ks "$ROOT_DIR/signing/release.jks" --ks-key-alias rrb-it-personal --ks-pass "file:$ROOT_DIR/signing/password.txt" --out "$ROOT_DIR/dist/RRB-IT-Practice-Lite.apk" "$BUILD/aligned.apk"
"$BT/apksigner" verify --verbose "$ROOT_DIR/dist/RRB-IT-Practice-Lite.apk"
"$BT/aapt" dump badging "$ROOT_DIR/dist/RRB-IT-Practice-Lite.apk" > "$ROOT_DIR/docs/apk-metadata.txt"
sha256sum "$ROOT_DIR/dist/RRB-IT-Practice-Lite.apk" > "$ROOT_DIR/dist/SHA256SUMS.txt"
ls -lh "$ROOT_DIR/dist/RRB-IT-Practice-Lite.apk"
