import json
import os
import numpy as np
import csv
from PIL import Image


#training_data_list = []


chart_type_list =["area", "heatmap", "horizontal bar", "horizontal interval", "line", "manhattan", "map", "pie", "scatter", "scatter-line", "surface", "venn", "vertical bar", "vertical box", "vertical interval"]

bbox_cls_list = ['chart_title', 'axis_title', 'tick_label', 'tick_grouping', 'legend_title', 'legend_label', 'value_label',  'mark_label', 'other']

for file in os.listdir('./data_test/split_1/json/'):
    

    
    if file == ".DS_Store":
        continue
    
       
#for file in os.listdir('./data/json/' + folder):
    g_data = []
    file_dir = './data_test/split_1/images/' + os.path.splitext(file)[0] + '.jpg'
    json_dir = './data_test/split_1/json/'  + file
    
    img = Image.open(file_dir)
    w, h = img.size
    

    with open('./data_test/split_1/json/'  + file) as f:
      data = json.load(f)
     
      chart_type = data['task1']['output']['chart_type']
      chart_type_index = chart_type_list.index(chart_type)

      
      chart_type_oh = np.zeros(15, dtype=int)
      chart_type_oh[chart_type_index] = 1
      
      try:
          bbox = data['task3']['input']['task2_output']['text_blocks']
      except:
          bbox = None
          continue
          
      try:
          bbox_cls = data['task3']['output']['text_roles']
      except:
          bbox_cls = None
          continue
      
      g_data = []
      for i, val in enumerate(bbox):
          
          bbox_id = val['id']
          bbox_x0 = val['polygon']['x0']
          bbox_x1 = val['polygon']['x1']
          bbox_x2 = val['polygon']['x2']
          bbox_x3 = val['polygon']['x3']
          bbox_y0 = val['polygon']['y0']
          bbox_y1 = val['polygon']['y1']
          bbox_y2 = val['polygon']['y2']
          bbox_y3 = val['polygon']['y3']
          
          for bb_i, bb_val in enumerate(bbox_cls):
              
              if bb_val['id'] == bbox_id:
                  bbox_id_cls = bb_val['role']
          
          
          #bbox_cls_oh = np.zeros(9, dtype=int)
          bbox_cls_index = bbox_cls_list.index(bbox_id_cls)
          #bbox_cls_oh[bbox_cls_index] = 1
          
          if bbox_cls_index == 2:
              bbox_cls_oh = 1
          else:
              bbox_cls_oh = 0
          
          g_item = []
          g_item.append(bbox_id)
          g_item.append(chart_type)
          g_item.extend(chart_type_oh)
          g_item.append(w)
          g_item.append(h)
          g_item.append(bbox_x0)
          g_item.append(bbox_x1)
          g_item.append(bbox_x2)
          g_item.append(bbox_x3)
          g_item.append(bbox_y0)
          g_item.append(bbox_y1)
          g_item.append(bbox_y2)
          g_item.append(bbox_y3)
          g_item.append(bbox_cls_oh)
          
          g_data.append(g_item)
          #print("yess")
          #g_data.append([bbox_id, chart_type_oh, bbox_x0, bbox_x1, bbox_x2, bbox_x3, bbox_y0, bbox_y1, bbox_y2, bbox_y3, bbox_cls_oh])
          
      with open('./data_test/split_1/csv/' + os.path.splitext(file)[0] + '.csv', 'w+') as csvf:
          #print(g_data)
          csvw = csv.writer(csvf)
          header = ["id", "chart_type", "chart_1", "chart_2", "chart_3", "chart_4", "chart_5", "chart_6", "chart_7", "chart_8", "chart_9", "chart_10", "chart_11", "chart_12", "chart_13", "chart_14", "chart_15", "width", "height", "x0", "x1", "x2", "x3", "y0", "y1", "y2", "y3", "class"]
          csvw.writerow(header)
          csvw.writerows(g_data)
          
      
     
    
      #print(g_data)
      """
      with open('./data/csv/' + folder + '/' + os.path.splitext(file)[0] + '.csv', 'w+') as csvf:
          csvw = csv.writer(csvf)
          header = ["id", "chart", "x0", "x1", "x2", "x3", "y0", "y1", "y2", "y3", "class"]
          csvw.writerow(header)
          csvw.writerows(g_data)
      """
      #print(bbox_cls_oh)
      #break

    #training_data_list.append((file_dir, chart_type_oh))


