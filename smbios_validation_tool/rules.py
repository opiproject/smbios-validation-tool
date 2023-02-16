# Lint as: python3
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2019 Google LLC
# Copyright (c) 2023 Dell Inc, or its subsidiaries.
"""Module defines and lists all the rules for validating SMBIOS info.

Usage Example:
Rule(
    matcher.Matcher([matcher.RecordTypeMatcher(constants.RecordType.BIOS_RECORD)]),
    validator.IndividualValidator([validator.FieldPresentChecker('Vendor')]),
    'ERROR: Vendor field is missing in BIOS information record (DMI type 0).',
    'ACTION: Please populate Vendor field with correct vendor name.')

This rule will match SMBIOS records with DMI type 0, and validate if field
'Vendor' is present. If not, the error message and suggested actions will be
printed out.
"""

from smbios_validation_tool import constants
from smbios_validation_tool import matcher
from smbios_validation_tool import validator


class Rule:
  """Class that defines a rule for validating SMBIOS records.

  Attributes:
    matchers: a list of matchers. A record is matched if and only if all the
      matchers are matched.
    validators: a list of validators. A record is valid if and only if all the
      validators are valid.
    err_msg: a string stores the error message if SMBIOS record is invalid.
    action_msg: a string stores suggested actions to correct error if SMBIOS
      record is invalid.
  """

  def __init__(self, matchers, validators, err_msg, action_msg):
    self.matchers = matchers
    self.validators = validators
    self.err_msg = err_msg
    self.action_msg = action_msg

rules = [
    # Rules for Type 0 (BIOS information) record
    Rule(
        matcher.Matcher(
            [matcher.RecordTypeMatcher(constants.RecordType.BIOS_RECORD)]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Vendor'),
        ]), 'ERROR: Invalid Vendor field in Type 0 (BIOS Information) record.',
        'ACTION: Please populate Vendor field with valid string.'),
    Rule(
        matcher.Matcher(
            [matcher.RecordTypeMatcher(constants.RecordType.BIOS_RECORD)]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Version'),
        ]), 'ERROR: Invalid Version field in Type 0 (BIOS Information) record.',
        ('ACTION: BIOS Version can be any string as long as it follows properly documented procedure.\n'
         'If none available please follow the XX.YY.RR format.')),
    Rule(
        matcher.Matcher(
            [matcher.RecordTypeMatcher(constants.RecordType.BIOS_RECORD)]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Release Date'),
            validator.FieldValueRegexpChecker(
                'Release Date', constants.FieldValueRegexps.DATE_REGEXP.value)
        ]),
        'ERROR: Invalid Release Date field in Type 0 (BIOS Information) record.',
        'ACTION: Please populate BIOS Release Date field with correct date (format is MM/DD/YYYY).'
    ),
    Rule(
        matcher.Matcher(
            [matcher.RecordTypeMatcher(constants.RecordType.BIOS_RECORD)]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('ROM Size'),
            validator.FieldValueRegexpChecker('ROM Size', r'\d+ [kmgKMG]B')
        ]),
        'ERROR: Invalid ROM Size field in Type 0 (BIOS Information) record.',
        ('ACTION: Please populate BIOS ROM Size field with valid size.\n'
         '*BIOS ROM Size indicates the BIOS size not the flash part size.*')),

    # Rules for Type 2 (Board Information) records
    Rule(
        matcher.Matcher(
            [matcher.RecordTypeMatcher(constants.RecordType.BASEBOARD_RECORD)]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Manufacturer'),
        ]),
        'ERROR: Invalid Manufacturer field in Type 2 (Board Information) record.',
        'ACTION: Please populate Manufacturer field with valid string.'),
    Rule(
        matcher.Matcher(
            [matcher.RecordTypeMatcher(constants.RecordType.BASEBOARD_RECORD)]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Product Name'),
        ]),
        'ERROR: Invalid Product field in Type 2 (Board Information) record.',
        'ACTION: Please populate Product field with valid string.'),
    Rule(
        matcher.Matcher(
            [matcher.RecordTypeMatcher(constants.RecordType.BASEBOARD_RECORD)]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Features'),
        ]),
        'ERROR: Invalid Features field in Type 2 (Board information) record.',
        ('ACTION: Please populate Features field with valid feature flags.\n'
         'Bit0 - 1 for Motherboard, 0 for daughter boards; Bit3 - 1 for replaceable board.'
        )),
    Rule(
        matcher.Matcher(
            [matcher.RecordTypeMatcher(constants.RecordType.BASEBOARD_RECORD)]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Location In Chassis'),
            validator.FieldValueRegexpChecker(
                'Location In Chassis',
                constants.FieldValueRegexps.DEVPATH_REGEXP.value)
        ]),
        'ERROR: Invalid Location In Chassis field in Type 2 (Board Information) record.',
        ('ACTION: Please populate Location In Chassis field with valid devpath.\n'
         'This field provides the devpath for the daughter board.')),
    Rule(
        matcher.Matcher(
            [matcher.RecordTypeMatcher(constants.RecordType.BASEBOARD_RECORD)]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Chassis Handle'),
        ]),
        'ERROR: Invalid Chassis Handle in Type 2 (Board Information) record.',
        'ACTION: Please populate Chassis Handle field.'),
    Rule(
        matcher.Matcher(
            [matcher.RecordTypeMatcher(constants.RecordType.BASEBOARD_RECORD)]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Contained Object Handles'),
            validator.FieldItemCountChecker('Contained Object Handles')
        ]),
        'ERROR: Invalid Contained Object Handles field in Type 2 (Board Information) record.',
        'ACTION: Please populate Contained Object Handles field with valid handles.\n'
    ),

    # Rules for Type 3 (Chassis) records
    Rule(
        matcher.Matcher(
            [matcher.RecordTypeMatcher(constants.RecordType.CHASSIS_RECORD)]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Manufacturer'),
        ]), 'ERROR: Invalid Manufacturer field in Type 3 (Chassis) record.',
        'ACTION: Please populate Manufacturer field with valid string.'),
    Rule(
        matcher.Matcher(
            [matcher.RecordTypeMatcher(constants.RecordType.CHASSIS_RECORD)]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Type'),
        ]), 'ERROR: Invalid Type field in Type 3 (Chassis) record.',
        'ACTION: Please populate Type field with valid string.'),
    Rule(
        matcher.Matcher(
            [matcher.RecordTypeMatcher(constants.RecordType.CHASSIS_RECORD)]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Lock'),
            validator.FieldValueEnumChecker(
                'Lock', constants.FieldValueEnums.CHASSIS_LOCK.value),
        ]), 'ERROR: Invalid Lock field in Type 3 (Chassis) record.',
        ('ACTION: Please populate Lock field with valid string.\n'
         'Valid Lock Status: ' +
         ', '.join(constants.FieldValueEnums.CHASSIS_LOCK.value))),
    Rule(
        matcher.Matcher(
            [matcher.RecordTypeMatcher(constants.RecordType.CHASSIS_RECORD)]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Contained Elements'),
            validator.FieldValueRegexpChecker(
                'Contained Elements',
                constants.FieldValueRegexps.NUMBER_REGEXP.value),
        ]),
        'ERROR: Invalid Contained Elements field in Type 3 (Chassis) record.',
        'ACTION: Please populate Contained Elements field with valid number.'),

    # Rules for Type 4 (Processor Information) records
    #TODO:  Should there be a regexp validation of Socket Designation?
    Rule(
        matcher.Matcher(
            [matcher.RecordTypeMatcher(constants.RecordType.PROCESSOR_RECORD)]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Socket Designation'),
        ]),
        'ERROR: Invalid Socket Designation field in Type 4 (Processor Information) record.',
        'ACTION: Please populate Socket Designation field with valid string.\n'),
    Rule(
        matcher.Matcher(
            [matcher.RecordTypeMatcher(constants.RecordType.PROCESSOR_RECORD)]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Type'),
            validator.FieldValueEnumChecker(
                'Type', constants.FieldValueEnums.PROCESSOR_TYPE.value),
        ]),
        'ERROR: Invalid Type field in Type 4 (Processor Information) record.',
        ('ACTION: Please populate Type field with valid string.\n'
         'Valid Processor Type(s): ' +
         ', '.join(constants.FieldValueEnums.PROCESSOR_TYPE.value))),
    Rule(
        matcher.Matcher(
            [matcher.RecordTypeMatcher(constants.RecordType.PROCESSOR_RECORD)]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Status'),
            validator.FieldValueEnumChecker(
                'Status', constants.FieldValueEnums.PROCESSOR_STATUS.value),
        ]),
        'ERROR: Invalid Status field in Type 4 (Processor Information) record.',
        ('ACTION: Please populate Status field with valid string.\n'
         'Valid Status: ' +
         ', '.join(constants.FieldValueEnums.PROCESSOR_STATUS.value))),
    Rule(
        matcher.Matcher(
            [matcher.RecordTypeMatcher(constants.RecordType.PROCESSOR_RECORD)]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('L1 Cache Handle'),
            validator.HandleFieldChecker('L1 Cache Handle',
                                         constants.RecordType.CACHE_RECORD)
        ]),
        'ERROR: Invalid L1 Cache Handle field in Type 4 (Processor Information) record.',
        'ACTION: Please populate L1 Cache Handle field with valid handle'),
    Rule(
        matcher.Matcher(
            [matcher.RecordTypeMatcher(constants.RecordType.PROCESSOR_RECORD)]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('L2 Cache Handle'),
            validator.HandleFieldChecker('L2 Cache Handle',
                                         constants.RecordType.CACHE_RECORD)
        ]),
        'ERROR: Invalid L2 Cache Handle field in Type 4 (Processor Information) record.',
        'ACTION: Please populate L2 Cache Handle field with valid handle'),
    Rule(
        matcher.Matcher(
            [matcher.RecordTypeMatcher(constants.RecordType.PROCESSOR_RECORD)]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('L3 Cache Handle'),
            validator.HandleFieldChecker('L3 Cache Handle',
                                         constants.RecordType.CACHE_RECORD)
        ]),
        'ERROR: Invalid L3 Cache Handle field in Type 4 (Processor Information) record.',
        'ACTION: Please populate L3 Cache Handle field with valid handle'),
    Rule(
        matcher.Matcher(
            [matcher.RecordTypeMatcher(constants.RecordType.PROCESSOR_RECORD)]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Core Count'),
            validator.FieldValueRegexpChecker(
                'Core Count', constants.FieldValueRegexps.NUMBER_REGEXP.value),
        ]),
        'ERROR: Invalid Core Count field in Type 4 (Processor Information) record.',
        'ACTION: Please populate Core Count field with valid number.\n'),
    Rule(
        matcher.Matcher(
            [matcher.RecordTypeMatcher(constants.RecordType.PROCESSOR_RECORD)]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Core Enabled'),
            validator.FieldValueRegexpChecker(
                'Core Enabled',
                constants.FieldValueRegexps.NUMBER_REGEXP.value),
        ]),
        'ERROR: Invalid Core Enabled field in Type 4 (Processor Information) record.',
        'ACTION: Please populate Core Enabled field with valid number.\n'),
    Rule(
        matcher.Matcher(
            [matcher.RecordTypeMatcher(constants.RecordType.PROCESSOR_RECORD)]),
        validator.IndividualValidator([
            validator.FieldPresentChecker('Thread Count'),
            validator.FieldValueRegexpChecker(
                'Thread Count',
                constants.FieldValueRegexps.NUMBER_REGEXP.value),
        ]),
        'ERROR: Invalid Thread Count field in Type 4 (Processor Information) record.',
        'ACTION: Please populate Thread Count field with valid number.\n'),
]
