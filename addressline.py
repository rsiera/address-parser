from __future__ import unicode_literals


class Address(object):
    SEPARATOR = ' '

    def __init__(self, street_name='', street_number=''):
        self.street_name = street_name
        self.street_number = street_number

    def normalized(self):
        return Address(self.street_name.strip(), self.street_number.strip())

    def append_to(self, field, token):
        previous_value = getattr(self, field)
        previous_value += token + self.SEPARATOR
        setattr(self, field, previous_value)


class InvalidAddressException(Exception):
    pass


class HasTwoPartsRule(object):
    @classmethod
    def validate(cls, input):
        return input and len(input.split()) >= 2


class AddressValidator(object):
    def __init__(self, rules=None):
        if rules is None:
            rules = []
        self.rules = rules

    def validate(self, input):
        for rule in self.rules:
            if not rule.validate(input):
                raise InvalidAddressException


class AddressRuleChecker(object):
    # TODO: This class should be extended to continue implementation, now it handles the simples
    # cases, but it's designed to handle more complex logic in future
    RULES = [
        [('is_street_part',), 'street_name'],
        [('is_number_part',), 'street_number'],
    ]

    def is_street_part(self, token, current_address):
        return token.isalpha() and not current_address.street_number

    def is_number_part(self, token, current_address):
        return not self.is_street_part(token, current_address)

    def check_rule(self, token, current_address):
        for rules in self.RULES:
            if not self.meet_all_rules(rules[0], token, current_address):
                continue
            else:
                return True, rules[1]
        return False, None

    def meet_all_rules(self, rules, token, current_address):
        return all([getattr(self, rule)(token, current_address) for rule in rules])


class AddressParser(object):
    def __init__(self):
        self.validator = AddressValidator(rules=[HasTwoPartsRule])
        self.checker = AddressRuleChecker()

    def sanitize_address(self, address):
        return address.strip().replace('.', '')

    def parse_address(self, address):
        sanitized_address = self.sanitize_address(address)
        self.validator.validate(sanitized_address)

        parsed_address = self.process_tokens(sanitized_address)
        return self.normalize_address(parsed_address)

    def normalize_address(self, address):
        return address.normalized()

    def process_tokens(self, sanitized_address):
        address = Address()

        for token in sanitized_address.split():
            result, part_type = self.checker.check_rule(token, address)
            if result:
                address.append_to(part_type, token)
        return address
