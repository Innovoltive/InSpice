####################################################################################################
#
# InSpice - A Spice Package for Python
# Copyright (C) 2020 jmgc / Fabrice Salvaire
# Copyright (C) 2025 Innovoltive
# Modified by Innovoltive on April 18, 2025
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
####################################################################################################

####################################################################################################

import pickle
import tempfile
import unittest

import numpy as np

####################################################################################################

import InSpice.Logging.Logging as Logging
logger = Logging.setup_logging()

####################################################################################################

from InSpice.Probe.WaveForm import WaveForm
from InSpice.Unit.Unit import UnitValues
from InSpice.Unit import u_kHz

####################################################################################################

class TestPickle(unittest.TestCase):

    ##############################################

    def test_ndarray(self):
        array = np.ndarray((1, 1))
        with tempfile.TemporaryFile() as fh:
            pickle.dump(array, fh)
            fh.seek(0)
            new_array = pickle.load(fh)
        self.assertEqual(array, new_array)

    ##############################################

    def test_unit_values(self):
        unit_values = UnitValues(u_kHz(100).prefixed_unit, (1, 1))
        new_unit_values = pickle.loads(pickle.dumps(unit_values))
        self.assertEqual(unit_values, new_unit_values)

    ##############################################

    def test_waveform(self):
        waveform = WaveForm('Test', u_kHz(100).prefixed_unit, (1, 1))
        new_waveform = pickle.loads(pickle.dumps(waveform))
        self.assertEqual(waveform, new_waveform)

####################################################################################################

if __name__ == '__main__':
    unittest.main()
