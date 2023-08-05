import typing
import codecs
import hashlib

from leanbase.models.feature import FeatureDefinition, FeatureGlobalStatus
from leanbase.models.segment import SegmentDefinition, ConditionCombinator
from leanbase.models.condition import Condition, OperatorMapping, O

__NORMALIZING_DIVISOR__ = float(0xFFFFFFFFFFFFFFF)

def evaluate(user_attributes:typing.Dict, feature_definition:FeatureDefinition):
    """ Evaluate whether a user with given attributes has access to a feature.
    Right now, multi-variate configuration is not supported, so boolean would 
    suffice.

    so, only a boolean should suffice. 
    :param user_attributes: user's attributes in a dictionary
    :type user_attributes: dict

    :param feature_definition: the feature to evaluate against
    :type feature_definition: FeatureDefinition

    :return: Access status true/false for the feature key and user attributes.
    :rtype: bool
    """
    if feature_definition.global_status == FeatureGlobalStatus.GA:
        # Implies global access. Including staff and everyone else.
        return True

    # Otherwise, fall back to checking each segment to figure out whether this
    # feature is available to them. Enable takes precedence over suppressing.
    for segment in feature_definition.enabled_for_segments:
        if _user_matches_segment(user_attributes, segment):
            return True

    for segment in feature_definition.suppressed_for_segments:
        if _user_matches_segment(user_attributes, segment):
            return False

    # If partial feature, try THE algorithm
    if feature_definition.global_status == FeatureGlobalStatus.PARTIAL:
        user_identifier = user_attributes.get('user_id', user_attributes.get('id', user_attributes.get('email')))
        cleartext = feature_definition.id + '-' + user_identifier
        _hash = hashlib.sha1(codecs.encode(cleartext)).hexdigest()

        # Normalize cleartext into a fraction. Take the first 15 hexcharacters
        # and divide by the largest possible such hexnumber (__NORMALIZING_DIVISOR__)
        user_normalized_value = int(_hash[:15], base=16) / __NORMALIZING_DIVISOR__

        # Rollout_percentage from the servers will be at a 100 scale, so normalize,
        # compare, make a boolean and return.
        return user_normalized_value <= (feature_definition.rollout_percentage / 100)


    # Could not find a segment where it is enabled or disabled, return False.
    return False

def _user_matches_segment(user_attributes:typing.Dict, segment_definition:SegmentDefinition)->bool:
    if segment_definition.combinator == ConditionCombinator.OR:
        return any(
            map(lambda c: _user_matches_condition(user_attributes, c), segment_definition.conditions)
        )
    else:
        return all(
            map(lambda c: _user_matches_condition(user_attributes, c), segment_definition.conditions)
        )

def _user_matches_condition(user_attributes:typing.Dict, condition:Condition)->bool:
    """ Algorithm for matching conditions:

    Preconditions and escape clauses:
    1. condition.attribute_key must exist in user_attributes. else True
    2. user_attribute.value and condition.value must have same type. else True
    3. condition.operator must be applicable to condition.type else True
       applicability is decided by <OperatorMapping> in the
       leanbase.models.condition module.
    """
    if not condition.attribute_key in user_attributes:
        # Precondition 1.
        return True
    
    if type(user_attributes[condition.attribute_key]) != type(condition.value):
        # Precondition 2.
        return True

    if condition.operator not in OperatorMapping[condition.kind]:
        # Precondition 3.
        return True

    op = condition.operator
    uv = user_attributes[condition.attribute_key]
    va = condition.value
    if op == O.GTE:
        return uv >= va
    elif op == O.LTE:
        return uv <= va
    elif op == O.GT:
        return uv > va
    elif op == O.LT:
        return uv < va
    elif op in (O.IS, O.EQUALS):
        return uv == va
    elif op in (O.ISNOT, O.DNEQUAL):
        return uv != va
    elif op == O.STRTWITH:
        return uv.startswith(va)
    elif op == O.ENDSWITH:
        return uv.endswith(va)
    elif op == O.MATCHES:
        return bool(va.match(uv))
    elif op == O.CONTAINS:
        return va in uv

    return False