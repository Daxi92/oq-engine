# Copyright (c) 2010-2012, GEM Foundation.
#
# OpenQuake is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# OpenQuake is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with OpenQuake.  If not, see <http://www.gnu.org/licenses/>.

import os
import csv
import numpy

from nose.plugins.attrib import attr as noseattr

from qa_tests import risk
from tests.utils import helpers

from openquake.engine.db import models


class EventBasedRiskCase1TestCase(risk.BaseRiskQATestCase):
    cfg = os.path.join(os.path.dirname(__file__), 'job.ini')

    EXPECTED_LOSS_CURVE_XML = """<?xml version='1.0' encoding='UTF-8'?>
<nrml xmlns:gml="http://www.opengis.net/gml"
      xmlns="http://openquake.org/xmlns/nrml/0.4">
  <lossCurves investigationTime="50.0"
              sourceModelTreePath="test_sm"
              gsimTreePath="test_gsim" unit="USD">
    <lossCurve assetRef="a1">
      <gml:Point>
        <gml:pos>15.48 38.09</gml:pos>
      </gml:Point>
      <poEs>1.0 0.979591836735 0.959183673469 0.938775510204 0.918367346939 0.897959183673 0.877551020408 0.857142857143 0.836734693878 0.816326530612 0.795918367347 0.775510204082 0.755102040816 0.734693877551 0.714285714286 0.69387755102 0.673469387755 0.65306122449 0.632653061224 0.612244897959 0.591836734694 0.571428571429 0.551020408163 0.530612244898 0.510204081633 0.489795918367 0.469387755102 0.448979591837 0.428571428571 0.408163265306 0.387755102041 0.367346938776 0.34693877551 0.326530612245 0.30612244898 0.285714285714 0.265306122449 0.244897959184 0.224489795918 0.204081632653 0.183673469388 0.163265306122 0.142857142857 0.122448979592 0.102040816327 0.0816326530612 0.0612244897959 0.0408163265306 0.0204081632653 0.0</poEs>
      <losses>34.2337411056 64.7589890607 68.2290881106 72.2352916074 76.6619792682 81.088666929 85.5153545895 90.2825736864 95.6331846177 100.983795549 106.334406481 111.685017412 117.035628344 122.386239275 127.736850207 133.087461138 138.43807207 143.788683002 149.139293933 152.893163398 156.604253472 160.315343546 164.026433621 167.737523695 171.44861377 175.159703844 178.870793918 182.581883992 186.292974067 190.004064141 193.715154216 197.42624429 201.137334364 204.848424439 208.559514513 212.270604587 215.981694662 219.692784736 223.40387481 227.114964885 230.826054959 234.537145033 238.248235108 241.959325182 245.670415256 249.381505331 253.092595405 256.803685479 260.514775554 264.225865628</losses>
      <lossRatios>0.0114112470352 0.0215863296869 0.0227430293702 0.0240784305358 0.0255539930894 0.027029555643 0.0285051181965 0.0300941912288 0.0318777282059 0.0336612651831 0.0354448021603 0.0372283391375 0.0390118761146 0.0407954130918 0.042578950069 0.0443624870461 0.0461460240233 0.0479295610005 0.0497130979777 0.0509643877993 0.052201417824 0.0534384478488 0.0546754778736 0.0559125078984 0.0571495379232 0.058386567948 0.0596235979727 0.0608606279975 0.0620976580223 0.0633346880471 0.0645717180719 0.0658087480966 0.0670457781214 0.0682828081462 0.069519838171 0.0707568681958 0.0719938982206 0.0732309282453 0.0744679582701 0.0757049882949 0.0769420183197 0.0781790483445 0.0794160783692 0.080653108394 0.0818901384188 0.0831271684436 0.0843641984684 0.0856012284931 0.0868382585179 0.0880752885427</lossRatios>
      <averageLoss>1.3384e+02</averageLoss>
    </lossCurve>
    <lossCurve assetRef="a2">
      <gml:Point>
        <gml:pos>15.56 38.17</gml:pos>
      </gml:Point>
      <poEs>1.0 0.979591836735 0.959183673469 0.938775510204 0.918367346939 0.897959183673 0.877551020408 0.857142857143 0.836734693878 0.816326530612 0.795918367347 0.775510204082 0.755102040816 0.734693877551 0.714285714286 0.69387755102 0.673469387755 0.65306122449 0.632653061224 0.612244897959 0.591836734694 0.571428571429 0.551020408163 0.530612244898 0.510204081633 0.489795918367 0.469387755102 0.448979591837 0.428571428571 0.408163265306 0.387755102041 0.367346938776 0.34693877551 0.326530612245 0.30612244898 0.285714285714 0.265306122449 0.244897959184 0.224489795918 0.204081632653 0.183673469388 0.163265306122 0.142857142857 0.122448979592 0.102040816327 0.0816326530612 0.0612244897959 0.0408163265306 0.0204081632653 0.0</poEs>
      <losses>8.80769990954 25.0364570154 27.0633066618 28.2335176244 28.7318389896 29.230160355 29.7284817202 30.067432699 30.1333534304 30.1992741618 30.2651948932 30.3311156246 30.397036356 30.4629570874 30.5288778188 30.5947985502 30.6607192818 30.7266400132 30.7925607446 30.8020310414 30.8099889362 30.817946831 30.8259047258 30.8338626204 30.8418205152 30.84977841 30.8577363048 30.8656941996 30.8736520944 30.881609989 30.8895678838 30.8975257786 30.9054836734 30.9134415682 30.921399463 30.9293573576 30.9373152524 30.9452731472 30.953231042 30.9611889368 30.9691468316 30.9771047262 30.985062621 30.9930205158 31.0009784106 31.0089363054 31.0168942002 31.0248520948 31.0328099896 31.0407678844</losses>
      <lossRatios>0.00440384995477 0.0125182285077 0.0135316533309 0.0141167588122 0.0143659194948 0.0146150801775 0.0148642408601 0.0150337163495 0.0150666767152 0.0150996370809 0.0151325974466 0.0151655578123 0.015198518178 0.0152314785437 0.0152644389094 0.0152973992751 0.0153303596409 0.0153633200066 0.0153962803723 0.0154010155207 0.0154049944681 0.0154089734155 0.0154129523629 0.0154169313102 0.0154209102576 0.015424889205 0.0154288681524 0.0154328470998 0.0154368260472 0.0154408049945 0.0154447839419 0.0154487628893 0.0154527418367 0.0154567207841 0.0154606997315 0.0154646786788 0.0154686576262 0.0154726365736 0.015476615521 0.0154805944684 0.0154845734158 0.0154885523631 0.0154925313105 0.0154965102579 0.0155004892053 0.0155044681527 0.0155084471001 0.0155124260474 0.0155164049948 0.0155203839422</lossRatios>
      <averageLoss>2.1409e+01</averageLoss>
    </lossCurve>
    <lossCurve assetRef="a3">
      <gml:Point>
        <gml:pos>15.48 38.25</gml:pos>
      </gml:Point>
      <poEs>1.0 0.979591836735 0.959183673469 0.938775510204 0.918367346939 0.897959183673 0.877551020408 0.857142857143 0.836734693878 0.816326530612 0.795918367347 0.775510204082 0.755102040816 0.734693877551 0.714285714286 0.69387755102 0.673469387755 0.65306122449 0.632653061224 0.612244897959 0.591836734694 0.571428571429 0.551020408163 0.530612244898 0.510204081633 0.489795918367 0.469387755102 0.448979591837 0.428571428571 0.408163265306 0.387755102041 0.367346938776 0.34693877551 0.326530612245 0.30612244898 0.285714285714 0.265306122449 0.244897959184 0.224489795918 0.204081632653 0.183673469388 0.163265306122 0.142857142857 0.122448979592 0.102040816327 0.0816326530612 0.0612244897959 0.0408163265306 0.0204081632653 0.0</poEs>
      <losses>11.3905266834 26.0726465488 29.8488432921 31.9478330478 32.7313347813 33.5148365149 34.2983382484 35.0629261139 35.7951111086 36.5272961033 37.259481098 37.9916660927 38.7238510873 39.456036082 40.1882210767 40.9204060714 41.6525910661 42.3847760608 43.1169610555 43.3396865246 43.5487627158 43.757838907 43.9669150982 44.1759912895 44.3850674807 44.5941436719 44.8032198631 45.0122960544 45.2213722456 45.4304484368 45.639524628 45.8486008193 46.0576770105 46.2667532017 46.4758293929 46.6849055842 46.8939817754 47.1030579666 47.3121341578 47.5212103491 47.7302865403 47.9393627315 48.1484389227 48.357515114 48.5665913052 48.7756674964 48.9847436876 49.1938198789 49.4028960701 49.6119722613</losses>
      <lossRatios>0.0113905266834 0.0260726465488 0.0298488432921 0.0319478330478 0.0327313347813 0.0335148365149 0.0342983382484 0.0350629261139 0.0357951111086 0.0365272961033 0.037259481098 0.0379916660927 0.0387238510873 0.039456036082 0.0401882210767 0.0409204060714 0.0416525910661 0.0423847760608 0.0431169610555 0.0433396865246 0.0435487627158 0.043757838907 0.0439669150982 0.0441759912895 0.0443850674807 0.0445941436719 0.0448032198631 0.0450122960544 0.0452213722456 0.0454304484368 0.045639524628 0.0458486008193 0.0460576770105 0.0462667532017 0.0464758293929 0.0466849055842 0.0468939817754 0.0471030579666 0.0473121341578 0.0475212103491 0.0477302865403 0.0479393627315 0.0481484389227 0.048357515114 0.0485665913052 0.0487756674964 0.0489847436876 0.0491938198789 0.0494028960701 0.0496119722613</lossRatios>
      <averageLoss>3.1041e+01</averageLoss>
    </lossCurve>
  </lossCurves>
</nrml>
"""

    EXPECTED_INS_LOSS_CURVE_XML = """<?xml version='1.0' encoding='UTF-8'?>
<nrml xmlns:gml="http://www.opengis.net/gml" xmlns="http://openquake.org/xmlns/nrml/0.4">
  <lossCurves insured="True" investigationTime="50.0" sourceModelTreePath="test_sm" gsimTreePath="test_gsim" unit="USD">
    <lossCurve assetRef="a1">
      <gml:Point>
        <gml:pos>15.48 38.09</gml:pos>
      </gml:Point>
      <poEs>0.999999997939 0.979591834716 0.959183671492 0.938775508269 0.918367345046 0.897959181823 0.877551018599 0.857142855376 0.836734692153 0.81632652893 0.795918365706 0.775510202483 0.75510203926 0.734693876037 0.714285712813 0.69387754959 0.673469386367 0.653061223144 0.63265305992 0.612244896697 0.591836733474 0.571428570251 0.551020407028 0.530612243804 0.510204080581 0.489795917358 0.469387754135 0.448979590911 0.428571427688 0.408163264465 0.387755101242 0.367346938018 0.346938774795 0.326530611572 0.306122448349 0.285714285125 0.265306121902 0.244897958679 0.224489795456 0.204081632232 0.183673469009 0.163265305786 0.142857142563 0.122448979339 0.102040816116 0.081632652893 0.0612244896697 0.0408163264465 0.0204081632232 0.0</poEs>
      <losses>40.5835007034 64.7589894039 68.2290884469 72.2352920271 76.6619796786 81.0886673304 85.5153549819 90.2825741496 95.6331850701 100.983795991 106.334406911 111.685017832 117.035628752 122.386239672 127.736850593 133.087461513 138.438072434 143.788683354 149.139294275 152.893163627 156.604253694 160.315343761 164.026433827 167.737523894 171.448613961 175.159704027 178.870794094 182.581884161 186.292974227 190.004064294 193.715154361 197.426244427 201.137334494 204.848424561 208.559514628 212.270604695 215.981694761 219.692784828 223.403874895 227.114964961 230.826055028 234.537145095 238.248235161 241.959325228 245.670415295 249.381505361 253.092595428 256.803685495 260.514775562 264.225865628</losses>
      <lossRatios>0.0135278335678 0.0215863298013 0.0227430294823 0.0240784306757 0.0255539932262 0.0270295557768 0.0285051183273 0.0300941913832 0.0318777283567 0.0336612653302 0.0354448023037 0.0372283392772 0.0390118762506 0.0407954132241 0.0425789501976 0.0443624871711 0.0461460241446 0.0479295611181 0.0497130980916 0.0509643878758 0.052201417898 0.0534384479202 0.0546754779424 0.0559125079647 0.0571495379869 0.0583865680091 0.0596235980314 0.0608606280536 0.0620976580758 0.0633346880981 0.0645717181203 0.0658087481425 0.0670457781648 0.068282808187 0.0695198382092 0.0707568682315 0.0719938982537 0.0732309282759 0.0744679582982 0.0757049883204 0.0769420183426 0.0781790483649 0.0794160783871 0.0806531084093 0.0818901384316 0.0831271684538 0.084364198476 0.0856012284982 0.0868382585205 0.0880752885427</lossRatios>
      <averageLoss>1.2755e+02</averageLoss>
    </lossCurve>
    <lossCurve assetRef="a2">
      <gml:Point>
        <gml:pos>15.56 38.17</gml:pos>
      </gml:Point>
      <poEs>0.999997739671 0.979589622534 0.959181505398 0.938773388262 0.918365271126 0.89795715399 0.877549036854 0.857140919718 0.836732802582 0.816324685445 0.795916568309 0.775508451173 0.755100334037 0.734692216901 0.714284099765 0.693875982629 0.673467865492 0.653059748356 0.63265163122 0.612243514084 0.591835396948 0.571427279812 0.551019162676 0.530611045539 0.510202928403 0.489794811267 0.469386694131 0.448978576995 0.428570459859 0.408162342723 0.387754225587 0.36734610845 0.346937991314 0.326529874178 0.306121757042 0.285713639906 0.26530552277 0.244897405634 0.224489288497 0.204081171361 0.183673054225 0.163264937089 0.142856819953 0.122448702817 0.102040585681 0.0816324685445 0.0612243514084 0.0408162342723 0.0204081171361 0.0</poEs>
      <losses>15.0469832111 25.0366769202 27.0635219852 28.2335694374 28.7318896764 29.2302099152 29.7285301542 30.0674389572 30.1333595396 30.199280122 30.2652007044 30.3311212868 30.3970418692 30.4629624516 30.528883034 30.5948036164 30.6607241988 30.7266447812 30.7925653636 30.802031581 30.8099894578 30.8179473346 30.8259052114 30.8338630882 30.841820965 30.8497788418 30.8577367184 30.8656945952 30.873652472 30.8816103488 30.8895682256 30.8975261024 30.9054839792 30.913441856 30.9213997328 30.9293576096 30.9373154862 30.945273363 30.9532312398 30.9611891166 30.9691469934 30.9771048702 30.985062747 30.9930206238 31.0009785006 31.0089363774 31.016894254 31.0248521308 31.0328100076 31.0407678844</losses>
      <lossRatios>0.00752349160553 0.0125183384601 0.0135317609926 0.0141167847187 0.0143659448382 0.0146151049576 0.0148642650771 0.0150337194786 0.0150666797698 0.015099640061 0.0151326003522 0.0151655606434 0.0151985209346 0.0152314812258 0.015264441517 0.0152974018082 0.0153303620994 0.0153633223906 0.0153962826818 0.0154010157905 0.0154049947289 0.0154089736673 0.0154129526057 0.0154169315441 0.0154209104825 0.0154248894209 0.0154288683592 0.0154328472976 0.015436826236 0.0154408051744 0.0154447841128 0.0154487630512 0.0154527419896 0.015456720928 0.0154606998664 0.0154646788048 0.0154686577431 0.0154726366815 0.0154766156199 0.0154805945583 0.0154845734967 0.0154885524351 0.0154925313735 0.0154965103119 0.0155004892503 0.0155044681887 0.015508447127 0.0155124260654 0.0155164050038 0.0155203839422</lossRatios>
      <averageLoss>1.5234e+01</averageLoss>
    </lossCurve>
    <lossCurve assetRef="a3">
      <gml:Point>
        <gml:pos>15.48 38.25</gml:pos>
      </gml:Point>
      <poEs>1.0 0.979591836735 0.959183673469 0.938775510204 0.918367346939 0.897959183673 0.877551020408 0.857142857143 0.836734693878 0.816326530612 0.795918367347 0.775510204082 0.755102040816 0.734693877551 0.714285714286 0.69387755102 0.673469387755 0.65306122449 0.632653061224 0.612244897959 0.591836734694 0.571428571429 0.551020408163 0.530612244898 0.510204081633 0.489795918367 0.469387755102 0.448979591837 0.428571428571 0.408163265306 0.387755102041 0.367346938776 0.34693877551 0.326530612245 0.30612244898 0.285714285714 0.265306122449 0.244897959184 0.224489795918 0.204081632653 0.183673469388 0.163265306122 0.142857142857 0.122448979592 0.102040816327 0.0816326530612 0.0612244897959 0.0408163265306 0.0204081632653 0.0</poEs>
      <losses>0.0 0.816326530612 1.63265306122 2.44897959184 3.26530612245 4.08163265306 4.89795918367 5.71428571429 6.5306122449 7.34693877551 8.16326530612 8.97959183673 9.79591836735 10.612244898 11.4285714286 12.2448979592 13.0612244898 13.8775510204 14.693877551 15.5102040816 16.3265306122 17.1428571429 17.9591836735 18.7755102041 19.5918367347 20.4081632653 21.2244897959 22.0408163265 22.8571428571 23.6734693878 24.4897959184 25.306122449 26.1224489796 26.9387755102 27.7551020408 28.5714285714 29.387755102 30.2040816327 31.0204081633 31.8367346939 32.6530612245 33.4693877551 34.2857142857 35.1020408163 35.9183673469 36.7346938776 37.5510204082 38.3673469388 39.1836734694 40.0</losses>
      <lossRatios>0.0 0.000816326530612 0.00163265306122 0.00244897959184 0.00326530612245 0.00408163265306 0.00489795918367 0.00571428571429 0.0065306122449 0.00734693877551 0.00816326530612 0.00897959183673 0.00979591836735 0.010612244898 0.0114285714286 0.0122448979592 0.0130612244898 0.0138775510204 0.014693877551 0.0155102040816 0.0163265306122 0.0171428571429 0.0179591836735 0.0187755102041 0.0195918367347 0.0204081632653 0.0212244897959 0.0220408163265 0.0228571428571 0.0236734693878 0.0244897959184 0.025306122449 0.0261224489796 0.0269387755102 0.0277551020408 0.0285714285714 0.029387755102 0.0302040816327 0.0310204081633 0.0318367346939 0.0326530612245 0.0334693877551 0.0342857142857 0.0351020408163 0.0359183673469 0.0367346938776 0.0375510204082 0.0383673469388 0.0391836734694 0.04</lossRatios>
      <averageLoss>2.0000e+01</averageLoss>
    </lossCurve>
  </lossCurves>
</nrml>
"""

    EXPECTED_AGG_LOSS_CURVE_XML = """<?xml version='1.0' encoding='UTF-8'?>
<nrml xmlns:gml="http://www.opengis.net/gml" xmlns="http://openquake.org/xmlns/nrml/0.4">
  <aggregateLossCurve investigationTime="50.0" sourceModelTreePath="test_sm" gsimTreePath="test_gsim" unit="USD">
    <poEs>1.0 0.979591836735 0.959183673469 0.938775510204 0.918367346939 0.897959183673 0.877551020408 0.857142857143 0.836734693878 0.816326530612 0.795918367347 0.775510204082 0.755102040816 0.734693877551 0.714285714286 0.69387755102 0.673469387755 0.65306122449 0.632653061224 0.612244897959 0.591836734694 0.571428571429 0.551020408163 0.530612244898 0.510204081633 0.489795918367 0.469387755102 0.448979591837 0.428571428571 0.408163265306 0.387755102041 0.367346938776 0.34693877551 0.326530612245 0.30612244898 0.285714285714 0.265306122449 0.244897959184 0.224489795918 0.204081632653 0.183673469388 0.163265306122 0.142857142857 0.122448979592 0.102040816327 0.0816326530612 0.0612244897959 0.0408163265306 0.0204081632653 0.0</poEs>
    <losses>55.3135 115.8387 115.9226 122.2153 133.3778 144.5403 155.7028 164.6824 169.9223 175.1622 180.4021 185.6420 190.8819 196.1218 201.3617 206.6017 211.8416 217.0815 222.3214 225.8414 229.3153 232.7893 236.2632 239.7372 243.2111 246.6851 250.1590 253.6330 257.1069 260.5808 264.0548 267.5287 271.0027 274.4766 277.9506 281.4245 284.8984 288.3724 291.8463 295.3203 298.7942 302.2682 305.7421 309.2160 312.6900 316.1639 319.6379 323.1118 326.5858 330.0597</losses>
    <averageLoss>1.8119e+02</averageLoss>
  </aggregateLossCurve>
</nrml>

    """

    EXPECTED_LOSS_MAP_0_1_XML = """<?xml version='1.0' encoding='UTF-8'?>
<nrml xmlns:gml="http://www.opengis.net/gml" xmlns="http://openquake.org/xmlns/nrml/0.4">
  <lossMap investigationTime="50.0" poE="0.1" sourceModelTreePath="test_sm" gsimTreePath="test_gsim" lossCategory="buildings" unit="USD">
    <node>
      <gml:Point>
        <gml:pos>15.48 38.09</gml:pos>
      </gml:Point>
      <loss assetRef="a1" value="246.041524264"/>
    </node>
    <node>
      <gml:Point>
        <gml:pos>15.56 38.17</gml:pos>
      </gml:Point>
      <loss assetRef="a2" value="31.0017742001"/>
    </node>
    <node>
      <gml:Point>
        <gml:pos>15.48 38.25</gml:pos>
      </gml:Point>
      <loss assetRef="a3" value="48.5874989243"/>
    </node>
  </lossMap>
</nrml>
    """

    EXPECTED_LOSS_MAP_0_2_XML = """<?xml version='1.0' encoding='UTF-8'?>
<nrml xmlns:gml="http://www.opengis.net/gml" xmlns="http://openquake.org/xmlns/nrml/0.4">
  <lossMap investigationTime="50.0" poE="0.2" sourceModelTreePath="test_sm" gsimTreePath="test_gsim" lossCategory="buildings" unit="USD">
    <node>
      <gml:Point>
        <gml:pos>15.48 38.09</gml:pos>
      </gml:Point>
      <loss assetRef="a1" value="227.8571829"/>
    </node>
    <node>
      <gml:Point>
        <gml:pos>15.56 38.17</gml:pos>
      </gml:Point>
      <loss assetRef="a2" value="30.9627805157"/>
    </node>
    <node>
      <gml:Point>
        <gml:pos>15.48 38.25</gml:pos>
      </gml:Point>
      <loss assetRef="a3" value="47.5630255873"/>
    </node>
  </lossMap>
</nrml>"""

    EXPECTED_LOSS_MAP_0_3_XML = """<?xml version='1.0' encoding='UTF-8'?>
<nrml xmlns:gml="http://www.opengis.net/gml" xmlns="http://openquake.org/xmlns/nrml/0.4">
  <lossMap investigationTime="50.0" poE="0.3" sourceModelTreePath="test_sm" gsimTreePath="test_gsim" lossCategory="buildings" unit="USD">
    <node>
      <gml:Point>
        <gml:pos>15.48 38.09</gml:pos>
      </gml:Point>
      <loss assetRef="a1" value="209.672841535"/>
    </node>
    <node>
      <gml:Point>
        <gml:pos>15.56 38.17</gml:pos>
      </gml:Point>
      <loss assetRef="a2" value="30.9237868313"/>
    </node>
    <node>
      <gml:Point>
        <gml:pos>15.48 38.25</gml:pos>
      </gml:Point>
      <loss assetRef="a3" value="46.5385522503"/>
    </node>
  </lossMap>
</nrml>
    """

    @noseattr('qa', 'risk', 'event_based')
    def test(self):
        self._run_test()

    def hazard_id(self):
        job = helpers.get_hazard_job(
            helpers.demo_file("event_based_hazard/job.ini"))

        job.hazard_calculation = models.HazardCalculation.objects.create(
            owner=job.hazard_calculation.owner,
            truncation_level=job.hazard_calculation.truncation_level,
            maximum_distance=job.hazard_calculation.maximum_distance,
            intensity_measure_types_and_levels=(
                job.hazard_calculation.intensity_measure_types_and_levels),
            calculation_mode="event_based",
            investigation_time=50,
            ses_per_logic_tree_path=1)
        job.save()
        hc = job.hazard_calculation

        lt_realization = models.LtRealization.objects.create(
            hazard_calculation=job.hazard_calculation,
            ordinal=1, seed=1, weight=None,
            sm_lt_path="test_sm", gsim_lt_path="test_gsim",
            is_complete=False, total_items=1, completed_items=1)

        gmf_set = models.GmfSet.objects.create(
            gmf_collection=models.GmfCollection.objects.create(
                output=models.Output.objects.create_output(
                    job, "Test Hazard output", "gmf"),
                lt_realization=lt_realization),
            investigation_time=hc.investigation_time,
            ses_ordinal=1)

        with open(os.path.join(
                os.path.dirname(__file__), 'gmf.csv'), 'rb') as csvfile:
            gmfreader = csv.reader(csvfile, delimiter=',')
            locations = gmfreader.next()

            gmv_matrix = numpy.array([[float(x) for x in row]
                                      for row in gmfreader]).transpose()

            rupture_ids = helpers.get_rupture_ids(
                job, hc, lt_realization, len(gmv_matrix[0]))

            for i, gmvs in enumerate(gmv_matrix):
                models.Gmf.objects.create(
                    gmf_set=gmf_set,
                    imt="PGA", gmvs=gmvs,
                    rupture_ids=map(str, rupture_ids),
                    result_grp_ordinal=1,
                    location="POINT(%s)" % locations[i])

        return gmf_set.gmf_collection.output.id

    def actual_data(self, job):
        return ([curve.poes
                 for curve in models.LossCurveData.objects.filter(
                loss_curve__output__oq_job=job,
                loss_curve__aggregate=False,
                loss_curve__insured=False).order_by('asset_ref')] +
                [curve.losses
                 for curve in models.LossCurveData.objects.filter(
                loss_curve__output__oq_job=job,
                loss_curve__aggregate=False,
                loss_curve__insured=False).order_by('asset_ref')] +
                [curve.losses
                 for curve in models.LossCurveData.objects.filter(
                loss_curve__output__oq_job=job,
                loss_curve__aggregate=False,
                loss_curve__insured=True).order_by('asset_ref')] +
                [curve.losses
                 for curve in models.AggregateLossCurveData.objects.filter(
                loss_curve__output__oq_job=job,
                loss_curve__aggregate=True,
                loss_curve__insured=False)] +
                [[point.value
                  for point in models.LossMapData.objects.filter(
                loss_map__output__oq_job=job).order_by(
                    'asset_ref', 'loss_map__poe')]] +
                [[el.aggregate_loss
                 for el in models.EventLoss.objects.filter(
                output__oq_job=job).order_by('-aggregate_loss')[0:10]]])

    def expected_data(self):
        poes = [0, 0.0204, 0.0408, 0.0612, 0.0816, 0.102, 0.1224, 0.1429,
                0.1633, 0.1837, 0.2041, 0.2245, 0.2449, 0.2653, 0.2857,
                0.3061, 0.3265, 0.3469, 0.3673, 0.3878, 0.4082, 0.4286,
                0.449, 0.4694, 0.4898, 0.5102, 0.5306, 0.551, 0.5714,
                0.5918, 0.6122, 0.6327, 0.6531, 0.6735, 0.6939, 0.7143,
                0.7347, 0.7551, 0.7755, 0.7959, 0.8163, 0.8367, 0.8571,
                0.8776, 0.898, 0.9184, 0.9388, 0.9592, 0.9796, 1][::-1]

        losses_1 = [264.2259, 260.5148, 256.8037, 253.0926, 249.3815,
                    245.6704, 241.9593, 238.2482, 234.5371, 230.8261,
                    227.115, 223.4039, 219.6928, 215.9817, 212.2706,
                    208.5595, 204.8484, 201.1373, 197.4262, 193.7152,
                    190.0041, 186.293, 182.5819, 178.8708, 175.1597,
                    171.4486, 167.7375, 164.0264, 160.3153, 156.6043,
                    152.8932, 149.1393, 143.7887, 138.4381, 133.0875,
                    127.7369, 122.3862, 117.0356, 111.685, 106.3344,
                    100.9838, 95.6332, 90.2826, 85.5154, 81.0887,
                    76.662, 72.2353, 68.2291, 64.759, 34.233][::-1]
        losses_2 = [31.04076788, 31.03280999, 31.02485209, 31.0168942,
                    31.00893631, 31.00097841, 30.99302052, 30.98506262,
                    30.97710473, 30.96914683, 30.96118894, 30.95323104,
                    30.94527315, 30.93731525, 30.92935736, 30.92139946,
                    30.91344157, 30.90548367, 30.89752578, 30.88956788,
                    30.88160999, 30.87365209, 30.8656942, 30.8577363,
                    30.84977841, 30.84182052, 30.83386262, 30.82590473,
                    30.81794683, 30.80998894, 30.80203104, 30.79256074,
                    30.72664001, 30.66071928, 30.59479855, 30.52887782,
                    30.46295709, 30.39703636, 30.33111562, 30.26519489,
                    30.19927416, 30.13335343, 30.0674327, 29.72848172,
                    29.23016035, 28.73183899, 28.23351762, 27.06330665,
                    25.03645701, 8.80769991][::-1]
        losses_3 = [49.612, 49.4029, 49.1938, 48.9847, 48.7757, 48.5666,
                    48.3575, 48.1484, 47.9394, 47.7303, 47.5212, 47.3121,
                    47.1031, 46.894, 46.6849, 46.4758, 46.2668, 46.0577,
                    45.8486, 45.6395, 45.4304, 45.2214, 45.0123, 44.8032,
                    44.5941, 44.3851, 44.176, 43.9669, 43.7578, 43.5488,
                    43.3397, 43.117, 42.3848, 41.6526, 40.9204, 40.1882,
                    39.456, 38.7239, 37.9917, 37.2595, 36.5273, 35.7951,
                    35.0629, 34.2983, 33.5148, 32.7313, 31.9478, 29.8488,
                    26.0726, 11.3905][::-1]

        # FIXME(lp) insured losses has not been got from a reliable
        # implementation. This is just a regression test
        insured_losses_1 = [40.5835007, 64.7589890606,
                            68.2290881107, 72.2352916074,
                            76.6619792681, 81.0886669289,
                            85.5153545896, 90.2825736863,
                            95.6331846178, 100.983795549,
                            106.334406481, 111.685017412,
                            117.035628344, 122.386239275,
                            127.736850207, 133.087461138,
                            138.43807207, 143.788683001,
                            149.139293933, 152.893163398,
                            156.604253472, 160.315343546,
                            164.026433621, 167.737523695,
                            171.44861377, 175.159703844,
                            178.870793918, 182.581883993,
                            186.292974067, 190.004064141,
                            193.715154216, 197.42624429,
                            201.137334364, 204.848424439,
                            208.559514513, 212.270604587,
                            215.981694662, 219.692784736,
                            223.40387481, 227.114964885,
                            230.826054959, 234.537145033,
                            238.248235108, 241.959325182,
                            245.670415256, 249.381505331,
                            253.092595405, 256.803685479,
                            260.514775554, 264.225865628]

        insured_losses_2 = [15.04698321, 25.0364570155,
                            27.0633066618, 28.2335176244,
                            28.7318389897, 29.230160355,
                            29.7284817202, 30.067432699,
                            30.1333534304, 30.1992741618,
                            30.2651948932, 30.3311156246,
                            30.3970363561, 30.4629570875,
                            30.5288778189, 30.5947985503,
                            30.6607192817, 30.7266400131,
                            30.7925607445, 30.8020310414,
                            30.8099889362, 30.8179468309,
                            30.8259047257, 30.8338626205,
                            30.8418205152, 30.84977841, 30.8577363048,
                            30.8656941995, 30.8736520943,
                            30.8816099891, 30.8895678838,
                            30.8975257786, 30.9054836734,
                            30.9134415681, 30.9213994629,
                            30.9293573577, 30.9373152524,
                            30.9452731472, 30.953231042,
                            30.9611889368, 30.9691468315,
                            30.9771047263, 30.9850626211,
                            30.9930205158, 31.0009784106,
                            31.0089363054, 31.0168942001,
                            31.0248520949, 31.0328099897,
                            31.0407678844]

        insured_losses_3 = [0., 0.81632653, 1.63265306, 2.44897959,
                            3.26530612, 4.08163265, 4.89795918,
                            5.71428571, 6.53061224, 7.34693878,
                            8.16326531, 8.97959184, 9.79591837,
                            10.6122449, 11.42857143, 12.24489796,
                            13.06122449, 13.87755102, 14.69387755,
                            15.51020408, 16.32653061, 17.14285714,
                            17.95918367, 18.7755102, 19.59183673,
                            20.40816327, 21.2244898, 22.04081633,
                            22.85714286, 23.67346939, 24.48979592,
                            25.30612245, 26.12244898, 26.93877551,
                            27.75510204, 28.57142857, 29.3877551,
                            30.20408163, 31.02040816, 31.83673469,
                            32.65306122, 33.46938776, 34.28571429,
                            35.10204082, 35.91836735, 36.73469388,
                            37.55102041, 38.36734694, 39.18367347, 40.]

        expected_aggregate_losses = [330.0596974, 326.5857542, 323.111811,
                                     319.6378677, 316.1639245, 312.6899813,
                                     309.2160381, 305.7420949, 302.2681517,
                                     298.7942084, 295.3202652, 291.846322,
                                     288.3723788, 284.8984356, 281.4244924,
                                     277.9505491, 274.4766059, 271.0026627,
                                     267.5287195, 264.0547763, 260.5808331,
                                     257.1068899, 253.6329466, 250.1590034,
                                     246.6850602, 243.211117, 239.7371738,
                                     236.2632306, 232.7892873, 229.3153441,
                                     225.8414009, 222.3213759, 217.0814518,
                                     211.8415276, 206.6016035, 201.3616793,
                                     196.1217552, 190.881831, 185.6419069,
                                     180.4019828, 175.1620586, 169.9221345,
                                     164.6822103, 155.7023863, 144.5398623,
                                     133.3773383, 122.2148143, 115.92256,
                                     115.8386574, 55.3134][::-1]

        # FIXME(lp). Event Loss Table data do not come from a reliable
        # implementation. This is just a regression test
        expected_event_loss_table = [330.0596974, 222.4581073, 162.7511019,
                                     115.9594444, 115.8300568, 107.8437644,
                                     105.7095923, 105.0259645, 96.6493404,
                                     93.7629886]

        return [
            poes, poes, poes,
            losses_1, losses_2, losses_3,
            insured_losses_1, insured_losses_2, insured_losses_3,
            expected_aggregate_losses,
            [246.04152426, 227.8571829, 209.67284154, 31.0017742,
             30.96278052, 30.92378683, 48.58749892, 47.56302559, 46.53855225],
            expected_event_loss_table]

    def actual_xml_outputs(self, job):
        """
        Event Loss is in CSV format
        """
        return models.Output.objects.filter(oq_job=job).exclude(
            output_type='event_loss')

    def expected_outputs(self):
        return [self.EXPECTED_LOSS_CURVE_XML,
                self.EXPECTED_LOSS_MAP_0_1_XML,
                self.EXPECTED_LOSS_MAP_0_2_XML,
                self.EXPECTED_LOSS_MAP_0_3_XML,
                self.EXPECTED_AGG_LOSS_CURVE_XML,
                self.EXPECTED_INS_LOSS_CURVE_XML]
