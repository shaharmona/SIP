import cv2
import classes
import numpy as np

white = 255


# black = 0
# dark_gray = 128
# light_gray = 211


def calculate_percent(sample_average, experiment_zero):
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
    """ find the average color of the pixels on a selected area
        Arg:
            wanted_area - sample class type
            img - 2D array
        Returns values:
            avg - number
        """
    center_coordinates = (wanted_area.middle.get_position())
    axes_length = (wanted_area.r1, wanted_area.r2)
    my = (center_coordinates[0] - (wanted_area.r1 / 2) - 1).__floor__()
    py = (center_coordinates[0] + (wanted_area.r1 / 2) + 1).__floor__()
    mx = (center_coordinates[1] - (wanted_area.r2 / 2) - 1).__floor__()
    px = (center_coordinates[1] + (wanted_area.r2 / 2) + 1).__floor__()
    mask = np.zeros_like(img)
    mask = cv2.ellipse(mask, center_coordinates, axes_length, 0, 0, 360, (255, 255, 255), -1)
    tmp = np.bitwise_and(img, mask)
    result = tmp[mx:px, my:py]
    a = cv2.mean(result)
    avg = a[0].__floor__()
    return avg


def analyzing_function(my_input):
    image = cv2.imread(my_input.img, 0)
    control_avg = area_average(my_input.control, image, 'control')
    check_control = calculate_percent(control_avg, control_avg)
    print("ctr: ", check_control)
    for sample in my_input.samples:
        avg = area_average(sample, image, my_input.samples.index(sample))
        if avg == white:
            check_control = 100
        else:
            check_control = calculate_percent(avg, control_avg)
        print(my_input.samples.index(sample), ": ", check_control)
    return True
