import os
import random

main = 'C:/Users/amir/Google Drive/scaffold_3_sempy/files/'
# main = 'D:/google_drive/scaffold_3_sempy/files/'
# main = '/home/amir/google_drive/scaffold_3_sempy/files/'
sem_originals = main + 'sem_originals/'
sem_measurements = main + 'sem_measurements/'
sem_adjusted = main + 'sem_adjusted/'
sem_output = main + 'sem_output/'
sem_cropped = main + 'sem_cropped/'
sem_temp = main + 'temp/'


sem_extension = 'tif'
bin_numbers = 10
delete_zeros = True
variable_list = 'Area,Circ.'


params = [8.426708993225787, 121.94985256081716, 74.34424657112046, 174.5166907800368]
min_threshold, max_threshold, min_diameter, max_diameter = params


error = 0.2