#
# auto-pts - The Bluetooth PTS Automation Framework
#
# Copyright (c) 2017, Intel Corporation.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms and conditions of the GNU General Public License,
# version 2, as published by the Free Software Foundation.
#
# This program is distributed in the hope it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#

"""SM test cases"""

try:
    from ptsprojects.testcase import TestCase, TestCmd, TestFunc, \
        TestFuncCleanUp
    from ptsprojects.mynewt.ztestcase import ZTestCase

except ImportError:  # running this module as script
    import sys
    sys.path.append("../..")  # to be able to locate the following imports

    from ptsprojects.testcase import TestCase, TestCmd, TestFunc, \
        TestFuncCleanUp
    from ptsprojects.mynewt.ztestcase import ZTestCase

from pybtp import btp
from pybtp.types import Addr, IOCap
from ptsprojects.stack import get_stack
from .sm_wid import sm_wid_hdl


def set_pixits(pts):
    """Setup SM profile PIXITS for workspace. Those values are used for test
    case if not updated within test case.

    PIXITS always should be updated accordingly to project and newest version of
    PTS.

    pts -- Instance of PyPTS"""

    pts.set_pixit("SM", "TSPX_bd_addr_iut", "DEADBEEFDEAD")
    pts.set_pixit("SM", "TSPX_iut_device_name_in_adv_packet_for_random_address", "")
    pts.set_pixit("SM", "TSPX_time_guard", "180000")
    pts.set_pixit("SM", "TSPX_use_implicit_send", "TRUE")
    pts.set_pixit("SM", "TSPX_new_key_failed_count", "0")
    pts.set_pixit("SM", "TSPX_Bonding_Flags", "01")
    pts.set_pixit("SM", "TSPX_ATTR_HANDLE", "0000")
    pts.set_pixit("SM", "TSPX_ATTR_VALUE", "0000000000000000")
    pts.set_pixit("SM", "TSPX_Min_Encryption_Key_Length", "07")
    pts.set_pixit("SM", "TSPX_OOB_Data", "0000000000000000FE12036E5A889F4D")
    pts.set_pixit("SM", "TSPX_tester_role_optional", "L2CAP_ROLE_INITIATOR")


def test_cases(pts):
    """Returns a list of SM test cases
    pts -- Instance of PyPTS"""

    pts_bd_addr = pts.q_bd_addr

    stack = get_stack()

    stack.gap_init()

    pre_conditions = [TestFunc(btp.core_reg_svc_gap),
                      TestFunc(btp.gap_read_ctrl_info),
                      TestFunc(lambda: pts.update_pixit_param(
                          "SM", "TSPX_bd_addr_iut",
                          stack.gap.iut_addr_get_str())),
                      TestFunc(lambda: pts.update_pixit_param(
                          "SM", "TSPX_OOB_Data", stack.gap.oob_legacy)),
                      TestFunc(lambda: pts.update_pixit_param(
                          "SM", "TSPX_Bonding_Flags", "01"
                          if stack.gap.current_settings_get('Bondable')
                          else "00")),
                      # FIXME Find better place to store PTS bdaddr
                      TestFunc(btp.set_pts_addr, pts_bd_addr, Addr.le_public)]

    test_cases = [
        ZTestCase("SM", "SM/CEN/PROT/BV-01-C",
                  pre_conditions,
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/PER/PROT/BV-02-C",
                  pre_conditions,
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/PER/JW/BV-02-C",
                  pre_conditions,
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/CEN/JW/BV-05-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.display_only)],
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/CEN/JW/BI-01-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.display_only)],
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/PER/JW/BI-02-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.no_input_output)],
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/PER/JW/BI-03-C",
                  pre_conditions,
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/CEN/JW/BI-04-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.display_only)],
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/CEN/PKE/BV-01-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.display_only),
                   TestFunc(btp.gap_set_mitm_off),
                   TestFunc(btp.gap_set_bondable_off)],
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/PER/PKE/BV-02-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.display_only)],
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/CEN/PKE/BV-04-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.display_only)],
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/PER/PKE/BV-05-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.display_only)],
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/CEN/PKE/BI-01-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.display_only)],
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/CEN/PKE/BI-02-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.display_only)],
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/PER/PKE/BI-03-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.display_only)],
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/CEN/OOB/BV-01-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.display_only),
                   TestFunc(btp.gap_oob_legacy_set_data, stack.gap.oob_legacy)],
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/CEN/OOB/BV-03-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.display_only),
                   TestFunc(btp.gap_oob_legacy_set_data, stack.gap.oob_legacy)],
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/CEN/OOB/BV-05-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.display_only),
                   TestFunc(btp.gap_oob_legacy_set_data, stack.gap.oob_legacy)],
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/CEN/OOB/BV-07-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.display_only),
                   TestFunc(btp.gap_oob_legacy_set_data, stack.gap.oob_legacy)],
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/CEN/OOB/BV-09-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.display_only),
                   TestFunc(btp.gap_oob_legacy_set_data, stack.gap.oob_legacy)],
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/CEN/OOB/BI-01-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.display_only),
                   TestFunc(btp.gap_oob_legacy_set_data, stack.gap.oob_legacy)],
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/PER/OOB/BV-02-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.display_only),
                   TestFunc(btp.gap_oob_legacy_set_data, stack.gap.oob_legacy)],
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/PER/OOB/BV-04-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.display_only),
                   TestFunc(btp.gap_oob_legacy_set_data, stack.gap.oob_legacy)],
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/PER/OOB/BV-06-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.display_only),
                   TestFunc(btp.gap_oob_legacy_set_data, stack.gap.oob_legacy)],
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/PER/OOB/BV-08-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.display_only),
                   TestFunc(btp.gap_oob_legacy_set_data, stack.gap.oob_legacy)],
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/PER/OOB/BV-10-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.display_only),
                   TestFunc(btp.gap_oob_legacy_set_data, stack.gap.oob_legacy)],
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/PER/OOB/BI-02-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.display_only),
                   TestFunc(btp.gap_oob_legacy_set_data, stack.gap.oob_legacy)],
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/CEN/EKS/BV-01-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.display_only)],
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/PER/EKS/BV-02-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.display_only)],
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/CEN/EKS/BI-01-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.display_only)],
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/PER/EKS/BI-02-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.display_only)],
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/PER/KDU/BV-01-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.display_only)],
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/PER/KDU/BV-02-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.display_only)],
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/PER/KDU/BV-03-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.display_only)],
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/CEN/KDU/BV-04-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.display_only)],
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/CEN/KDU/BV-05-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.display_only)],
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/CEN/KDU/BV-06-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.display_only)],
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/PER/KDU/BI-01-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.display_only)],
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/CEN/KDU/BI-01-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.display_only)],
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/PER/KDU/BV-07-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.display_only)],
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/PER/SIP/BV-01-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.keyboard_display)],
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/CEN/SIP/BV-02-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.keyboard_display),
                   TestFunc(btp.gap_set_mitm_off)],
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/PER/SIE/BV-01-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.no_input_output)],
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/CEN/KDU/BV-10-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.display_only)],
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/CEN/KDU/BV-11-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.display_only)],
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/CEN/SCJW/BV-01-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.display_only),
                   TestFunc(btp.gap_set_mitm_off),
                   TestFunc(btp.gap_set_bondable_off)],
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/CEN/SCJW/BV-04-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.display_only)],
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/CEN/SCJW/BI-01-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.display_only)],
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/CEN/SCPK/BV-01-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.display_only),
                   TestFunc(btp.gap_set_mitm_off),
                   TestFunc(btp.gap_set_bondable_off)],
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/CEN/SCPK/BV-04-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.display_only)],
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/CEN/SCPK/BI-01-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.display_only)],
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/CEN/SCPK/BI-02-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.display_only),
                   TestFunc(btp.gap_set_bondable_on)],
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/PER/KDU/BV-08-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.display_only)],
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/PER/KDU/BV-09-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.display_only)],
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/PER/SCJW/BV-02-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.display_only),
                   TestFunc(btp.gap_set_mitm_off),
                   TestFunc(btp.gap_set_bondable_off)],
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/PER/SCJW/BV-03-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.display_only)],
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/PER/SCJW/BI-02-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.display_only)],
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/PER/SCPK/BV-02-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.display_only)],
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/PER/SCPK/BV-03-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.display_only)],
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/PER/SCPK/BI-03-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.display_only)],
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/PER/SCPK/BI-04-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.keyboard_only)],
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/CEN/SCOB/BV-01-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.display_only)],
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/CEN/SCOB/BV-04-C",
                  pre_conditions,
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/CEN/SCOB/BI-01-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.display_only)],
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/CEN/SCOB/BI-04-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.display_only)],
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/PER/SCOB/BV-02-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.display_only)],
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/PER/SCOB/BV-03-C",
                  pre_conditions,
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/PER/SCOB/BI-02-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.display_only)],
                  generic_wid_hdl=sm_wid_hdl),
        ZTestCase("SM", "SM/PER/SCOB/BI-03-C",
                  pre_conditions +
                  [TestFunc(btp.gap_set_io_cap, IOCap.display_only)],
                  generic_wid_hdl=sm_wid_hdl),
    ]

    return test_cases


def main():
    """Main."""
    import ptsprojects.mynewt.iutctl as iutctl

    iutctl.init_stub()

    test_cases_ = test_cases("AB:CD:EF:12:34:56")

    for test_case in test_cases_:
        print()
        print(test_case)

        if test_case.edit1_wids:
            print("edit1_wids: %r" % test_case.edit1_wids)

        if test_case.verify_wids:
            print("verify_wids: %r" % test_case.verify_wids)

        for index, cmd in enumerate(test_case.cmds):
            print("%d) %s" % (index, cmd))


if __name__ == "__main__":
    main()
