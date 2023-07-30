import cv2
import classes
import numpy as np

white = 255
# black = 0
# dark_gray = 128
# light_gray = 211


def calculate_percent(sample_average, experiment_zero):
    print('3: calculate_percent')
    """ calculate the percent of our sample between our zero and the absolute hundred(white)
    Arg:
        sample_average - number
        zero - number
    Returns values:
        percent - number
    """
    percent = (sample_average - experiment_zero) * (100 / (white - experiment_zero))
    return percent


def area_average(wanted_area, img, index):
    print('2: area_average')
    """ find the average color of the pixels on a selected area
        Arg:
            wanted_area - sample class type
            img - 2D array
        Returns values:
            avg - number
        """
    center_coordinates = (wanted_area.middle.get_position())
    axes_length = (wanted_area.r1, wanted_area.r2)
    my = (center_coordinates[0]-(wanted_area.r1/2)-1).__floor__()
    py = (center_coordinates[0]+(wanted_area.r1/2)+1).__floor__()
    mx = (center_coordinates[1]-(wanted_area.r2/2)-1).__floor__()
    px = (center_coordinates[1]+(wanted_area.r2/2)+1).__floor__()
    mask = np.zeros_like(img)
    mask = cv2.ellipse(mask, center_coordinates, axes_length, 0, 0, 360, (255, 255, 255), -1)
    tmp = np.bitwise_and(img, mask)
    result = tmp[mx:px, my:py]
    cv2.imwrite(index.__str__() + '.png',  tmp)
    # cv2.namedWindow("mask", cv2.WINDOW_NORMAL)
    # cv2.imshow("mask", mask)
    # cv2.namedWindow("tmp", cv2.WINDOW_NORMAL)
    # cv2.imshow("tmp", tmp)
    # cv2.namedWindow("result", cv2.WINDOW_NORMAL)
    # cv2.imshow("result", result)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    a = cv2.mean(result)
    avg = a[0].__floor__()
    return avg

# gray <class 'numpy.ndarray'>
# normal <class 'numpy.ndarray'>


def main():
    i = classes.Input()
    window_name = 'image'
    image = i.img.copy()
    # cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    # cv2.imshow(window_name, image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    control_avg = area_average(i.control, image, 'control')
    d = calculate_percent(control_avg, control_avg)
    print("ctr: ", d)
    for sample in i.samples:
        avg = area_average(sample, image, i.samples.index(sample))
        if avg == white:
            d = 100
        else:
            d = calculate_percent(avg, control_avg)
        print(i.samples.index(sample), ": ", d)


if __name__ == '__main__':
    main()

# TODO: open a github
