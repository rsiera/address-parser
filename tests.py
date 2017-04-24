from unittest import TestCase

from addressline import AddressParser, InvalidAddressException


# TODO: No negative tests, which should have been done, but this solution is very limited
# so there would be a lot examples when this code fails.

class AddressParserTest(TestCase):
    def setUp(self):
        super(AddressParserTest, self).setUp()
        self.parser = AddressParser()

    def test_sanitized_address_should_sanitize_when_ok(self):
        sanitized_input = self.parser.sanitize_address('      Winterallee .3  ')
        self.assertEqual('Winterallee 3', sanitized_input)

    def test_parse_address_should_raise_error_when_empty_input(self):
        with self.assertRaises(InvalidAddressException):
            self.parser.parse_address('')

    def test_parse_address_should_raise_error_when_only_street_name_part(self):
        with self.assertRaises(InvalidAddressException):
            self.parser.parse_address('')

    def test_parse_address_should_return_parsed_address_when_two_parts(self):
        parsed_address = self.parser.parse_address("Blaufeldweg 123B")

        self.assertEqual('Blaufeldweg', parsed_address.street_name)
        self.assertEqual('123B', parsed_address.street_number)

    def test_parse_address_should_return_parsed_address_when_more_parts(self):
        parsed_address = self.parser.parse_address('Auf der Vogelwiese 23 b')

        self.assertEqual('Auf der Vogelwiese', parsed_address.street_name)
        self.assertEqual('23 b', parsed_address.street_number)

