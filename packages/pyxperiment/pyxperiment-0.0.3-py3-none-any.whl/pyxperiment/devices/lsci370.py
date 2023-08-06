"""
    pyxperiment/devices/lsci370.py:
    Support for Lake Shore Model 370 resistance bridge

    This file is part of the PyXperiment project.

    Copyright (c) 2019 PyXperiment Developers

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.
"""

from pyxperiment.controller import VisaInstrument
from pyxperiment.controller.device_options import ValueDeviceOption
from pyxperiment.controller.validation import SimpleRangeValidator

class LakeShore370ResBridge(VisaInstrument):
    """
    Lake Shore Model 370 resistance bridge support
    """

    def __init__(self, rm, resource):
        super().__init__(rm, resource)
        self.write('*CLS')
        self.set_options(
            self.temperature + self.resistance +
            [self.target_temp]
        )

    @staticmethod
    def driver_name():
        return 'Lake Shore Model 370 resistance bridge'

    def device_name(self):
        value = self.query_id().translate({ord(c): None for c in ['\r', '\n']}).split(',')
        return value[0] + ' ' + value[1] + ' resistance bridge'

    temperature = [
        ValueDeviceOption(
            'Temperature CH ' + str(i), 'K',
            get_func=lambda instr, ch=i: instr.query('RDGK? '+str(ch))
            )
        for i in [2, 6]]

    resistance = [
        ValueDeviceOption(
            'Resistance CH ' + str(i), 'Ohm',
            get_func=lambda instr, ch=i: instr.query('RDGR? '+str(ch))
            )
        for i in [2, 6]]

    target_temp = ValueDeviceOption(
        'Set Temperature', 'K',
        get_func=lambda instr: instr.query('SETP?'),
        set_func=lambda instr, value: instr.write('SETP '+value),
        validator=SimpleRangeValidator('0', '4.2')
    )
