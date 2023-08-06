#!/bin/env python3

#######################################################################
# Copyright (C) 2018, 2019 David Palao
#
# This file is part of QULo.
#
#  QULo is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  QULo is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with QULo.  If not, see <http://www.gnu.org/licenses/>.
#
#######################################################################

import unittest
from unittest.mock import patch, MagicMock
import pickle

from qulo.qmessage import QMessage, UnsuitableQMessage, WrongPickleMessage
from qulo.constants import (
    WRONG_MESSAGE_TO_GRAPHITE_MSG, WRONG_MESSAGE_TO_GRAPHITE_DETAIL_MSG,
)


class QMessageTestCase(unittest.TestCase):
    def make_qmessage(self, in_msg):
        pickled_message = pickle.dumps(in_msg)
        test_qmsg = QMessage(pickled_message)
        return test_qmsg

    @patch("qulo.qmessage.QMessage._identify_message_type")
    @patch("qulo.qmessage.pickle.loads")
    def test_instance_sets_message_attribute(self, mock_loads, mock_ident):
        raw_test_message = "Winnipeg viene"
        loadsed_message = MagicMock()
        def _loads(arg):
            if arg == raw_test_message:
                return loadsed_message
            else:
                return None
        mock_loads.side_effect = _loads
        #
        qmsg = QMessage(raw_test_message)
        #
        self.assertEqual(qmsg._message, loadsed_message)

    @patch("qulo.qmessage.QMessage._identify_message_type")
    @patch("qulo.qmessage.pickle.loads")
    def test_instances_init_calls_identify_message_type(self, mock_loads, mock_ident):
        raw_test_message = "Winnipeg viene"
        qmsg = self.make_qmessage(raw_test_message)
        mock_ident.assert_called_once_with()

    @patch("qulo.qmessage.QMessage._identify_message_type")
    @patch("qulo.qmessage.pickle.loads")
    def test_init_raises_WrongPickleQMessage_if_pickle_fails(self, mock_loads, mock_ident):
        raw_test_message = MagicMock()
        for excpt in (pickle.UnpicklingError, EOFError):
            mock_loads.side_effect = excpt
            with self.assertRaises(WrongPickleMessage):
                qmsg = QMessage(raw_test_message)

    def test_identify_message_type_if_not_graphitable_message(self):
        raw_test_message = {"value": "Winnipeg viene"}
        qmsg = self.make_qmessage(raw_test_message)
        qmsg._identify_message_type()
        self.assertFalse(qmsg._is_graphitable)

    def test_identify_message_type_if_multi_value_message(self):
        raw_test_message = {"value": {"quei": "valiu"}}
        qmsg = self.make_qmessage(raw_test_message)
        qmsg._identify_message_type()
        self.assertTrue(qmsg._is_graphitable)
        self.assertTrue(qmsg._is_multi_valued)

    def test_identify_message_type_if_numeric_message(self):
        raw_test_message = {"value": "42.3"}
        qmsg = self.make_qmessage(raw_test_message)
        qmsg._identify_message_type()
        self.assertTrue(qmsg._is_graphitable)
        self.assertFalse(qmsg._is_multi_valued)

    @patch("qulo.qmessage.QMessage._identify_message_type")
    @patch("qulo.qmessage.QMessage._pack_for_graphite")
    @patch("qulo.qmessage.QMessage._arrange_for_graphite")
    def test_to_graphite_arranges_and_packs_data_for_graphite(
            self, mock_arrange_for_graphite,
            mock_pack_for_graphite, mock_ident):
        test_data = MagicMock()
        expected_return = MagicMock()
        def mock_pack_for_graphite_side_effect(value):
            if value == test_data:
                return expected_return
        mock_arrange_for_graphite.return_value = test_data
        mock_pack_for_graphite.side_effect = mock_pack_for_graphite_side_effect
        test_qmsg = self.make_qmessage("Winnipeg vuelve")
        test_qmsg._is_graphitable = True
        #
        result = test_qmsg.to_graphite()
        #
        self.assertEqual(result, expected_return)

    def test_to_graphite_raises_UnsuitableQMessage_if_not_graphitable(self):
        values = [{"winimo": "11", "jatemate": "3"}]
        original_message = {
            "host": "mongolia",
            "sensor": "frescor",
            "time": "1843348596.0087",
            "value": values,
        }
        expected_msg = "{} ({})".format(
            WRONG_MESSAGE_TO_GRAPHITE_MSG, WRONG_MESSAGE_TO_GRAPHITE_DETAIL_MSG
        )
        expected_msg = expected_msg.format(
            sensor=original_message["sensor"], measurement=values
        )
        qmsg = self.make_qmessage(original_message)
        with self.assertRaises(UnsuitableQMessage) as cm:
            qmsg.to_graphite()
        self.assertEqual(str(cm.exception), expected_msg)
            
    def test_arrange_for_graphite_return_value_if_messages_value_is_dict(self):
        values = {"0": "32", "winimo": "11", "jatemate": "3"}
        original_message = {
            "host": "machupichu",
            "sensor": "cochambrosidad",
            "time": "1843219764.8351722",
            "value": values,
        }
        prepath = "{host}.{sensor}".format(**original_message)
        timestamp = original_message["time"]
        expected = [
            ("{}.{}".format(prepath, k), (timestamp, v)) for k,v in values.items()
        ]
        test_qmsg = self.make_qmessage(original_message)
        result = test_qmsg._arrange_for_graphite()
        self.assertEqual(result, expected)

    def test_arrange_for_graphite_return_value_if_messages_value_is_a_number(self):
        value = "44"
        original_message = {
            "host": "here",
            "sensor": "humility",
            "time": "1840009763.6",
            "value": value,
        }
        path = "{host}.{sensor}".format(**original_message)
        timestamp = original_message["time"]
        expected = [(path, (timestamp, value))]
        test_qmsg = self.make_qmessage(original_message)
        result = test_qmsg._arrange_for_graphite()
        self.assertEqual(result, expected)

    @patch("qulo.qmessage.QMessage._identify_message_type")
    def test_pack_for_graphite_returns_expected_data(self, mock_ident):
        in_data = "caca de vaca"
        import struct
        test_qmsg = self.make_qmessage("Winnipeg no me gusta")
        result = test_qmsg._pack_for_graphite(in_data)
        header = result[:4]
        payload = result[4:]
        self.assertEqual(in_data, pickle.loads(payload))
        self.assertEqual(
            struct.unpack("!L", header)[0],
            len(pickle.dumps(in_data, protocol=2))
        )
