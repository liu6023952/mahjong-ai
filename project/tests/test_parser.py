import json
import os
import unittest

from base.log_parser import LogParser
from betaori_closed_hand.parser import BetaoriClosedHandParser


class ClientTestCase(unittest.TestCase):

    def test_parse_rounds_number(self):
        parser = LogParser()
        rounds_data = self._load_game_rounds_data(
            parser,
            'simple_hanchan.xml',
            '2018050300gm-00a9-0000-ce6923eb'
        )
        self.assertEqual(len(rounds_data), 9)

    def test_prepare_betaori_output(self):
        parser = BetaoriClosedHandParser()
        rounds_data = self._load_game_rounds_data(
            parser,
            'one_round.xml',
            '2018050300gm-00a9-0000-ce6923eb'
        )
        data = parser.parse_game_rounds(rounds_data)
        self._print_pretty_json(data)

        self.assertTrue(len(data) > 0)

    def _print_pretty_json(self, data):
        print(json.dumps(data, indent=2))

    def _load_game_rounds_data(self, parser, file_name, log_id):
        data_path = os.path.join(os.path.dirname(
            os.path.realpath(__file__)),
            'resources',
            file_name
        )

        with open(data_path, 'r') as f:
            log_content = f.read()
            rounds_data = parser.get_game_rounds(log_content, log_id)

            # we need to remove \n and spaces from loaded xml
            # because it was added there only for better tests readability
            for round_item in rounds_data:
                for i, tag in enumerate(round_item):
                    round_item[i] = tag.strip()

            return rounds_data
