'''
@author: santhosh
'''
from datetime import datetime
import os
import sys

import AppUtil
from util import StatConstants


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print 'Usage: python -m \"tryout.testItunes\" csvFolder'
        sys.exit()
    csvFolder = sys.argv[1]
    currentDateTime = datetime.now().strftime('%d-%b--%H:%M')
    plotDir = os.path.join(os.path.join(os.path.join(csvFolder, os.pardir), 'stats'), 'it')

#     bnss_list = ['284235722']
#     AppUtil.detectAnomaliesForBnsses(csvFolder, plotDir,
#                                      StatConstants.MEASURE_CHANGE_THRES_ITUNES,
#                                      doPlot=True, dologStats=True, bnss_list=bnss_list)

    bnss_key_time_wdw_list = [('284235722', (147,152)),
                              ]
    AppUtil.doGatherEvidence(csvFolder, plotDir, bnss_key_time_wdw_list=bnss_key_time_wdw_list)