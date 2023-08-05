#!/usr/bin/env bash
#
# Detaches / Re-attached NVMe devices from kernel to SPDK and configures HUGEMEM
#
# on-enter: de-attach from kernel NVMe driver
# on-exit: re-attach to kernel NVMe driver
#
CIJ_TEST_NAME=$(basename "${BASH_SOURCE[0]}")
export CIJ_TEST_NAME
# shellcheck source=modules/cijoe.sh
source "$CIJ_ROOT/modules/cijoe.sh"
test::require ssh
test::enter

hook::spdk_enter() {
  if [[ ! -v SPDK_HOME ]]; then
    cij::err "hook::spdk_enter: FAILED: SPDK_HOME is unset"
    return 1
  fi

  SPDK_CMD="$SPDK_HOME/scripts/setup.sh"
  if [[ -v HUGEMEM ]]; then
    SPDK_CMD="HUGEMEM=$HUGEMEM $SPDK_CMD"
  fi
  if [[ -v NRHUGE ]]; then
    SPDK_CMD="NRHUGE=$NRHUGE $SPDK_CMD"
  fi
  if [[ -v HUGENODE ]]; then
    SPDK_CMD="HUGENODE=$HUGENODE $SPDK_CMD"
  fi

  if ! ssh::cmd "$SPDK_CMD"; then
    cij::err "hook::spdk_enter: FAILED: setting up SPDK devices"
    return 1
  fi

  return 0
}

hook::spdk_enter
exit $?
