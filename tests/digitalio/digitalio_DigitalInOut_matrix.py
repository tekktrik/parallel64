# SPDX-FileCopyrightText: 2023 Alec Delaney
#
# SPDX-License-Identifier: MIT

"""
Helper functions for testing parallel64.digitalio.DigitalInOut settings
"""

from typing import Iterable
from typing_extensions import TypedDict, TypeAlias, Literal

from parallel64.digitalio import DigitalInOut, Direction, Pull, DriveMode

SettingOption: TypeAlias = Literal["direction", "pull", "drive_mode", "value"]
Setting: TypeAlias = Direction | DriveMode | Pull | bool
SettingResult: TypeAlias = BaseException | None
SettingRule: TypeAlias = tuple[Setting, SettingResult]
GetSetOption: Literal["get", "set"]

# SetRuleSet: TypeAlias = dict[Literal["set"], SettingRule]


class GetSetRules(TypedDict):
    get: SettingResult
    set: Iterable[SettingRule]


class SettingRuleSet(TypedDict):
    drive_mode: GetSetRules
    pull: GetSetRules
    value: GetSetRules


PossibleSettingRuleSet: TypeAlias = SettingRuleSet | BaseException


class PinRuleSet(TypedDict):
    input: PossibleSettingRuleSet
    output: PossibleSettingRuleSet


def dio_test_settings(dio: DigitalInOut, pin_ruleset: PinRuleSet) -> None:
    # Iterate through directions
    for io_direction, setting_ruleset in pin_ruleset.items():
        direction_setting = (
            Direction.INPUT if io_direction == "input" else Direction.OUTPUT
        )

        print("aaaaaaaaaaaaaaa", io_direction, dio.direction)
        # Test settings within this direction
        if isinstance(setting_ruleset, dict):
            dio_test_set_success(dio, "direction", direction_setting)
            print("xxxxxxxxxxxxxx", dio.direction)
            for setting_name, getsetting_rules in setting_ruleset.items():
                print("?????????", dio.direction)
                if getsetting_rules["get"] is None:
                    dio_test_get_success(dio, setting_name)
                else:
                    print("!!!!!!!!!!!!!!!!!!!!!", dio.direction)
                    dio_test_get_failure(dio, setting_name, getsetting_rules["get"])
                for setting_value, setting_result in getsetting_rules["set"]:
                    if setting_result is None:
                        dio_test_set_success(dio, setting_name, setting_value)
                    else:
                        dio_test_set_failure(
                            dio, setting_name, setting_value, setting_result
                        )
            continue

        dio_test_set_failure(dio, "direction", direction_setting, setting_ruleset)
        continue


def dio_test_set_success(
    dio: DigitalInOut, setting_option: SettingOption, setting: Setting
):
    try:
        setattr(dio, setting_option, setting)
    except:
        assert False


def dio_test_set_failure(
    dio: DigitalInOut,
    setting_option: SettingOption,
    setting: Setting,
    setting_result: BaseException,
):
    try:
        setattr(dio, setting_option, setting)
    except setting_result:
        assert True
    else:
        assert False


def dio_test_get_success(dio: DigitalInOut, setting_option: SettingOption):
    try:
        _ = getattr(dio, setting_option)
    except:
        assert False


def dio_test_get_failure(
    dio: DigitalInOut, setting_option: SettingOption, setting_result: BaseException
):
    try:
        _ = getattr(dio, setting_option)
        print(_)
    except setting_result as err:
        assert True
    else:
        assert False
