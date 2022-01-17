import numpy as np
import matplotlib.pyplot as plt
import cv2


def show_image(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    plt.imshow(image)
    plt.show()


def valid_image(image):
    # check size
    height, width, layers = np.shape(img)
    if (height != 800 or
        width != 800 or
        layers != 3):
        return False
    # check if dark
    avg_color_per_row = np.average(image, axis=0)
    avg_colors = np.average(avg_color_per_row, axis=0)
    print('Average colors sum: {:3.1f}'.format(avg_colors.sum()))
    if avg_colors.sum() < 10:
        return False
    # check if blury
    laplacian_var = cv2.Laplacian(img, cv2.CV_64F).var()
    print('Laplacian variable: {:4.1f}'.format(laplacian_var))
    if laplacian_var < 350:
        return False
    return True


if __name__ == '__main__':

    img = cv2.imread('example_images/blurr.png')
    result = valid_image(img)
    if result:
        print('Image is correct')
    else:
        print('Image is incorrect')

    show_image(img)

    img = cv2.imread('example_images/light_blurr.png')
    result = valid_image(img)
    if result:
        print('Image is correct')
    else:
        print('Image is incorrect')

    show_image(img)

    img = cv2.imread('example_images/good.png')
    result = valid_image(img)
    if result:
        print('Image is correct')
    else:
        print('Image is incorrect')

    show_image(img)