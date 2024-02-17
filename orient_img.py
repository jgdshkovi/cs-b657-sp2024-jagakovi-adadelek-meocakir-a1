from PIL import Image
import cv2
from params import FILE_HEADER_BUFFER, RED, BLUE, GREEN, WHITE, BLACK, RGB_BLACK

def orient_image(input_file):
    img = Image.open(input_file)

    pixels = img.load()
    print(img.height, img.width)
    orient = "UD"
    
    if img.width < img.height:
        # image is up/down

        # check for up-right
        count = 0
        for y in range(350, 650):
            # print(pixels[3, y], BLACK)
            # break
            black_count = sum(1 for x in range(img.width) if pixels[x, y] == BLACK)
            if black_count < 4:
                # print(y)
                count += 1
        if count/300>0.95:
            orient = "UD"    
            rotated_image = img.rotate(0, expand=True)
            rotated_image.save('correct side up.jpg') 
            rotated_image.show()        
        else:
            count = 0
            y1 = 2200- 650
            y2 = 2200- 350
            for y in range(y1, y2):
                # print(pixels[3, y], BLACK)
                # break
                black_count = sum(1 for x in range(img.width) if pixels[x, y] == BLACK)
                if black_count < 4:
                    # print(y)
                    count += 1
            if count/300>0.95:
                orient = "DU"   
                rotated_image = img.rotate(180, expand=True)
                rotated_image.save('correct side up.jpg') 
                rotated_image.show()
    else:
        # print("img is sideways")
        count = 0
        for x in range(350, 650):
            # print(pixels[3, y], BLACK)
            # break
            black_count = sum(1 for y in range(img.height) if pixels[x, y] == BLACK)
            if black_count < 4:
                # print(y)
                count += 1
        if count/300>0.95:
            orient = "LR" 
            rotated_image = img.rotate(-90, expand=True)
            rotated_image.save('correct side up.jpg') 
            rotated_image.show()
        else:
            count = 0
            x1 = 2200- 650
            x2 = 2200- 350
            for x in range(x1, x2):
                # print(pixels[3, y], BLACK)
                # break
                black_count = sum(1 for y in range(img.height) if pixels[x, y] == BLACK)
                if black_count < 4:
                    # print(y)
                    count += 1
            if count/300>0.95:
                orient = "RL" 
                rotated_image = img.rotate(90, expand=True)
                rotated_image.save('correct side up.jpg') 
                rotated_image.show()
    print(orient)
    # angle = 0
    # if orient=="UD":
    #     angle = 0
    # if orient=="DU":
    #     angle = 180
    # if orient=="LR":
    #     angle = -90
    # if orient=="DU":
    #     angle = 90
    
    # rotated_image = img.rotate(angle, expand=True)
    # rotated_image.save('correct side up.jpg') 
    # rotated_image.show()
    return orient



print('orient')
# returns TOP-BOTTOM
rotated = orient_image("injected_rotated.jpg")
# rotated.save('correct side up.jpg')    
# print(rotated)