# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright (C) 2015-2020 GEM Foundation
#
# OpenQuake is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# OpenQuake is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with OpenQuake. If not, see <http://www.gnu.org/licenses/>.

from openquake.hazardlib.gsim.youd_etal_2002 import YoudEtAl2002
from openquake.hazardlib.tests.gsim.utils import BaseGSIMTestCase


class YoudEtAl2002TestCase(BaseGSIMTestCase):
    GSIM_CLASS = YoudEtAl2002

    # Verification tables provided by P. R. Jadhav and D. Wijewickreme
    
    def test_mean(self):
        
        self.check('YOUD04/Youd2004_MEAN.csv',
                   max_discrep_percentage=0.44)

    def test_std_total(self):
        self.check('YOUD04/Youd2004_STDDEV.csv',
                   max_discrep_percentage=0.1)
