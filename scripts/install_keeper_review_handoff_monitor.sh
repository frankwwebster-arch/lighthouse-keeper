#!/bin/zsh
# Install the Keeper review monitor as a per-user macOS launchd job.

set -euo pipefail

SCRIPT_DIR="${0:A:h}"
LABEL="com.lighthousekeeper.review-handoff-monitor"
SUPPORT_DIR="/Users/frank/Library/Application Support/Lighthouse Keeper"
LOG_DIR="/Users/frank/Library/Logs/LighthouseKeeper"
PLIST_PATH="/Users/frank/Library/LaunchAgents/${LABEL}.plist"
INSTALLED_SCRIPT="${SUPPORT_DIR}/keeper_review_handoff_monitor.py"
TEMPLATE="${SCRIPT_DIR}/${LABEL}.plist.template"
TEMP_PLIST="$(mktemp /private/tmp/${LABEL}.XXXXXX)"

cleanup() {
  rm -f "${TEMP_PLIST}"
}
trap cleanup EXIT

mkdir -p "${SUPPORT_DIR}" "${LOG_DIR}"
cp "${SCRIPT_DIR}/keeper_review_handoff_monitor.py" "${INSTALLED_SCRIPT}"
chmod 700 "${INSTALLED_SCRIPT}"
sed "s|__KEEPER_REVIEW_MONITOR_SCRIPT__|${INSTALLED_SCRIPT}|g" "${TEMPLATE}" > "${TEMP_PLIST}"
plutil -lint "${TEMP_PLIST}" >/dev/null
launchctl bootout "gui/$(id -u)" "${PLIST_PATH}" >/dev/null 2>&1 || true
mv "${TEMP_PLIST}" "${PLIST_PATH}"
launchctl bootstrap "gui/$(id -u)" "${PLIST_PATH}"
"${INSTALLED_SCRIPT}" --check
echo "Installed ${LABEL}; it checks every four hours and notifies only for changed hand-backs."
