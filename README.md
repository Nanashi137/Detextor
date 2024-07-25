**Setup enviroment:**
```
conda create <enviroment_name> python=3.9
pip install -r requirements.txt
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118 #install torch with cuda independently 
```
**Download pretrained model:** 
Download big-lama from this google drive: [big-lama](https://drive.google.com/drive/folders/1wpY-upCo4GIW4wVPnlMh_ym779lLIG2A?usp=sharing) 
Put the big-lama folder inside a ./pretrained_models
