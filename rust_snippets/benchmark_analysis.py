#!/usr/bin/env python

from __future__ import print_function

import json
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib import collections

import argparse

data_run_1 = [
    [936.9390178217823, 936.9514752475249, 936.983300990099, 937.1064257425743, 937.162291089109, 942.2369742574257, 957.928596039604, 965.350502970297, 973.9054910891089, 992.7786039603959],
    [938.8820495049505, 938.962104950495, 939.0282277227723, 939.222396039604, 939.2274356435644, 939.233798019802, 939.3271683168317, 939.4318910891088, 950.7690277227723, 963.0895049504951],
    [938.4214633663366, 938.4651247524753, 938.4715168316832, 938.4790217821783, 938.4872653465346, 938.5477089108911, 939.3126495049504, 941.2063227722773, 949.3787623762377, 950.2716673267328],
    [932.8412158415842, 932.9603306930693, 933.0592297029702, 933.0697762376238, 933.1750930693069, 933.3159029702971, 933.9662633663366, 934.360295049505, 934.5942613861386, 937.7966257425743],
    [939.4584198019803, 945.4972079207921, 950.870291089109, 952.5445029702971, 954.7401980198019, 958.3372851485149, 960.1108712871287, 960.8565386138614, 978.6521861386138, 981.3234118811881],
    [937.7431603960396, 937.7735267326733, 937.9121544554455, 938.1376059405941, 950.2989445544555, 952.0052396039604, 953.3402475247525, 955.4446792079209, 959.9284455445545, 991.2856811881187],
    [939.4012118811881, 939.404394059406, 939.4576792079208, 939.4940198019801, 939.5051663366337, 939.6084891089109, 939.6578217821782, 939.730586138614, 939.7923702970296, 955.0923148514851],
    [933.2412415841584, 935.2135148514852, 939.586798019802, 942.1710574257427, 942.7164594059406, 946.3556435643563, 947.1767326732673, 947.776495049505, 954.8047247524752, 956.0851524752476],
    [941.3928673267327, 941.5737366336634, 941.6413346534653, 941.6480158415841, 941.7577306930694, 941.7669168316831, 941.9393702970297, 942.1023485148515, 946.174700990099, 949.9951722772278],
    [936.6203762376239, 936.6308891089109, 936.708693069307, 936.7243801980198, 936.7316435643564, 936.7468396039603, 936.7475287128714, 936.9528396039603, 937.541798019802, 957.3243861386138],
    [935.5727306930694, 935.6014732673268, 935.7803267326732, 935.8194752475248, 935.8351485148515, 935.8906099009901, 936.0038178217821, 936.1969603960397, 937.8703663366337, 938.6487584158416],
    [939.8891861386139, 940.0606910891089, 940.1008633663366, 940.738403960396, 951.7597405940594, 954.6346475247525, 956.7378633663367, 958.2439900990099, 964.4786752475247, 993.6164574257426],
    [936.883697029703, 937.0054158415842, 937.0122376237623, 937.0157287128712, 937.0817247524752, 937.1025207920792, 937.2044356435644, 937.3934415841585, 956.0564891089109, 973.8146891089109],
    [935.7198950495049, 935.7251247524753, 935.9440237623762, 935.9512178217822, 936.2207881188118, 936.4058059405941, 936.5386356435644, 936.6127346534654, 952.3110732673267, 970.3779742574258],
    [939.3096613861386, 939.3687603960395, 939.4171821782178, 939.5332633663367, 939.9494356435644, 941.0720554455446, 955.2563168316831, 964.2058178217821, 978.8590693069308, 985.012302970297],
    [936.2279603960396, 936.9399089108912, 937.1417049504951, 938.0422752475248, 954.2265584158415, 958.4034554455445, 960.1885584158416, 975.5460415841584, 984.2422435643564, 984.8753544554455],
    [935.434887128713, 935.4739564356435, 935.492712871287, 935.5182534653464, 935.5681504950495, 935.5890792079208, 935.5961762376238, 935.615885148515, 935.7644534653466, 935.7710534653465],
    [937.5251465346535, 937.5414118811882, 937.6481722772278, 937.678310891089, 937.6870811881188, 937.7371544554455, 937.7583306930693, 937.8345267326733, 953.9094178217822, 966.1485247524752],
    [938.2473287128713, 938.3577168316831, 938.4551445544554, 938.742910891089, 951.3441148514851, 961.5853999999999, 963.7369445544555, 980.3954138613861, 988.6925920792079, 991.5872059405941],
    [935.5723089108911, 935.8472198019803, 936.1159603960396, 936.7412118811881, 939.2345485148514, 939.8197623762376, 940.1555722772277, 944.0299386138613, 952.8630871287129, 957.6861465346535],
]

data_run_2 = [
    [938.563592079208, 946.2247485148514, 957.0724356435643, 958.5946653465347, 961.4759346534654, 973.734687128713, 974.1153089108911, 974.6874514851486, 982.0901267326733, 990.4019326732673],
    [936.9977742574257, 940.9632792079208, 945.6786118811881, 947.467811881188, 951.8572475247526, 954.5995742574257, 957.536908910891, 960.7841425742574, 971.059093069307, 975.2378356435644],
    [939.4827643564356, 945.3202376237624, 946.7772336633664, 949.0481881188119, 953.7014811881188, 958.6699207920792, 962.0308356435644, 973.0095603960397, 973.4972396039605, 978.379293069307],
    [934.5445603960395, 939.4574792079208, 940.4312910891089, 943.7712376237624, 944.8084376237624, 948.2966297029702, 949.671112871287, 952.0652198019802, 958.9626297029703, 960.0336613861386],
    [942.7392693069306, 946.1993782178217, 952.4990613861386, 956.5614514851485, 959.2770039603961, 964.7887623762376, 970.3279148514852, 975.7012277227723, 982.6069207920791, 985.4880376237622],
    [929.7608376237624, 936.1356297029703, 936.3239821782179, 940.9976930693069, 943.561102970297, 946.6242653465347, 957.1682237623762, 958.8610495049504, 960.9966217821783, 977.8289326732672],
    [944.4037683168316, 949.9661069306932, 952.6803980198019, 956.7712534653465, 960.6449366336634, 967.3931445544554, 968.0388554455445, 983.4690752475249, 984.99760990099, 993.9136178217822],
    [934.5132514851485, 937.275405940594, 939.8444376237624, 941.224001980198, 941.2880297029703, 942.8214514851486, 943.2411485148515, 944.121192079208, 949.6129663366337, 951.8988673267327],
    [931.8153722772278, 939.5871861386139, 949.5945069306931, 957.5068336633664, 958.9076118811881, 968.6653485148516, 968.7611267326732, 970.4297128712872, 981.0398257425743, 983.4024534653466],
    [933.4745762376238, 937.1468792079208, 937.330110891089, 938.8681306930694, 941.3950138613861, 941.4711346534654, 941.7245405940595, 942.2444792079208, 948.2155306930694, 953.1235306930693],
    [937.1145188118812, 946.8892712871286, 955.4195227722772, 958.4910772277228, 964.6965524752476, 966.5736792079208, 967.7059267326732, 973.1660554455445, 973.2581940594059, 982.2263584158416],
    [937.2587108910891, 939.5349900990099, 941.2552891089108, 941.7882633663367, 951.9744653465347, 953.4128198019803, 954.0399623762376, 957.7144158415841, 959.4573861386139, 968.2122891089109],
    [932.0847524752475, 943.1072158415841, 948.07899009901, 948.2886693069306, 948.8492297029703, 951.2509782178219, 956.3317465346535, 956.5122336633663, 961.484499009901, 968.0393504950493],
    [936.4729465346535, 936.5469861386138, 938.6751207920793, 939.192792079208, 947.1470356435643, 949.6745287128713, 955.2347445544555, 956.4662752475248, 964.7258712871287, 971.3571326732673],
    [943.1523742574258, 943.3866475247526, 947.5564118811881, 948.1268415841585, 950.3012316831682, 968.9820732673268, 973.1985683168316, 979.3834356435643, 987.2522396039604, 990.3810356435642],
    [937.2945465346535, 938.619700990099, 945.9297168316832, 946.3176990099009, 952.1998138613861, 953.8867663366337, 954.5833960396039, 956.1197821782179, 964.8686534653465, 966.9203861386138],
    [931.7429069306932, 935.8547445544555, 939.5298415841584, 943.656998019802, 944.1100217821783, 945.2667287128712, 945.4731445544554, 945.6934613861386, 948.4662396039604, 950.6160475247525],
    [935.323403960396, 938.725306930693, 939.5109287128712, 940.1786198019802, 943.3136217821782, 944.3324871287128, 946.68559009901, 951.8468534653466, 952.0611623762376, 965.8365821782178],
    [931.8273148514852, 939.096914851485, 942.2539801980198, 942.661293069307, 946.7289722772276, 949.5933089108911, 954.8386158415842, 955.2322594059405, 955.3019425742574, 957.2062831683169],
    [934.2843663366338, 944.3642752475247, 948.1395900990099, 948.4130435643564, 950.2699267326733, 958.2009465346534, 959.3600910891089, 967.9225683168318, 977.589502970297, 982.5163564356435],
]

data_run_3 = [
    [932.1766554455446, 934.7733168316831, 935.9324198019802, 936.5173287128713, 937.3277168316831, 937.9310356435643, 941.5322673267326, 944.8337227722773, 944.8658772277228, 945.9268772277228, 946.4254712871286, 946.7465188118812, 947.3698851485149, 947.5506891089109, 948.8782277227723, 950.2481366336634, 951.1214158415842, 958.8724534653464, 959.3097128712872, 959.903001980198, 960.3412653465347, 960.7609920792079, 962.4491722772276, 963.5143623762377, 965.5130851485148, 965.9091227722773, 966.7458752475247, 969.7445920792079, 974.3242198019801, 974.4493683168317],
    [931.1730079207921, 937.4190910891089, 939.7745841584159, 940.016695049505, 940.5521108910891, 942.6427485148515, 944.4459445544555, 944.6642158415841, 944.9980099009902, 945.1371544554456, 945.2812930693068, 945.8493544554456, 946.976099009901, 947.1294039603961, 948.9856514851485, 949.0579366336634, 950.0058277227722, 953.8928277227723, 954.0130633663366, 956.2143762376238, 957.2170732673267, 958.0194514851486, 958.4001742574258, 958.8032, 960.2575900990099, 964.3480237623762, 966.4800356435644, 970.8664336633664, 970.9090534653466, 978.8684039603961],
    [933.2698752475247, 938.8447128712871, 939.6182019801981, 940.022203960396, 940.7131544554455, 940.8066158415842, 941.671005940594, 942.5521267326732, 942.7026138613861, 943.2103485148514, 943.5795702970297, 943.6969128712872, 944.0225584158416, 944.7154356435643, 946.9640851485149, 947.2794851485148, 947.8689564356437, 947.8870237623763, 950.027908910891, 951.1087207920792, 952.3386059405941, 952.7735287128713, 952.7826732673267, 954.380605940594, 956.3839386138613, 956.8608752475246, 957.6320118811881, 960.0057960396039, 968.8508712871286, 970.673893069307],
    [932.0745148514851, 936.9459108910892, 938.0716831683168, 938.2799524752476, 939.0350495049504, 940.5327326732673, 940.5475069306931, 940.594394059406, 943.633095049505, 944.3280990099009, 944.6441821782179, 944.9801485148514, 945.1896633663366, 946.8741722772278, 947.3719267326733, 947.7464673267327, 949.9496633663366, 950.4106554455445, 951.594203960396, 952.5401603960396, 952.7311584158416, 953.9549881188118, 955.6203742574257, 955.9242514851485, 956.1817148514851, 961.2604693069306, 961.4620693069307, 963.4795900990099, 963.5312257425743, 971.8986811881189],
    [933.2851544554455, 941.0842871287128, 941.3660178217822, 942.9364277227724, 944.7832118811882, 945.5773148514851, 945.823495049505, 946.1512, 946.1639940594059, 947.7703960396041, 949.2640653465346, 949.294699009901, 949.444295049505, 949.4784732673268, 950.1010653465347, 950.4845386138614, 950.9287405940594, 951.9249188118812, 953.4277188118812, 954.8865603960396, 955.4348435643564, 955.5286811881188, 958.1299960396041, 962.0600475247523, 963.3797148514851, 964.7788693069306, 965.5652732673267, 971.0250495049505, 975.1657702970298, 989.3980851485148],
    [932.4442336633664, 934.6022970297029, 939.4626752475248, 940.2638178217821, 940.7547504950495, 941.0998732673266, 942.0879544554456, 944.8360316831684, 948.618594059406, 948.8891603960396, 949.5998792079207, 949.9039247524753, 950.3316297029702, 951.6184237623762, 953.9102277227722, 954.2283445544555, 956.6100930693069, 958.9243841584158, 959.0419346534654, 959.7117465346535, 960.1130237623762, 961.165201980198, 963.2835722772278, 963.728687128713, 964.4299762376238, 965.6558415841585, 968.1358178217821, 970.9961623762376, 973.5889782178218, 975.7964732673267],
    [934.1371782178218, 938.8210514851486, 939.1844693069307, 939.5458237623764, 939.7304732673267, 940.5253584158415, 940.710099009901, 940.7239643564357, 940.8727287128713, 941.8415940594059, 942.0304455445545, 942.0596019801981, 944.0447544554455, 944.4151980198019, 945.4175544554456, 945.9531762376238, 948.5224257425742, 949.2542891089109, 949.8509861386138, 950.3043306930695, 950.6487663366337, 951.3631841584158, 955.3110554455445, 958.0385999999999, 959.8017207920793, 962.1629980198019, 962.2442336633663, 964.8313524752475, 965.0392118811882, 967.0166415841584],
    [936.3740811881189, 937.652304950495, 937.7057128712871, 938.0605762376238, 938.5043584158417, 941.3249702970297, 942.1039881188119, 951.5816693069307, 953.2915168316831, 955.2241386138613, 956.8799188118812, 958.2035306930693, 959.9575188118812, 960.4184910891089, 960.4948891089108, 961.6452356435643, 964.0155108910891, 964.2809742574258, 964.4073564356436, 965.3264257425742, 965.4786574257427, 965.6357603960396, 965.9899603960396, 967.0505920792078, 971.9651801980198, 976.1752831683168, 981.8703524752475, 985.2394534653464, 988.1996910891088, 990.3568970297031],
    [933.2311485148515, 937.6563089108911, 939.7073207920793, 939.7280851485148, 939.9674693069306, 942.312299009901, 944.3069702970297, 947.2007227722772, 947.5356693069307, 948.1522455445545, 948.2299544554455, 949.6315148514851, 950.507401980198, 950.816095049505, 951.118302970297, 956.4125227722773, 956.8315267326732, 958.3663128712872, 963.322796039604, 963.4042178217823, 965.407398019802, 966.4045702970296, 968.5755306930693, 970.0651524752476, 972.858994059406, 972.9148792079208, 979.7254237623762, 982.5510475247524, 983.1841920792081, 992.0408396039604],
    [936.699702970297, 939.1613247524753, 939.9512811881189, 940.402295049505, 941.5046118811881, 941.670211881188, 942.5493287128713, 943.0104277227723, 943.3072178217822, 943.4645326732674, 943.950893069307, 945.5066871287129, 947.9708495049505, 949.654603960396, 949.7492514851485, 951.2531683168316, 951.3532871287129, 954.508908910891, 954.536594059406, 954.7764613861386, 956.0473148514852, 957.4761128712871, 958.2730950495048, 958.563104950495, 959.6586396039604, 964.3836811881188, 967.0849366336635, 970.7312514851484, 979.1288712871287, 980.0001306930694],
    [933.1601643564356, 934.835299009901, 938.3042336633664, 940.4354356435643, 943.5985485148515, 944.0959643564357, 944.9824891089108, 948.9807821782179, 950.2504693069307, 950.5826396039604, 955.4289267326733, 960.4428178217822, 960.4702871287129, 961.4675089108911, 964.1449564356436, 970.463120792079, 971.1427762376238, 972.2790990099011, 975.1998217821782, 976.0233643564356, 979.8825207920793, 980.1335148514852, 982.2451188118812, 984.2669287128713, 986.163192079208, 987.3035742574258, 991.1851247524752, 992.1063584158417, 992.7919742574256, 993.5945128712871],
    [939.5146, 942.039118811881, 942.4087465346535, 942.4328257425742, 943.4764059405941, 944.3795227722773, 944.5325683168317, 945.3279267326733, 946.1486198019802, 946.2755524752475, 947.6571108910891, 948.5199306930692, 949.4432455445544, 949.6039425742574, 951.0446574257426, 951.5929762376237, 951.718302970297, 951.768506930693, 951.9196495049505, 952.4851485148515, 957.1592455445544, 959.4901564356435, 961.2230079207922, 962.4031940594059, 964.1538554455447, 967.9519445544555, 969.5580356435644, 970.7385722772277, 973.2130613861386, 975.5298138613862],
    [938.9331326732673, 942.029794059406, 943.674592079208, 945.0954871287129, 945.9317089108912, 946.563299009901, 947.6387821782178, 949.7907821782179, 951.1059603960397, 953.7519623762375, 957.470613861386, 958.7735168316832, 959.335706930693, 960.1596237623762, 962.7556435643564, 962.9987861386139, 963.661497029703, 966.9160613861386, 967.3028118811881, 968.0488158415842, 968.3714613861385, 970.6614732673268, 972.3591346534654, 973.7551445544555, 975.0509762376237, 982.0104851485148, 987.9676712871287, 988.7157524752475, 989.5096376237624, 994.338405940594],
    [937.5395465346535, 941.6528435643563, 941.6990732673268, 944.0078257425744, 944.6906495049506, 945.6869207920793, 947.4976495049506, 947.6907584158416, 949.0160257425744, 949.975087128713, 949.9871188118813, 950.4104851485148, 951.5912851485149, 951.8323465346534, 952.0218752475248, 953.9415762376238, 954.818104950495, 955.2580217821783, 956.6122851485148, 957.4560811881188, 957.4981524752475, 958.4040712871287, 958.9198435643564, 961.6977405940595, 963.7759504950494, 967.0524257425743, 970.6163801980198, 970.6634811881188, 972.3211861386138, 976.6019306930693],
    [934.2455643564356, 938.8524970297029, 940.0614475247526, 941.0240673267326, 942.0106158415841, 942.5218376237623, 943.9056613861386, 944.6743881188119, 945.1262871287129, 946.0119168316832, 946.8110495049505, 947.1263108910891, 947.1863584158415, 947.4730811881188, 949.5505623762376, 949.9381623762376, 949.9402396039604, 953.3357188118813, 954.1542316831682, 954.4248554455445, 955.5573623762376, 955.832403960396, 956.1463168316832, 958.1700079207922, 958.3590396039604, 959.0680970297029, 962.5199564356435, 966.7064712871287, 968.2074653465346, 970.5031900990099],
    [936.3243841584158, 937.0011702970297, 939.0943326732673, 942.0270316831684, 946.2585326732673, 947.7454732673267, 948.2747188118811, 949.3728217821782, 955.5538732673268, 959.5763564356436, 962.842306930693, 964.1806831683168, 964.4564554455445, 965.4015227722772, 965.6610772277228, 966.5544237623762, 967.3664851485149, 968.0370495049505, 969.7647584158416, 969.7688495049505, 971.507798019802, 973.8322316831683, 974.9869603960396, 981.5971188118812, 982.2918752475248, 982.3348178217822, 983.0312554455446, 983.0903168316831, 983.3361287128713, 983.3373900990099],
    [933.8034792079209, 941.0511722772277, 941.1000534653466, 941.1619980198019, 943.0487841584159, 943.1494673267326, 944.0605801980198, 944.1917841584159, 944.3147683168318, 945.2568138613861, 945.2710752475247, 945.6100871287128, 946.3345544554455, 946.4588712871287, 947.1277089108911, 947.4380435643565, 947.7480871287129, 948.5135722772277, 953.0809960396039, 953.191392079208, 954.1966475247525, 958.5601762376238, 958.9879049504951, 959.9321148514852, 960.7095900990099, 963.9196138613861, 965.8295326732673, 967.6752910891089, 969.481003960396, 969.6070316831684],
    [939.4846871287128, 939.5477504950495, 940.8966336633663, 941.3738673267327, 941.4504376237625, 943.2512673267327, 944.4433306930692, 944.4640158415841, 945.5060732673268, 947.1598435643565, 947.2610752475247, 947.8020178217822, 950.2658237623762, 954.4167366336634, 955.6016158415841, 956.1155485148515, 956.2194356435643, 956.8622653465346, 957.8741683168316, 958.3153425742574, 958.6667366336634, 959.2106376237623, 959.225392079208, 962.2769960396041, 962.476013861386, 965.1205841584158, 966.485702970297, 967.7773663366336, 971.4527643564356, 990.580095049505],
    [935.939500990099, 939.1755861386139, 939.4976336633663, 940.5929524752477, 941.0124871287129, 943.1170633663367, 943.266499009901, 943.415198019802, 944.0013584158415, 944.2062118811881, 944.647910891089, 945.7333465346535, 945.7939861386138, 947.5777603960397, 949.0233207920792, 949.4414277227723, 951.7741683168317, 952.3574099009901, 952.6398673267327, 953.3318336633664, 954.6515821782178, 955.2296356435643, 956.5277683168317, 956.8057920792079, 958.1133801980197, 959.5062594059406, 960.4059128712871, 963.0222455445545, 972.5980851485149, 973.5365900990098],
    [940.5142495049505, 943.1339603960396, 949.1710376237623, 949.7267742574257, 951.3858831683168, 952.0293168316832, 955.0283128712871, 955.9833326732672, 956.1336435643564, 956.589091089109, 958.2773643564357, 961.3338178217822, 962.2496891089108, 963.3605702970298, 963.4443584158415, 964.3802415841584, 965.3608970297029, 965.9946336633665, 968.9668455445544, 970.5210594059406, 970.9037742574257, 971.8174534653466, 975.222302970297, 975.5270376237625, 978.3861762376238, 980.313912871287, 981.0577207920793, 982.9552811881188, 985.135493069307, 987.2772732673267],
]

data_run_4 = [
    [937.1139465346535, 937.1463069306932, 937.1858534653466, 937.266500990099, 937.3593663366336, 937.4790376237623, 937.5416871287129, 937.5757029702969, 937.6595128712872, 937.7994277227723, 937.8041920792078, 937.8927148514852, 937.9710732673267, 937.9823405940593, 938.0358376237624, 938.0892415841585, 938.1686792079208, 938.2027881188119, 938.3041821782178, 938.3511425742574, 938.5795742574257, 938.8959207920792, 938.9591128712872, 939.1538237623762, 939.7486158415842, 939.9388336633663, 942.8280752475247, 945.8066415841585, 946.1309207920793, 956.8289326732673],
    [935.7789940594059, 937.8617188118812, 937.9251821782177, 938.0097663366337, 938.0211643564356, 938.0520237623763, 938.0685762376238, 938.0942455445544, 938.1001801980198, 938.144087128713, 938.1486554455445, 938.2459366336634, 938.305102970297, 938.3053108910891, 938.3833485148515, 938.3834554455445, 938.4025742574257, 938.5146118811882, 938.5264811881189, 938.541108910891, 938.6808079207922, 938.7415722772278, 938.7527920792079, 938.8450237623763, 944.5531227722771, 947.915302970297, 952.7551603960396, 963.1989663366337, 969.5892198019802, 975.4476118811881],
    [938.9261742574257, 939.2064118811882, 939.2649227722771, 939.3047980198019, 939.3319881188119, 939.333, 939.3419663366336, 939.4304891089108, 939.4331425742574, 939.5111762376238, 939.5138138613862, 939.5619643564356, 939.6749960396039, 939.6847841584158, 939.7637148514851, 939.7744316831684, 939.9841663366336, 940.0473584158417, 940.1029742574258, 940.125700990099, 940.2087564356435, 940.4147287128712, 940.4775881188119, 940.6682079207922, 940.8028990099009, 941.5070118811881, 942.9548574257426, 946.3142257425742, 946.4383267326733, 949.2046891089109],
    [936.2325643564355, 936.233998019802, 936.2869108910891, 936.3513465346535, 936.3998574257425, 936.421304950495, 936.4928475247525, 936.4988673267327, 936.5320891089109, 936.5546178217821, 936.5561108910891, 936.5644237623762, 936.6152455445545, 936.6432970297029, 936.6526811881188, 936.7448594059406, 936.7886574257426, 936.7952475247524, 936.8407524752475, 936.8930237623763, 936.9015544554456, 936.9483564356435, 937.0043782178218, 937.047392079208, 940.0794495049504, 941.3025584158415, 943.1975108910891, 944.234201980198, 956.2532237623763, 964.2578990099009],
    [937.3178831683168, 937.5297346534653, 937.6660178217821, 937.7224673267326, 937.7344772277228, 937.7457900990099, 937.7842257425742, 937.9232792079208, 937.9453762376238, 937.949205940594, 938.1206257425742, 938.2156217821782, 938.2169049504951, 938.3099683168317, 938.3491148514851, 938.4688891089108, 938.5614158415842, 938.7097247524753, 938.933499009901, 939.0109465346535, 939.1195821782178, 939.1517128712871, 939.4886316831684, 939.6426376237624, 939.6892811881188, 940.9938396039604, 941.4880475247525, 941.7857940594059, 942.3380158415841, 944.3113683168317],
    [936.702603960396, 936.7110792079209, 936.7617148514852, 936.7736613861385, 936.7900613861386, 936.8144693069307, 936.8304693069307, 936.8338178217822, 936.8388831683169, 936.8439227722772, 936.8471287128713, 936.8526297029703, 936.8766198019802, 936.889798019802, 936.8978000000001, 936.9074514851485, 936.9703900990098, 937.0296415841584, 937.0356396039604, 937.0516118811881, 937.0967386138614, 937.1475188118811, 938.7456455445545, 938.9486158415842, 939.5629366336633, 940.6359108910891, 942.9011881188119, 943.1287029702971, 944.9738178217821, 964.837295049505],
    [935.8629504950495, 938.0544, 938.0860554455445, 938.1331584158416, 938.1842118811882, 938.2488297029703, 938.3210138613861, 938.345087128713, 938.4029188118811, 938.4282316831684, 938.4452950495049, 938.4545326732673, 938.457403960396, 938.4611227722772, 938.4960613861386, 938.502598019802, 938.586702970297, 938.6267940594059, 938.635495049505, 938.7297584158415, 938.7666653465346, 943.2633326732672, 944.4775564356436, 945.1761227722772, 946.5412198019802, 949.8090772277228, 954.5993702970296, 959.2047386138613, 961.3052019801979, 969.5137623762377],
    [939.7913247524752, 939.8231267326731, 939.8247405940594, 939.8480178217823, 939.8606514851485, 939.8807405940594, 939.8946257425742, 939.9378415841585, 939.9998831683168, 940.0258435643565, 940.0318831683169, 940.0615841584158, 940.1058118811882, 940.2051445544555, 940.2159346534653, 940.2361405940594, 940.2892752475248, 940.3374396039604, 940.3954158415842, 940.4005425742574, 940.4129742574256, 940.504112871287, 940.5703742574257, 940.86440990099, 942.0601999999999, 948.1775188118813, 953.6400316831683, 954.3696851485148, 954.4517999999999, 958.1894534653464],
    [939.3310039603961, 939.3326594059406, 939.3370455445544, 939.505603960396, 939.5191227722772, 939.5605722772277, 939.6112851485149, 939.6963900990098, 939.7178079207921, 939.720596039604, 939.7535841584158, 939.7603584158416, 939.7672574257426, 939.7884732673267, 939.7989049504951, 939.8552871287129, 939.8618851485147, 939.9941247524753, 940.0856356435644, 940.1188792079207, 940.1597326732673, 940.476504950495, 940.5412059405941, 940.6182752475248, 943.079291089109, 951.5651168316831, 951.8061940594059, 952.0891049504951, 959.583299009901, 964.6986198019802],
    [939.6001643564357, 939.6301782178218, 939.6715465346534, 939.7060079207921, 939.7491267326732, 939.8615188118812, 939.8694297029704, 939.8741584158416, 939.8986950495049, 939.9131188118812, 939.9193702970297, 939.931994059406, 940.0207683168317, 940.059893069307, 940.0865425742574, 940.1276316831684, 940.1473603960396, 940.1796752475248, 940.3098752475247, 940.4077762376237, 940.7120495049505, 940.8051207920793, 940.8584633663365, 941.2774198019802, 941.3877366336634, 941.9224831683167, 945.6152475247525, 949.3029623762376, 950.4094574257425, 952.5582910891088],
    [944.0602772277228, 944.2316, 946.4546811881187, 946.4607881188119, 946.600902970297, 949.4760237623763, 952.9279782178219, 957.6979564356435, 959.0647207920791, 959.2765544554455, 960.2442316831684, 960.5347485148515, 961.1372356435643, 962.3829306930693, 964.0954673267327, 964.5823742574258, 965.0105425742574, 967.5180831683167, 967.6226376237624, 968.0537405940595, 969.4912059405941, 971.1982871287129, 974.7539485148515, 977.4689564356436, 981.9490772277229, 982.3928455445545, 984.2255722772278, 989.0215366336633, 997.3641128712871, 1000.4131584158415],
    [936.2534633663365, 936.2798435643564, 936.4925504950495, 936.5371742574257, 936.5481821782178, 936.6179960396039, 936.6734, 936.67639009901, 936.7013801980197, 936.7585029702971, 936.7803089108911, 936.7941386138614, 936.8513029702971, 936.8515386138613, 936.8960257425742, 936.9287425742575, 936.9936356435644, 937.0087762376238, 937.1472514851486, 937.1795584158416, 937.9905524752475, 938.3036000000001, 938.3759326732674, 939.1002257425743, 939.5953148514851, 940.9726297029703, 941.3737980198019, 942.217104950495, 945.9352693069306, 951.8130415841583],
    [935.4701227722773, 938.19880990099, 938.2449346534654, 938.2869247524752, 938.4071089108911, 938.4464851485147, 938.4830198019802, 938.6600277227723, 938.7245326732673, 938.7750198019802, 938.8404158415842, 939.2008356435643, 939.2444356435644, 939.3346752475247, 940.2173366336633, 940.4061683168317, 943.845497029703, 945.3180673267327, 945.8650574257426, 949.879300990099, 950.6119821782179, 951.3482673267326, 951.985594059406, 952.8238772277228, 959.8950554455446, 962.4539188118812, 970.9745207920793, 974.8824099009901, 981.6130415841585, 989.9609346534653],
    [938.90660990099, 938.9969584158416, 940.1251762376238, 942.056201980198, 943.1777980198019, 943.6019762376238, 944.8965564356436, 945.9363643564358, 946.3972396039603, 946.7021881188118, 947.406201980198, 947.5633801980198, 949.1896, 950.702702970297, 952.2090554455445, 952.5713861386139, 952.7436831683169, 953.0214653465347, 953.5201465346535, 953.6277485148514, 955.9683148514852, 956.8416534653466, 956.9656534653466, 957.535796039604, 957.6571960396041, 961.9349980198019, 962.1758613861386, 967.8820554455446, 973.1156752475248, 974.3449861386139],
    [936.2097445544555, 937.3965841584159, 937.4714772277227, 937.518803960396, 937.6201504950495, 937.666293069307, 937.672998019802, 937.7034831683169, 937.7576613861386, 937.9830673267326, 938.0238613861386, 938.3156594059407, 938.3397782178217, 938.3712534653465, 938.9302534653465, 941.667495049505, 941.9636297029703, 942.8957069306931, 942.9342673267327, 943.0154297029703, 944.1908415841584, 944.4597267326733, 949.4803623762376, 951.2206990099011, 951.4844554455445, 953.0667326732673, 954.2376891089109, 958.1331247524752, 965.6745287128713, 979.8573801980198],
    [937.8432039603961, 937.9858970297029, 938.0051108910891, 938.1923485148515, 938.2817287128713, 938.6644574257425, 938.6896633663366, 938.7452475247525, 938.7853485148514, 938.8465326732672, 939.2254455445545, 940.1736198019802, 940.3169445544554, 940.4405702970296, 940.4827504950496, 940.7412613861387, 941.4452732673268, 942.3748514851486, 942.4752910891089, 942.9139841584158, 942.9394554455446, 943.0350772277227, 943.7982891089109, 943.9729683168316, 945.064007920792, 945.2851069306931, 947.1994455445545, 947.4441524752476, 949.9765782178217, 950.7277306930692],
    [941.5965287128713, 941.6185445544555, 941.6750554455446, 941.9084, 942.0101722772278, 942.0269207920792, 942.2086534653465, 942.2602851485149, 942.3397960396039, 942.3709465346535, 942.3722613861386, 942.4556811881189, 942.6347900990099, 942.6924079207921, 942.8383623762377, 943.5061247524752, 943.5445683168317, 943.9207326732674, 945.7009801980198, 947.6950079207921, 948.2358732673267, 948.3073128712872, 950.3272871287129, 951.113500990099, 951.3674811881189, 952.4681366336634, 952.8380633663368, 955.7955108910892, 958.3670198019802, 969.2381207920793],
    [940.8755465346535, 942.3031326732673, 942.4340495049505, 942.4577702970298, 942.5258257425742, 942.5268376237624, 942.6065683168317, 942.6120217821783, 942.6171841584159, 942.6222257425742, 942.6516653465346, 942.6773564356437, 942.7534396039604, 942.8019485148516, 942.9082297029703, 942.9209227722772, 942.9489089108911, 942.9792930693069, 943.020106930693, 943.082192079208, 943.3551762376238, 947.2294336633663, 947.5666732673267, 954.5381108910891, 954.9930772277228, 956.144304950495, 962.0150475247525, 968.0758594059406, 968.8108415841584, 970.9391702970296],
    [947.8633485148515, 949.0724376237624, 952.3688257425742, 954.1195584158415, 956.7673485148515, 959.3404198019803, 960.4337663366337, 960.8918950495049, 961.7574475247526, 963.2634554455445, 963.9567722772277, 963.9820970297029, 965.1789702970297, 965.231807920792, 967.200005940594, 967.4878752475247, 967.8290198019802, 969.2420059405941, 972.5437168316831, 972.5895722772277, 974.6030178217821, 975.4286118811882, 975.8216257425743, 977.4865306930692, 977.8692138613862, 980.9579999999999, 982.5763643564356, 984.4142316831682, 984.4620673267327, 990.0784792079209],
    [937.8863782178217, 937.9445326732674, 937.9979445544554, 938.0237148514851, 938.1606514851485, 938.1832732673267, 938.4378693069308, 940.0082415841583, 940.0542237623762, 940.135295049505, 940.1741801980198, 940.2472693069307, 940.6678336633664, 940.7121603960395, 940.7622495049505, 940.8500277227722, 940.9431366336634, 941.2480396039604, 944.7992396039604, 945.030605940594, 951.2254257425743, 951.6745227722772, 957.1516435643565, 958.9932574257426, 961.9762475247525, 964.2148396039604, 974.9248891089109, 976.2029009900989, 978.5834891089108, 980.0189683168317],
]

data_run = data_run_4

fig, ax = plt.subplots(1, 1, figsize=(16, 8))

num_runs = len(data_run)
num_times = len(data_run[0])

data_transpose = [[times[i] for times in data_run] for i in range(num_times)]

for i in range(num_times):
    #ax.plot(range(1, num_runs + 1), data_transpose[i], "o-", c="b", ms=2, alpha=0.5)
    ax.plot(range(1, num_runs + 1), data_transpose[i], "o-", ms=2, alpha=0.5)

#for i, run in enumerate(data_run_1):
#    ax.plot([i + 1] * len(run), run, "o", c="b", ms=2, alpha=0.5)

plt.show()