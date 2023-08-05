from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__license__ = 'MIT'
__maintainer__ = ['Avinash Kori']
__email__ = ['koriavinash1@gmail.com']


import os
import sys
from time import gmtime, strftime
from google_drive_downloader import GoogleDriveDownloader as gdd
from os.path import expanduser
home = expanduser("~")

model_path = os.path.join(home, '.DeepBrainSeg/BestModels')
if (not os.path.exists(model_path)) or (os.listdir(model_path) == []):
	os.makedirs(model_path)
	print ("[INFO: DeepBrainSeg] (" + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()) + ") " + 'Tramisu_3D_FC57_best_acc.pth.tar')
	gdd.download_file_from_google_drive(file_id='1FM0zMBZ1Njdc63KfZ9jDc9qzib6d5A7v',
                                    dest_path=os.path.join(model_path, 'Tramisu_3D_FC57_best_acc.pth.tar'))

	print ("[INFO: DeepBrainSeg] (" + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()) + ") " + 'Tramisu_2D_FC57_best_loss.pth.tar')
	gdd.download_file_from_google_drive(file_id='1JrTIV65ZTyPTMNswYXRF5R92xFYaV1y6',
                                    dest_path=os.path.join(model_path, 'Tramisu_2D_FC57_best_loss.pth.tar'))

	print ("[INFO: DeepBrainSeg] (" + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()) + ") " + 'BrainNet_3D_best_acc.pth.tar')
	gdd.download_file_from_google_drive(file_id='1Fu13If4JNEqTbD8x8JHA74aoQxVYv-Ma',
                                    dest_path=os.path.join(model_path, 'BrainNet_3D_best_acc.pth.tar'))

	print ("[INFO: DeepBrainSeg] (" + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()) + ") " + 'ABL_CE_best_model_loss_based.pth.tar')
	gdd.download_file_from_google_drive(file_id='1HUbx3xXFvGU2eQ66N7vcaCLqNChIekxM',
                                    dest_path=os.path.join(model_path, 'ABL_CE_best_model_loss_based.pth.tar'))
else :
	print ("[INFO: DeepBrainSeg] (" + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()) + ") " + 'Skipping Download Files already exists')


print ("[INFO: DeepBrainSeg] (" + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()) + ") " + 'Ants Installation')

ants_path = os.path.join(home, '.DeepBrainSeg/ants')
current_path = os.getcwd()
if (not os.path.exists(ants_path)) or (os.listdir(ants_path) == []):
	os.makedirs(os.path.join(ants_path, 'code')) 
	os.chdir(os.path.join(ants_path, 'code'))
	os.system('git clone https://github.com/stnava/ANTs.git')
	os.makedirs(os.path.join(ants_path, 'bin/antsBuild'))
	os.chdir(os.path.join(ants_path, 'bin/antsBuild'))

	try:
		print (os.getcwd())
		os.system('cmake '+os.path.join(ants_path, 'code/ANTs'))
		os.system('make -j 2')
	except:
		print ("[INFO: DeepBrainSeg] (" + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()) + ") " + 'Cmake Latest version installation')
		os.system('wget https://github.com/Kitware/CMake/releases/download/v3.15.3/cmake-3.15.3.tar.gz')
		os.system('tar xvzf cmake-3.15.3.tar.gz')
		os.chdir('cmake-3.15.3')
		os.system('./bootstrap')
		os.system('make')
		os.system('sudo make install')

		os.system('cmake '+os.path.join(ants_path, 'code/ANTs'))
		os.system('make -j 2')

	os.chdir(os.path.join(ants_path, 'bin/antsBuild/ANTS-build')) 
	os.system('make install 2>&1 | tee install.log')

os.chdir(current_path)

bet_path = os.path.join(home, '.DeepBrainSeg/bets')
current_path = os.getcwd()
if (not os.path.exists(bet_path)) or (os.listdir(bet_path) == []):
        os.makedirs(bet_path, exist_ok=True)
        os.chdir(bet_path)
        os.system('git clone https://github.com/MIC-DKFZ/HD-BET')
        os.chdir(os.path.join(bet_path, 'HD-BET'))
        os.system('pip install -e .')
		



