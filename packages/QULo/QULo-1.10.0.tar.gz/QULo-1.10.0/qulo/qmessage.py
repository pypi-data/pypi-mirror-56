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

import pickle
import struct

from qulo.constants import (
    WRONG_MESSAGE_TO_GRAPHITE_MSG, WRONG_MESSAGE_TO_GRAPHITE_DETAIL_MSG
)


class QMessageError(Exception):
    pass


class UnsuitableQMessage(QMessageError):
    pass


class WrongPickleMessage(QMessageError):
    pass


class QMessage:
    """The QMessage class packs functionality to interact with messages produced in
    the sensors.
    """
    def __init__(self, message):
        try:
            self._message = pickle.loads(message)
        except (pickle.UnpicklingError, EOFError):
            raise WrongPickleMessage()
        self._identify_message_type()
        
    def _identify_message_type(self):
        try:
            self._message["value"].items()
        except AttributeError:
            self._is_multi_valued = False
            try:
                float(self._message["value"])
            except (ValueError, TypeError):
                self._is_graphitable = False
            else:
                self._is_graphitable = True
        else:
            self._is_multi_valued = True
            self._is_graphitable = True

    def to_graphite(self):
        if not self._is_graphitable:
            err_msg = "{} ({})".format(
                WRONG_MESSAGE_TO_GRAPHITE_MSG, WRONG_MESSAGE_TO_GRAPHITE_DETAIL_MSG
            )
            err_msg = err_msg.format(
                sensor=self._message["sensor"],
                measurement=self._message["value"],
            )
            raise UnsuitableQMessage(err_msg)
        data = self._arrange_for_graphite()
        dressed_message = self._pack_for_graphite(data)
        return dressed_message
    
    def _arrange_for_graphite(self):
        """Internal method to be used by 'to_graphite'"""
        output_data = []
        basepath = "{}.{}".format(self._message["host"], self._message["sensor"])
        timestamp = self._message["time"]
        if self._is_multi_valued:
            for k, v in self._message["value"].items():
                path = "{}.{}".format(basepath, k)
                output_data.append((path, (timestamp, v)))
        else:
            value = self._message["value"]
            output_data.append((basepath, (timestamp, value)))
        return output_data

    def _pack_for_graphite(self, in_data):
        """Internal method to be used by 'to_graphite'"""
        payload = pickle.dumps(in_data, protocol=2)
        header = struct.pack("!L", len(payload))
        message_out = header + payload
        return message_out
