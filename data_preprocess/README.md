1. get the data, you can download and extract the **test dataset** from [Google Drive](https://docs.google.com/uc?export=download&id=1_849LvuT3WBEHktBT97P2oMBzeJz7-UP) or [Baidu Disk](https://pan.baidu.com/s/1z1cQiqLUgjfxlWoajIPr0g) (ye1q).
2. for **train data**, you need to download from the [Mixamo](https://www.mixamo.com/), watching this [tutorial](https://github.com/ChrisWu1997/2D-Motion-Retargeting/blob/master/dataset/Guide%20For%20Downloading%20Mixamo%20Data.md) and the JavaScript feasible now from this [site](https://github.com/ChrisWu1997/2D-Motion-Retargeting/blob/master/dataset/mixamo_download_script.java). **Remark**: if the site Mixamo updates, the JavaScript maybe not working. 
3. enter the code folder
4. use code in fbx2bvh.py and convert fbx to bvh (command useful: D:/blender/blender.exe -b -P fbx2bvh.py)
5. open preprocess.ipynb to remove data in the test list (optional)
6. delete .fbx
7. use preprocess.py to create train dataset and test dataset.