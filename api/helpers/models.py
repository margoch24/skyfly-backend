from uuid import uuid4


def get_uuid():
    return uuid4().hex


def prepare_condition(cls, config={}, **kwargs):
    conditions = {}
    comparative_conditions = []

    for key, value in kwargs.items():
        comparative_condition, condition = prepare_condition_property(
            cls=cls,
            key=key,
            value=value,
            config=config,
        )

        conditions.update(condition)
        comparative_conditions.extend(comparative_condition)

    return comparative_conditions, conditions


def prepare_condition_property(cls, key, value, config):
    condition = {}
    comparative_condition = []

    if not value:
        return comparative_condition, condition

    config_value = config.get(key)
    if not config_value:
        condition[key] = value
        return comparative_condition, condition

    attribute = getattr(cls, key)

    type = config_value.get("type")
    match type:
        case "range":
            [min, max] = value
            comparative_condition.append(attribute >= min)
            comparative_condition.append(attribute <= max)

        case "in":
            comparative_condition.append(attribute.in_(value))

        case "datetime":
            one_day_difference = 24 * 60 * 60 * 1000
            min = value - one_day_difference
            max = value + one_day_difference

            comparative_condition.append(attribute >= min)
            comparative_condition.append(attribute <= max)

    operator = config_value.get("operator")

    match operator:
        case ">=":
            comparative_condition.append(attribute >= value)

        case "<=":
            comparative_condition.append(attribute <= value)

        case ">":
            comparative_condition.append(attribute > value)

        case "<":
            comparative_condition.append(attribute <= value)

        case "==":
            comparative_condition.append(attribute == value)

    return comparative_condition, condition
