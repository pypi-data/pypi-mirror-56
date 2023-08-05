import unittest

from . import fixtures

from leanbase.models.feature import FeatureDefinition
from leanbase.models.condition import Kinds, Operators
 
class DecodeTestCase(unittest.TestCase):
    def test_decode(self):
        feature_def = FeatureDefinition.from_encoding(**fixtures.LBAPP_ALL_FEATURES_RESPONSE[7])
        self.assertEqual(feature_def.id, 'plgYqgG')

        self.assertEqual(len(feature_def.enabled_for_segments), 1)
        self.assertEqual(len(feature_def.suppressed_for_segments), 1)

        self.assertEqual(len(feature_def.enabled_for_segments[0].conditions), 9)
        self.assertEqual(len(feature_def.suppressed_for_segments[0].conditions), 2)

        # Test a string condition (check fixture for details)
        condition_to_check = feature_def.enabled_for_segments[0].conditions[4]
        self.assertEqual(condition_to_check.kind, Kinds.STRING)
        self.assertEqual(condition_to_check.attribute_key, 'user.email')
        self.assertEqual(condition_to_check.operator, Operators.DNEQUAL)
        self.assertEqual(condition_to_check.value, 'sdf')
        
        # Test a boolean condition (check fixture for details)
        condition_to_check = feature_def.suppressed_for_segments[0].conditions[0]
        self.assertEqual(condition_to_check.kind, Kinds.BOOLEAN)
        self.assertEqual(condition_to_check.attribute_key, 'user.is_staff')
        self.assertEqual(condition_to_check.operator, Operators.ISNOT)
        self.assertEqual(condition_to_check.value, True)
