from paddleocr import PaddleOCR
import cv2 as cv 
import numpy as np
from lama_inpaint import inpaint_img_with_lama
import torch
from utils import dilate_mask
import os 
TF_ENABLE_ONEDNN_OPTS=0

def mask_from_box(mask, box):
    cv.polylines(mask, [box], isClosed=True, color=(255,255,255), thickness=-1)
    return mask 

def polygon_region(mask, bbox, offset=0): 
    try:
        pt1 = (int(bbox[0][0]-offset), int(bbox[0][1]-offset))
        pt2 = (int(bbox[1][0]+offset), int(bbox[1][1]-offset))
        pt3 = (int(bbox[2][0]+offset), int(bbox[2][1]+offset))
        pt4 = (int(bbox[3][0]-offset), int(bbox[3][1]+offset))
        
        polygon = [pt1, pt2, pt3, pt4]

        if not type(polygon) == type(np.array([])):
            polygon = np.array(polygon)

        cv.fillConvexPoly(mask, polygon, 255)
        return mask
    except:
        pt1 = (int(bbox[0][0]), int(bbox[0][1]))
        pt2 = (int(bbox[1][0]), int(bbox[1][1]))
        pt3 = (int(bbox[2][0]), int(bbox[2][1]))
        pt4 = (int(bbox[3][0]), int(bbox[3][1]))
        
        polygon = [pt1, pt2, pt3, pt4]

        if not type(polygon) == type(np.array([])):
            polygon = np.array(polygon)

        cv.fillConvexPoly(mask, polygon, 255)
        return mask 


if __name__ == "__main__":
    device = "cuda" if torch.cuda.is_available() else "cpu"
    lama_ckpt = "./pretrained_models/big-lama"
    lama_config = "./lama/configs/prediction/default.yaml"
    out_dir = "./output"
    ocr = PaddleOCR(use_angle_cls=True, lang='en', show_log = False) 

    img_path = "./input" 
    for image in os.listdir(img_path):
        img_name = image.split(".")[0]
        rpath = f"{img_path}/{img_name}.jpg"   
        img = cv.imread(rpath)
        result = ocr.ocr(img, cls=True)[0]
        if result is not None:
            BoundingBoxes = [box[0] for box in result]
            Texts = [text[1][0] for text in result]
            Score = [score[1][1] for score in result]

            # Creating image's mask 
            h, w = img.shape[:2]
            mask = np.zeros((h,w), dtype=np.uint8)
            for i, box in enumerate(BoundingBoxes): 
                mask = polygon_region(mask, box, offset=2)

            # Dilate mask
            dilate_kernel_size = 23
            mask = dilate_mask(mask, dilate_factor=dilate_kernel_size)

            # Inpaint mask 
            mask_p = f"{out_dir}/{img_name}_mask.png"
            img_inpainted_p = f"{out_dir}/{img_name}_inpainted.png"
            img_inpainted = inpaint_img_with_lama(
                img, mask, lama_config, lama_ckpt, device=device)
            cv.imwrite(img_inpainted_p, img_inpainted)
            cv.imwrite(mask_p, mask)
        else:
            mask_p = f"{out_dir}/{img_name}_mask.png"
            img_inpainted_p = f"{out_dir}/{img_name}_inpainted.png"

            cv.imwrite(img_inpainted_p, img)
            cv.imwrite(mask_p, np.zeros((h, w), dtype=np.uint8))


