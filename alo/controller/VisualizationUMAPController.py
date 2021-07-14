'''
VisualizationUMAPController
'''

import numpy as np
import pandas as pd
import datetime as dt
import umap
from ..api.singelSteel import data_names, without_cooling_data_names, specifications


class getVisualizationUMAP:
    '''
    getVisualizationUMAP
    '''

    def __init__(self):
        pass
        # print('生成实例')

    def run(self, data):
        X = []
        for item in data:
            process_data = []
            if item[9] == 0:
                for data_name in data_names:
                    process_data.append(item[6][data_name])
                X.append(process_data)
            elif item[9] == 1:
                for data_name in without_cooling_data_names:
                    process_data.append(item[6][data_name])
                X.append(process_data)

        X = pd.DataFrame(X).fillna(0).values.tolist()
        X_embedded = umap.UMAP().fit_transform(X)

        index = 0
        upload_json = {}
        for item in data:
            label = 0
            if item[10] == 0:
                flags = item[7]['method1']['data']
                if np.array(flags).sum() == 5:
                    label = 1
            elif item[10] == 1:
                label = 404

            single = {}
            single["x"] = X_embedded[index][0].item()
            single["y"] = X_embedded[index][1].item()
            single["toc"] = str(item[2])
            single["upid"] = item[0]
            single["label"] = str(label)
            single["status_cooling"] = item[9]
            for name in specifications:
                single[name] = item[6][name] if item[6][name] is not None else 0
            # 新增规格信息
            single["tgtthickness"] = item[5]
            single["slab_thickness"] = item[11]
            single["tgtdischargetemp"] = item[12]
            single["tgttmplatetemp"] = item[13]
            single["cooling_start_temp"] = item[14]
            single["cooling_stop_temp"] = item[15]
            single["cooling_rate1"] = item[16]

            upload_json[str(index)] = single
            index += 1
        return upload_json