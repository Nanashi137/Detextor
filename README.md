**Setup enviroment:**
```
conda create -n <enviroment_name> python=3.9 #or use -p with a specific path
pip install -r requirements.txt
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118 #install torch with cuda independently 
```
**Download pretrained model:** <br>
 &nbsp;&nbsp;&nbsp;&nbsp;Download [big-lama](https://drive.google.com/drive/folders/1wpY-upCo4GIW4wVPnlMh_ym779lLIG2A?usp=sharing) folder. <br>
 &nbsp;&nbsp;&nbsp;&nbsp;Put the big-lama folder inside a ./pretrained_models folder.
