import os
import random
import shutil
import cv2
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from scipy.signal import _savitzky_golay
import parameters
from statistics import stdev


class Tools:
    """
    Handy tools and small functions.
    """
    def str_to_float_bracket(self, string):
        """
        converts string of list to list of floats:

        Parameters:
            string (str): "[a, b, c, d]"

        Return:
            (list): [a, b, c, d]
        """
        list = []
        splitted = string.strip('[]').split(' ')

        for i in splitted:
            try:
                list.append(float(i))
            except:
                pass
        return list

    def str_to_float_tuple(self, string):
        """
        converts string of tuple to list of floats:

        Parameters:
            string (str): "(a, b, c, d)"

        Return:
            (list): [a, b, c, d]
        """
        list_new = []
        splitted = string.strip('()').split(',')

        for i in splitted:
            try:
                list_new.append(float(i))
            except:
                pass
        return list(map(int, list_new))


    def new_column(self, column):
        """
        Converts:     column
                     | a  b |       |a|b|
                     | .  . | -->   |.|.|
                     | .  . |       |.|.|

        Parameters:
            column (str): String of n dimensional dataframe

        Return:
            column_new_list (DataFrame): n dimensional DataFrame
        """
        column_new_list = []
        column_items = column.values
        for i in column_items:
            column_new_list.append(self.str_to_float_bracket(i))
        return column_new_list

    def common_indices(self, list_1, list_2):
        """
        Find indices of common items in list_1 and list_2.

        Parameters:
            list_1 (list): first list to be compared
            list_2 (list): second list to be compared

        Return:
            indices (list): [[a,b], [c,d], ...] where a is index of first common file in list_1 and b is index of the
            first common file in second list (list_2), c is index of second common file in list_1 and d is index of
            the second common file in second list (list_2)...
        """
        indices = []
        for i, x in enumerate(list_1):
            for j, y in enumerate(list_2):
                if x == y:
                    indices.append([i, j])
        return indices

    def normal_obj(self, a, b):
        """
        calculates normalized values of difference for two variables.

        Parameters:
            a (float): first value
            b (float): second value

        Return:
            normalized (float): |a-b|/ave(a,b)
        """
        normalized = abs(a - b) / ((a + b) / 2)
        return normalized

    def smooth(self, x, y):
        """
        Smoothens a function f(x,y).

        Parameters:
            x (list): variable values of the original fuction
            y (list): function values of the original fuction

        Return:
            X (list): Variable values of smoothed function
            Y (list): Function values of smoothed function
        """
        # X = np.linspace(0, x[-1], 18)

        def smooth_calc(y, box):
            box = np.ones(box)/box
            Y = np.convolve(y, box, mode='same')
            return Y

        X = x
        Y = smooth_calc(y, 3)
        return X,Y

    def analyze_distribution(self, x, y):
        """
        Calculates mean, max number and max value of a distribution.

        Parameters:
            x (list): list of distribution variable values
            y (list): list of distribution valiable numbers

        Returns:
            (float): mean of distribution
            (float): maximum variable value of the distribution
            (int): maximum number exist in the distribution
            (float): standard deviation of the distribution
        """
        pore_number = np.sum(y)
        mean = np.dot(x,y)
        mean = np.sum(mean)/pore_number
        max_val = max(x)
        max_num = max(y)
        std = stdev(y)
        return mean, max_val, max_num, std


########################################################################################################################
########################################################################################################################
########################################################################################################################
class Variables:
    """
    Encapsulates variables
    """
    image_processing_parameters = 0
    # image_processing_parameters = 0
    def __init__(self):
        pass

########################################################################################################################
########################################################################################################################
########################################################################################################################
class FilesFolders:
    """
    This class handles Files/Folders.

    Attributes:
        full_address (str): Full address of file/folder.
        overwrite (bool): True when allowing File/Folder to overwrite during operations.
    """

    def __init__(self, full_address = '', overwrite=True):
        """
        This constructor for FilesFolders class.

        Parameters:
            full_address (str): Full address of file/folder
            overwrite (bool): True when allowing overwrite during operations
        """
        self.full_address = full_address
        self.overwrite = overwrite
        self.name = self.full_address.split('/')[-1]  # gets name of file based in its address
        self.address = self.full_address.strip(self.name)

    def random_pick(self):
        """
        Pick a random file within address.

        Return:
            full_address (str): complete file address including name
        """
        original_name = random.choice(os.listdir(self.address))
        full_address = self.address + original_name
        return full_address

    def keep(self):
        """
        This method removes everything in that directory but this file
        """
        for f in os.listdir(self.address):
            if f != self.name:
                try:
                    os.remove(self.address + '/' + f)
                except:
                    try:
                        shutil.rmtree(self.address + '/' + f)
                    except:
                        print('file/folder {} could not be deleted'.format(f))

    def clean(self):
        """
        This method cleans content of folder
        """
        files = os.listdir(self.address)
        try:
            for f in files:
                try:
                    os.remove(self.address + '/' + f)
                except:
                    shutil.rmtree(self.address + '/' + f)
        except:
            print('One or more files/folders could not be deleted from {} directory'.format(self.address))
            raise

    def initiate(self):
        """
        Clean up the project folders before new processing
        """
        all_files_folders = os.listdir(parameters.main)
        desired_folders = ['sem_adjusted', 'sem_cropped', 'sem_output', 'temp']
        allowed_file_folders = desired_folders + ['sem_originals', 'sem_measurements', 'design_points.txt',
                                                  'manual_measurments.txt']
        allowed_addresses = []
        for f in allowed_file_folders:
            allowed_addresses.append(parameters.main + f)
        df_objects = []  # create object of desired folders
        for df in desired_folders:
            df_objects.append(FilesFolders(parameters.main + df))
        for dfo in df_objects:
            if dfo.address in desired_folders:
                dfo.clean()
        removed = []
        for f in all_files_folders:
            if (parameters.main + f) not in allowed_addresses:
                print(f)
                try:
                    os.remove(parameters.main + f)
                except:
                    shutil.rmtree(parameters.main + f)
                removed.append(f)
        if removed:
            print('The following file/folders were removed: {}'.format(removed))

    def backup(self):
        """
        This method backs up files/folders and saves them as *.bak
        """
        try:
            if self.address + self.name + '.bak' in os.listdir(self.address):
                os.remove(self.address + self.name + '.bak')
            shutil.copy(self.address + self.name, self.address + self.name + '.bak')
        except:
            try:
                if self.address + self.name + '.bak' in os.listdir(self.address):
                    shutil.rmtree(self.address + self.name + '.bak')
                shutil.copytree(self.address + self.name, self.address + self.name + '.bak')
            except:
                print('Backing up failed')
                raise


########################################################################################################################
########################################################################################################################
########################################################################################################################
class Experiment:
    """
    This class handles experimental measurements

    Attributes:
        bin_numbers (int): Number of bins for distribution calculation
        variables (str): Variables headers in the measurement files (i.e. 'Area,Circ.')
    """

    def __init__(self, bin_numbers = parameters.bin_numbers, variables=parameters.variable_list):
        """
        The constructor for Experiment class.

        It handles manipulations on experimental data (i.e. read manual measurements and calculate size distribution...)

        Parameters:
            bin_numbers (int): Number of bins for distribution calculation
            variables (str): Variables headers in the measurement files (i.e. 'Area,Circ.')
        """
        self.bin_numbers = bin_numbers
        self.variables = variables

    def distribution_calc(self, variable_name, variable_values):
        """
        Calculates Variable Distribution.

        This method calculates variable distribution based on list of the values.

        Parameters:
            variable_name (str): name of variable
            variable_values (list): list of variable values
        Return:
            (x, y) (tuple):  (variable values, values distribution)
        """
        areas_list = pd.cut(variable_values, self.bin_numbers).value_counts()
        areas_list = areas_list.to_frame()
        areas_list = areas_list.sort_index()
        areas_list = areas_list.reset_index()
        areas_index = areas_list['index'].to_numpy()
        x = [0]
        for i in range(len(areas_index)):
            x.append(areas_index[i].mid)
        y = [0]
        zero_indices = []
        counter = 0
        for j in areas_list[variable_name]:
            if j == 0 and counter > 0:
                zero_indices.append(counter)
            counter += 1
            y.append(j)
        x = np.array(x)
        y = np.array(y)

        return x, y


    def parse_experiment(self):
        """
        This method reads the manually measured variable data following format '.csv' file created by ImageJ
            | ...   |Area   |Circ.  |...
        1   | ...   |A1     |C1     |...
        2   | ...   |A2     |C2     |...
        ... | ...   |...    |...    |...

        save the parsed data to csv file:  containing (variable_name, variable_name distribution) for the sem images in
        'sem_measurements' directory in the following format:

             sem_file|variable_name    |var_number    |...
        1   | ...    |A1     |C1            |...
        2   | ...    |A2     |C2            |...
        ... | ...    |...    |...           |...

        where A1, A2,... and C1, C2, and ... are lists

        :return:
            [area_distributions, elongation_distributions] (list):  where
             area_distributions (DataFrame): ['sem_name', 'Area', 'Area_number']
             elongation_distributions (DataFrame): ['sem_name', 'Circ.', 'Circ._number']
        """
        files = os.listdir(parameters.sem_measurements)
        files_csv = []
        for f in files:
            if 'csv' in f:
                files_csv.append(f)

        parsed = []
        for variable_name in self.variables.split(','):
            sem_measurements_data = pd.DataFrame()
            for f in files_csv:
                file = pd.read_csv(parameters.sem_measurements + f)
                variable_values = file[variable_name]
                x, y = self.distribution_calc(variable_name, variable_values)
                sem_measurements_data = sem_measurements_data.append([[f, x, y]])
            sem_measurements_data.columns = ['sem_name', variable_name, variable_name + '_number']
            sem_measurements_data.to_csv(parameters.sem_output + 'experiment_{}_distribution.csv'.format(variable_name),
                                         index=False)
            parsed.append(sem_measurements_data)
        return parsed

    def area_distribution(self, sem_name):
        """
        This function calculated area distribution from experiment measurements.

        Parameters:
            sem_name (str): name of sem image file with extension (i.e. 'name.tif')

        Return:
            X (list):  list of variable values of the distribution
            Y (list):  list of variable numbers of the distribution
        """
        sem_name_no_ext = sem_name.split('.' + parameters.sem_extension)[-2]
        measurements = self.parse_experiment()
        area_distributions = measurements[0]
        area_distribution_experiment = area_distributions[area_distributions['sem_name'] == sem_name_no_ext + '.csv']
        X = area_distribution_experiment['Area'].values
        Y = area_distribution_experiment['Area_number'].values
        return list(X)[0], list(Y)[0]

    def area_average(self, sem_name):
        tools = Tools()
        x, y = self.area_distribution(sem_name)
        mean, _, _, _ = tools.analyze_distribution(x, y)
        return mean

    def elongation_distribution(self, sem_name):
        """
        This function calculated elongation distribution from experiment measurements.

        Parameters:
            sem_name (str): name of sem image file with extension (i.e. 'name.tif')

        Return:
            X (numpy array):  numpy array of variable values of the distribution
            Y (numpy array):  numpy array of variable numbers of the distribution
        """
        sem_name_no_ext = sem_name.split('.' + parameters.sem_extension)[-2]
        measurements = self.parse_experiment()
        elongation_distributions = measurements[1]
        elongation_distribution_experiment = elongation_distributions[elongation_distributions['sem_name'] == sem_name_no_ext + '.csv']
        X = elongation_distribution_experiment['Circ.'].values
        Y = elongation_distribution_experiment['Circ._number'].values
        return list(X)[0], list(Y)[0]

    def elongation_average(self, sem_name):
        tools = Tools()
        x, y = self.elongation_distribution(sem_name)
        mean, _, _, _ = tools.analyze_distribution(x, y)
        return mean

########################################################################################################################
########################################################################################################################
########################################################################################################################
class Sem:
    """
    This class creates a SEM object able to do manipulations on single SEM file

    Attributes:
        image_address (str): Complete address of SEM file including its name
        min_diameter (int): Minimum diameter of pores in pixel
        max_diameter (int): Maximum diameter of pores in pixel
        min_threshold (float): Minimum threshold value for image segmentation. 0. < min_threshold < 255.
        max_threshold (float): Maximum threshold value for image segmentation. 0. < min_threshold < 255.
        bin_numbers (int): Number of bins used to calculate values distributions
    """
    #   Class attributes

    bin_numbers = parameters.bin_numbers

    def __init__(self, image_address):
        """
        The constructor of Sem class.

        Parameters:
            image_address (str): Complete address of SEM file including its name
        """
        self.address = image_address
        #   Gray scale version of the image
        self.image = cv2.imread(self.address, cv2.IMREAD_GRAYSCALE)
        #   Get image name from its full address
        self.image_name = self.address.split('/')[-1]
        self.image_name_no_ext = self.image_name.split('.' + parameters.sem_extension)[-2]

    def plot(self, plot_show=True, plot_type='all'):
        """
        This method plots four image. Original, threshold, contours and fitted ellipses.

        Parameters:
            plot_show (bool): Determines whether the plot will be shown or not
        Return:
            Plot (object): Four plots: Originals, threshold, contours, and fitted ellipses.
        """
        titles = ['Original', 'Thresholding',
                  'Pore Boundaries', 'Pore Approximations']
        original, threshold = self.threshold()
        contours, _ = self.contour()
        ellipses = self.ellipse_draw()

        if plot_show:
            [area_distribution_values, area_distribution_numbers, average_area,
             eccentricity_distribution_values, eccentricity_distribution_numbers, average_eccentricity,
             angle_distribution_values, angle_distribution_numbers, average_angle] = self.pore_info()
            tools = Tools()

            if 'all_types' in plot_type:
                drawings = [original, threshold, contours, ellipses]
                for i in range(4):
                    plt.subplot(2, 2, i + 1), plt.imshow(drawings[i], 'gray')
                    plt.title(titles[i])
                    plt.xticks([]), plt.yticks([])
                if plot_show:
                    plt.show()
                else:
                    pass
            elif 'rigin' in plot_type:
                """
                plots original image.
                """
                plt.imshow(original, 'gray')
                if plot_show:
                    plt.show()
                else:
                    pass
            elif 'reshol' in plot_type:
                """
                plots thresholded image.
                """
                plt.imshow(threshold, 'gray')
                if plot_show:
                    plt.show()
                else:
                    pass
            elif 'ontour' in plot_type:
                """
                plots contours in the image.
                """
                plt.imshow(contours, 'gray')
                if plot_show:
                    plt.show()
                else:
                    pass
            elif 'llipse' in plot_type:
                """
                plots fitted ellipse in the image.
                """
                plt.imshow(ellipses, 'gray')
                if plot_show:
                    plt.show()
                else:
                    pass
            elif 'psd' in plot_type or 'PSD' in plot_type:
                """
                plots pore size distribution in the image.
                """
                X, Y = tools.smooth(area_distribution_values, area_distribution_numbers)
                plt.plot(X, Y)
                if plot_show:
                    plt.show()
                else:
                    return X, Y
            elif 'ped' in plot_type or 'PED' in plot_type:
                """
                plots pore elongation distribution in the image.
                """
                X, Y = tools.smooth(eccentricity_distribution_values, eccentricity_distribution_numbers)
                plt.plot(X,Y)
                if plot_show:
                    plt.show()
                else:
                    return X, Y
            elif 'pod' in plot_type or 'POD' in plot_type:
                """
                plots pore orientation distribution in the image.
                """
                X, Y = tools.smooth(angle_distribution_values, angle_distribution_numbers)
                plt.plot(X, Y)
                if plot_show:
                    plt.show()
                else:
                    return X, Y
            elif 'all_distributions':
                psd = tools.smooth(area_distribution_values, area_distribution_numbers)
                ped = tools.smooth(eccentricity_distribution_values, eccentricity_distribution_numbers)
                pod = tools.smooth(angle_distribution_values, angle_distribution_numbers)
                titles = ['PSD', 'PED', 'POD']
                drawings = [psd, ped, pod]
                for i in range(3):
                    plt.subplot(3, 1, i + 1), plt.plot(drawings[i][0], drawings[i][1], 'gray')
                    plt.title(titles[i])
                    plt.xticks([]), plt.yticks([])
                if plot_show:
                    plt.show()
                else:
                    return psd, ped, pod
            else:
                print('Plot name is not correct!')
        else:
            pass


    def histogram_show(self, bins=parameters.bin_numbers, plot_show = True):
        plt.hist(self.image, bins)
        if plot_show:
            plt.show()
        return plt.hist(self.image, bins)

    def adjust(self, plot_show=True, write_adjusted=False):
        """
        This method adjusts original the sem image.
        Parameters:
            plot_show (bool): Determines whether the plot will be shown or not
        :return:
            Plot (object): Four plots: Originals, threshold, contours, and fitted ellipses.
        """
        clashe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        cll = clashe.apply(self.image)
        plt.imshow(cll, cmap='gray', vmin=0, vmax=255)
        if plot_show:
            plt.show()
        else:
            pass
        if write_adjusted:
            cv2.imwrite(parameters.sem_adjusted + self.image_name, cll)
        else:
            pass


    def set_scale_bar(self):
        """
        Reads scale bar dimension in pixel.

        Return:
            scale_bar_length (int): Scale bar length in pixel
        """

        if 'scale_bar_dimension.txt' not in os.listdir(parameters.sem_output):
            window_name = 'SEM calibration'  # Window name
            cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
            cv2.resizeWindow(window_name, 800, 600)
            endpoints_location = []  # Reading scale bar end points' locations

            def set_scale(scale_bar_length):
                scale_bar_length = scale_bar_length
                return

            def scale_bar_coordinates(event, x, y, flags, param):
                global scale_bar_length
                if event == cv2.EVENT_LBUTTONDOWN and len(endpoints_location) < 2:
                    cv2.circle(self.image, (x, y), 10, (255, 0,), -1)
                    endpoints_location.append((x, y))
                if len(endpoints_location) == 2:
                    cv2.line(self.image, endpoints_location[0],
                             endpoints_location[1], (255, 0,), 10)
                    scale_bar_length = int(np.sqrt((endpoints_location[0][0] - endpoints_location[1][0]) ** 2 +
                                                   (endpoints_location[0][1] - endpoints_location[1][1]) ** 2))
                    set_scale(scale_bar_length)
                    file = open(parameters.sem_output + 'scale_bar_dimension.txt', 'w+')
                    file.write(str(scale_bar_length))
                    file.close()
                else:
                    pass
                return


            cv2.setMouseCallback(window_name, scale_bar_coordinates)
            while (True):
                cv2.imshow(window_name, self.image)
                if cv2.waitKey(20) == 27:
                    break
            cv2.destroyAllWindows()

            return

        else:
            print("Scale bar dimension file exists in 'sem_output' directory")
            scale_bar_length = int(np.genfromtxt(parameters.sem_output + 'scale_bar_dimension.txt', dtype=float))
            return scale_bar_length


    def set_anlysis_region(self):
        """
        Assigns analysis zone defines by the user.

        Return:
             rectangle (list): List of four points of analysis zone rectangle.
        """
        if 'analysis_region.txt' not in os.listdir(parameters.sem_output):
            window_name = 'SEM calibration'  # Window name
            cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
            cv2.resizeWindow(window_name, 800, 600)

            def crop(event, x, y, flags, param):
                fromCenter = False
                global rectangle
                rectangle = cv2.selectROI(window_name, self.image, fromCenter=False)
                file = open(parameters.sem_output + 'analysis_region.txt', 'w+')
                file.write(str(rectangle[:]))
                file.close()

            cv2.setMouseCallback(window_name, crop)
            cv2.imshow(window_name, self.image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            return

        else:
            file = open(parameters.sem_output + 'analysis_region.txt', 'r')
            rectangle = file.read()
            tools = Tools()
            rectangle = tools.str_to_float_tuple(rectangle)
            print("Analysis file exists in 'sem_outputs' directory!")
            return rectangle[:]

    def threshold(self):
        """
        Calculates thresholding results.

        Return:
            img (numpy array): Original image
            threshold (numpy array): Thresholded image
        """
        img = cv2.imread(self.address, 0)
        img = cv2.medianBlur(img, 5)
        _, threshold = cv2.threshold(img, self.min_threshold, self.max_threshold, cv2.THRESH_BINARY)
        return img, threshold

    def contour(self):
        """
        Calculates the contours based on the thresholded image.

        Return:
            mask (numpy array): Background image all 255.
            contours (list): List of 2D np arrays showing contour points
        """
        _, threshold = self.threshold()
        try:
            _, contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        except:
            contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        mask = np.zeros(threshold.shape, np.uint8)
        cv2.drawContours(mask, contours, -1, (255, 0, 0), 3)
        return mask, contours

    def ellipse_gen(self):
        """
        Generates fitted ellipses.

        Return:
            (x, y), (MA, ma), angle (list): List of tuple (x,y) center of ellipses, tuple (Ma, ma) large and small axes
            of ellipses and angle (float) angle of long axis with horizontal axis (x)
        """
        _, contours = self.contour()
        ellipses = []
        for contour in contours:
            if contour.shape[0] > 5:
                ellipses.append(cv2.fitEllipseAMS(contour))
        acceptable_ellipses = []
        for ellipse in ellipses:
            axes = ellipse[1]
            if min(int(axes[0]), int(axes[1])) >= self.min_diameter and max(int(axes[0]),
                                                                            int(axes[1])) <= self.max_diameter:
                acceptable_ellipses.append(ellipse)
        return acceptable_ellipses

    def ellipse_draw(self, draw_on_original=True):
        """
        Draw the generate ellipses on the original image.

        Parameters:
            draw_on_original (bool): Draws the ellipses on the original sem image if True. Draw them on solid image if False.
        """
        mask, _ = self.contour()
        if draw_on_original:
            mask = cv2.imread(self.address)
        else:
            mask = np.zeros(mask.shape, np.uint8)
        ellipses = self.ellipse_gen()
        for ellipse in ellipses:
            center, axes, angle = ellipse
            center = (int(center[0]), int(center[1]))
            axes = (int(axes[0]), int(axes[1]))
            cv2.ellipse(mask, center, axes, angle, 0, 360, (255, 0, 0), 2)
        return mask

    def pore_info(self):
        """
        Calculates all the pore statistics.

        Return:
            (list): [area distribution values, area distribution numbers, average area,
             eccentricity distribution values, eccentricity distribution numbers, average eccentricity,
             angle distribution values, angle distribution numbers, average angle relative to horizontal axis]
        """

        ellipses = self.ellipse_gen()

        def parse(ellipse):
            """
            Calculates ellipse dimensiones in 'mm' and conve
            :param ellipse:
            :return:
            """
            (x, y), (a, b), angle = ellipse
            x = (x * pixel_length)
            y = (y * pixel_length)
            a = (a * pixel_length)
            b = (b * pixel_length)
            angle = (angle)
            return [x, y, a, b, angle]

        def center_coordinates(ellipse):
            [x, y, a, b, angle] = parse(ellipse)
            return x, y

        def area(ellipse):
            [x, y, a, b, angle] = parse(ellipse)
            return np.pi * a * b

        def eccentricity(ellipse):
            [x, y, a, b, angle] = parse(ellipse)
            return np.sqrt(abs(a ** 2 - b ** 2)) / max(a, b)

        def distribution(list):
            area_dist = pd.cut(list, parameters.bin_numbers).value_counts()
            area_dist = area_dist.to_frame()
            area_dist = area_dist.reset_index()
            area_index = area_dist['index'].to_numpy()
            x = []
            for i in range(len(area_index)):
                x.append(round(area_index[i].mid, 3))
            area_dist['x'] = pd.DataFrame(x)
            area_dist.columns = ['index', 'number', 'value']
            df = []
            df.insert(0, {'value': 0, 'number': 0})
            df = pd.DataFrame(df)
            area_dist = pd.concat([df, area_dist], ignore_index=True, sort=True)
            return [area_dist['value'].values, area_dist['number'].values]

        scale_length = int(np.genfromtxt(parameters.sem_output + 'scale_bar_dimension.txt'))
        pixel_length = 1 / scale_length  # each pixel is mm length
        area_list, ecc_list, angle_list = [], [], []  # area, eccentricity, and angle lists

        for e in ellipses:
            area_list.append(area(e))
            ecc_list.append(eccentricity(e))
            angle_list.append(parse(e)[-1])

        variables = [area_list, ecc_list, angle_list]
        variable_names = ['area_list', 'ecc_list', 'angle_list']
        info = []
        counter = 0
        for var in variables:
            info.append(distribution(var)[0])
            info.append(distribution(var)[1])
            info.append(np.average(var))
            counter += 1
        return info

    def compare_ave(self):
        """
        compares the average values of manual measurement and image processing for the selected sem image.

        Return:
            average_comparison (DataFrame): Dataframe
                                |Manual Measurement  Image Processing  Difference %
                    variable    |
                    area        |
                    elongation  |
                    orientation |      0.000000                          0.000000
        """
        average_comparison = pd.DataFrame()
        exp = Experiment()
        area_values_experiment, area_numbers_experiment = exp.area_distribution(self.image_name)
        area_average_experiment = exp.area_average(self.image_name)
        elongation_values_experiment, elongation_numbers_experiment = exp.elongation_distribution(self.image_name)
        elongation_average_experiment = exp.elongation_average(self.image_name)
        area_values_image_procc, area_numbers_image_procc, area_average_image_procc = self.pore_info()[:3]
        elongation_values_image_procc, elongation_numbers_image_procc, elongation_average_image_procc = self.pore_info()[3:6]
        angle_values_image_procc, angle_numbers_image_procc, angle_average_image_procc = self.pore_info()[6:]
        average_comparison['variable'] = ['area', 'elongation', 'orientation']
        average_comparison['Manual Measurement'] = [area_average_experiment, elongation_average_experiment, 0]
        average_comparison['Image Processing'] = [area_average_image_procc, elongation_average_image_procc, angle_average_image_procc]
        average_comparison['Difference %'] = abs(average_comparison['Manual Measurement'] - average_comparison['Image Processing'])/average_comparison['Manual Measurement']
        average_comparison = average_comparison.set_index('variable')
        average_comparison.at['orientation','Difference %'] = 0
        return average_comparison

    def psd(self, option='compare', show_plot=True):
        """
        Calculates pore size distribution.

        Parameter:
            option (str): 'compare', 'manual_measurement', 'image_processing'
            show_plot (bool): if 'True', plot will be shown

        Return:
            option: 'compare' -->
                area_values_experiment (list): area values obtained from manual measurement
                area_numbers_experiment (list): area numbers obtained from manual measurement
                area_values_image_procc (list): area values obtained from image processing
                area_numbers_image_procc (list): area numbers obtained from image processing

            option: 'manual_measurement' -->
                area_values_experiment (list): area values obtained from manual measurement
                area_numbers_experiment (list): area numbers obtained from manual measurement

            option: 'image_processing' -->
                area_values_image_procc (list): area values obtained from image processing
                area_numbers_image_procc (list): area numbers obtained from image processing
        """
        exp = Experiment()
        area_values_experiment, area_numbers_experiment = exp.area_distribution(self.image_name)
        area_values_image_procc, area_numbers_image_procc, _ = self.pore_info()[:3]

        if option == 'compare':
            plt.plot(area_values_experiment, area_numbers_experiment, label = 'Manual Measurement')
            plt.plot(area_values_image_procc, area_numbers_image_procc, label = 'Image Processing')
            plt.legend()
            if show_plot:
                plt.show()
            return area_values_experiment, area_numbers_experiment, area_values_image_procc, area_numbers_image_procc
        elif option == 'manual_measurement':
            plt.plot(area_values_experiment, area_numbers_experiment, label = 'Manual Measurement')
            if show_plot:
                plt.show()
            return area_values_experiment, area_numbers_experiment
        elif option == 'image_processing':
            plt.plot(area_values_image_procc, area_numbers_image_procc, label = 'Image Processing')
            if show_plot:
                plt.show()
            return area_values_image_procc, area_numbers_image_procc


    def ped(self, option='compare', show_plot=True):
        """
        Calculates pore elongation distribution. 0 for line and 1 for circle

        Parameter:
            option (str): 'compare', 'manual_measurement', 'image_processing'
            show_plot (bool): if 'True', plot will be shown

        Return:
            option: 'compare' -->
                elongation_values_experiment (list): elongation values obtained from manual measurement
                elongation_numbers_experiment (list): elongation numbers obtained from manual measurement
                elongation_values_image_procc (list): elongation values obtained from image processing
                elongation_numbers_image_procc (list): elongation numbers obtained from image processing

            option: 'manual_measurement' -->
                elongation_values_experiment (list): elongation values obtained from manual measurement
                elongation_numbers_experiment (list): elongation numbers obtained from manual measurement

            option: 'image_processing' -->
                elongation_values_image_procc (list): elongation values obtained from image processing
                elongation_numbers_image_procc (list): elongation numbers obtained from image processing
        """
        exp = Experiment()
        elongation_values_experiment, elongation_numbers_experiment = exp.elongation_distribution(self.image_name)
        elongation_values_image_procc, elongation_numbers_image_procc, _ = self.pore_info()[3:6]

        if option == 'compare':
            plt.plot(elongation_values_experiment, elongation_numbers_experiment, label = 'Manual Measurement')
            plt.plot(elongation_values_image_procc, elongation_numbers_image_procc, label = 'Image Processing')
            if show_plot:
                plt.show()
            return elongation_values_experiment, elongation_numbers_experiment, elongation_values_image_procc, elongation_numbers_image_procc
        elif option == 'manual_measurement':
            plt.plot(elongation_values_experiment, elongation_numbers_experiment, label = 'Manual Measurement')
            if show_plot:
                plt.show()
            return elongation_values_experiment, elongation_numbers_experiment
        elif option == 'image_processing':
            plt.plot(elongation_values_image_procc, elongation_numbers_image_procc, label = 'Image Processing')
            if show_plot:
                plt.show()
            return elongation_values_image_procc, elongation_numbers_image_procc


    def pod(self, show_plot=True):
        """
        Calculates pore orientation distribution. 0 to 180 degree.

        Parameter:
            show_plot (bool): if 'True', plot will be shown

        Return:
            orientation_values_image_procc (list): orientation values obtained from image processing
            orientation_numbers_image_procc (list): orientation numbers obtained from image processing
        """
        exp = Experiment()
        orientation_values_image_procc, orientation_numbers_image_procc, _ = self.pore_info()[6:]
        plt.plot(orientation_values_image_procc, orientation_numbers_image_procc, label = 'Image Processing')
        if show_plot:
            plt.show()
        return orientation_values_image_procc, orientation_numbers_image_procc












########################################################################################################################
########################################################################################################################
########################################################################################################################
class Processing:
    """
    This class does the batch processings.


    Attributes:
        min_diameter (int): Minimum pore diameter in pixels
        max_diameter (int): Maximum pore diameter in pixels
        min_threshold (int): Minimum threshold value
        max_threshold (int): Maximum threshold value
        bin_numbers (int): Number of bins used for distribution calculation
        listdir (list): list of adjusted sem file names
        sem_adjusted (obj): Object of 'sem_adjusted' directory
        sem_cropped (obj): Object of 'sem_cropped' directory
        sem_output (obj): Object of 'sem_output' directory
        sem_originals (obj): Object of 'sem_originals' directory
        sem_temp (obj): Object of 'sem_temp' directory
        sem_measurements (obj): Object of 'sem_measurements' directory
        sample_sem_name (str): Name of sample sem file for calibration picked from 'sem_originals' directory
        sample_sem (obj): Object of sample sem for further manipulations on that
    """



    listdir = os.listdir(parameters.sem_adjusted)
    sem_adjusted = FilesFolders(parameters.sem_adjusted)
    sem_cropped = FilesFolders(parameters.sem_cropped)
    sem_output = FilesFolders(parameters.sem_output)
    sem_originals = FilesFolders(parameters.sem_originals)
    sem_temp = FilesFolders(parameters.sem_temp)
    sem_measurements = FilesFolders(parameters.sem_measurements)
    sample_sem_name = sem_originals.random_pick()
    sample_sem = Sem(sample_sem_name)

    def __init__(self):
        """
        Constructor of Processing class

        Parameter:
            params (list): [min_diameter, max_diameter, min_threshold, max_threshold]
        """


    def batch_adjust(self):
        """
        Adjust all the sem images from "sem_original" directory to "sem_adjusted" directory
        """
        self.sem_adjusted.clean()  # clean previous files
        for path, subdirs, files in os.walk(parameters.sem_originals):
            for name in files:
                if '.' + parameters.sem_extension in name:
                    sem = os.path.join(path, name)
                    img = cv2.imread(sem, cv2.IMREAD_GRAYSCALE)
                    clashe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
                    cll = clashe.apply(img)
                    cv2.imwrite(parameters.sem_adjusted + name, cll)
        return

    def batch_crop(self):
        """
        Crop all the sem images from "sem_adjusted" directory to "sem_cropped" directory
        """
        self.sample_sem.set_scale_bar()

        rectangle = list(self.sample_sem.set_anlysis_region())
        self.sem_cropped.clean()  # clean previous files
        for name in self.listdir:
            img = cv2.imread(parameters.sem_adjusted + name)
            #  Crop image
            imCrop = img[int(rectangle[1]):int(rectangle[1]) + int(rectangle[3]),
                     int(rectangle[0]):int(rectangle[0]) + int(rectangle[2])]
            cv2.imwrite(parameters.main + 'sem_cropped/' + name, imCrop)

    def batch_process(self, batch_params):
        """
        Runs pore analysis on all adjusted-cropped images and saves the results in output directory.

        Parameter:
            batch_params (list): [min_diameter, max_diameter, min_threshold, max_threshold]

        Return:
            raw_results (DataFrame): raw pore analysis results, the following labels will add to the dataframe using
            parse_image_processing method. The raw results are also saved to 'sem_output' directory as
            'image_processing_results_raw.csv'.

            index|sem_name|area_values|area_numbers|area_ave|ecc_values|ecc_numbers|ecc_ave|angle_values|angle_numbers|angle_ave
        """
        self.batch_params = batch_params
        processed_files = []
        raw_results = []
        for file in os.listdir(parameters.sem_cropped):
            sem_image = Sem(parameters.sem_cropped + file)
            sem_image.min_diameter, sem_image.max_diameter, \
            sem_image.min_threshold, sem_image.max_threshold = self.batch_params
            raw_results.append(sem_image.pore_info())
            sem_image_name = sem_image.address.split('/')[-1]
            processed_files.append(sem_image_name)
        raw_results = pd.DataFrame(raw_results)
        raw_results.insert(loc=0, column='sem_name', value=processed_files)  # insert column at the beginning
        raw_results.to_csv(parameters.sem_output + 'image_processing_results_raw.csv')
        return raw_results

    def parse_image_processing(self):
        """
        Reads and Parses image processing results

        Return:
            results (DataFrame): index|sem_name|area_values|area_numbers|area_ave|ecc_values|ecc_numbers|ecc_ave|angle_values|angle_numbers|angle_ave
        """
        results = pd.read_csv(parameters.sem_output + 'image_processing_results_raw.csv')
        results.columns = ['index', 'sem_name', 'area_values', 'area_numbers', 'area_ave',
                           'ecc_values', 'ecc_numbers', 'ecc_ave',
                           'angle_values', 'angle_numbers', 'angle_ave']
        results = results.drop(['index'], axis=1)
        tools = Tools()
        columns_to_convert = ['area_values', 'area_numbers', 'ecc_values', 'ecc_numbers', 'angle_values',
                              'angle_numbers']
        for i in columns_to_convert:
            results[i] = tools.new_column(results[i])
        return results


    def objective_function(self, params):
        """
        The function calculates difference between experiment measurement and image processing results.

        Parameter:
            batch_params (list): [min_diameter, max_diameter, min_threshold, max_threshold]

        Return:
            differences_average_list (list): [diff_area_numbers, diff_area_values, diff_area_x, diff_ecc_values, diff_ecc_numbers, diff_ecc_x]
            contraints (list): contraints where the list items are greater and equal to zero [self.min_diameter, self.max_diameter, self.min_threshold, self.max_threshold].
        """
        self.min_diameter, self.max_diameter, self.min_threshold, self.max_threshold, = params

        Sem.min_diameter = self.min_diameter
        Sem.max_diameter = self.max_diameter
        Sem.min_threshold = self.min_threshold
        Sem.max_threshold = self.max_threshold
        Sem.bin_numbers = parameters.bin_numbers

        constrains = self.max_threshold - self.min_threshold


        if self.min_threshold >= self.max_threshold:
            print('DIVERGED!')
            return [2,2,2,2,2,2], [self.max_threshold-self.min_threshold]
        else:
            try:
                #   Read data
                experiment = Experiment()
                experiment_area, experiment_ecc = experiment.parse_experiment()
                sem_names_exp = experiment_area['sem_name'].values
                sem_names_exp = [i.strip('.csv') for i in sem_names_exp]  # remove the extension to be comparable
                image_processing_result = self.batch_process(params)
                image_processing_result.columns = ['sem_name', 'area_values', 'area_numbers', 'area_ave',
                                                   'ecc_values', 'ecc_numbers', 'ecc_ave',
                                                   'angle_values', 'angle_numbers', 'angle_ave']
                sem_name_imageprocessing = image_processing_result['sem_name'].values
                #   remove the extension to be comparable
                sem_name_imageprocessing = [i.strip('.tif') for i in
                                            sem_name_imageprocessing]
                #   find common files exist in experiment and image processing files for validation
                tools = Tools()
                indices = tools.common_indices(sem_names_exp, sem_name_imageprocessing)

                def differences_average():
                    objective_function = []
                    for [i, j] in indices:
                        #   Read experiment valiables of common files
                        ##################################################
                        sem_name_exp = experiment_area['sem_name'].iloc[i]
                        area_values_exp = experiment_area['Area'].iloc[i]
                        area_numbers_exp = experiment_area['Area_number'].iloc[i]
                        ecc_values_exp = experiment_ecc['Circ.'].iloc[i]
                        ecc_numbers_exp = experiment_ecc['Circ._number'].iloc[i]
                        #   Read image processing variables of common files
                        #######################################################################
                        sem_name_imageprocessing = image_processing_result['sem_name'][j]
                        area_values_imageprocessing = image_processing_result['area_values'][j]
                        area_numbers_imageprocessing = image_processing_result['area_numbers'][j]
                        ecc_values_imageprocessing = image_processing_result['ecc_values'][j]
                        ecc_numbers_imageprocessing = image_processing_result['ecc_numbers'][j]
                        angle_values_imageprocessing = image_processing_result['angle_values'][j]
                        angle_numbers_imageprocessing = image_processing_result['angle_numbers'][j]
                        #   x direction comparison
                        diff_area_values = tools.normal_obj(area_values_exp[-1], area_values_imageprocessing[-1])
                        diff_area_numbers = tools.normal_obj(max(area_numbers_exp), max(area_numbers_imageprocessing))
                        #   y direction comparison
                        diff_ecc_values = tools.normal_obj(ecc_values_exp[-1], ecc_values_imageprocessing[-1])
                        diff_ecc_numbers = tools.normal_obj(max(ecc_numbers_exp), max(ecc_numbers_imageprocessing))
                        #   Pick location comparison
                        index_max_area_experiment = np.argmax(area_numbers_exp)
                        index_max_area_imageprocessing = np.argmax(area_numbers_imageprocessing)
                        diff_area_x = tools.normal_obj(area_values_exp[index_max_area_experiment],
                                                 area_values_imageprocessing[index_max_area_imageprocessing])
                        index_max_ecc_experiment = np.argmax(ecc_numbers_exp)
                        index_max_ecc_imageprocessing = np.argmax(ecc_numbers_imageprocessing)
                        diff_ecc_x = tools.normal_obj(ecc_values_exp[index_max_ecc_experiment],
                                                ecc_values_imageprocessing[index_max_ecc_imageprocessing])
                        ######################################################################################################################
                        differences = [diff_area_numbers, diff_area_values, diff_area_x, diff_ecc_values, diff_ecc_numbers,
                                       diff_ecc_x]
                        objective_function.append(differences)
                    objective_function = np.array(objective_function)
                    return np.average(objective_function,
                                      axis=0)  # calculates average of n list by calculating the avergae of items in order


                loss = np.average(differences_average())
                if 'ga.log' not in os.listdir(parameters.sem_output):
                    log_file = open(parameters.sem_output + 'ga.log', 'a+')
                if loss <= parameters.error:
                    log_file = open(parameters.sem_output + 'ga.log', 'a+')
                    log_file.write(str(params) + '\t' + str(loss) + '\n')
                    log_file.close()
                differences_average_list = list(differences_average())
                if loss < parameters.error:
                    print('loss: ', loss, ' CONVERGED!')
                else:
                    print('loss: ', loss)
                return differences_average_list, constrains
            except:
                print('DIVERGED!')
                return [2, 2, 2, 2, 2, 2], constrains


########################################################################################################################
########################################################################################################################
########################################################################################################################
class PostProcessing:

    def find_best_params(self):
        """
        Finds parameter values assiciated with minimum loss value.

        Return:
            params (list): List of float (parameter values associated with minimum loss function)
        """
        file = pd.read_csv(parameters.sem_output + 'ga.log', skiprows=1, sep='\t')
        file.columns = ['params', 'loss function']
        index = file['loss function'].idxmin()
        param = file['params'].iloc[index]
        tools = Tools()
        params = tools.str_to_float_bracket(param)
        return param

    def plot_best_fit(self, i, j):
        """
        This function plots manual measurement graph vs image processing graph for minimum loss function.

        Parameters:
            i (int):   index of manual measurement file in the manual measurement files list
            j (int):   index of image processing file in the image processing files list

        Return:
            Plots image processing vs manual measurements
        """
        #   Read data
        experiment = Experiment()
        experiment_area, experiment_ecc = experiment.parse_experiment()
        proc = Processing()
        image_processing_result = proc.parse_image_processing()
        image_processing_result.columns = ['sem_name', 'area_values', 'area_numbers', 'area_ave',
                                           'ecc_values', 'ecc_numbers', 'ecc_ave',
                                           'angle_values', 'angle_numbers', 'angle_ave']
        sem_name_exp = experiment_area['sem_name'].iloc[i]
        area_values_exp = experiment_area['Area'].iloc[i]
        area_numbers_exp = experiment_area['Area_number'].iloc[i]
        ecc_values_exp = experiment_ecc['Circ.'].iloc[i]
        ecc_numbers_exp = experiment_ecc['Circ._number'].iloc[i]
        sem_name_imageprocessing = image_processing_result['sem_name'][j]
        area_values_imageprocessing = image_processing_result['area_values'][j]
        area_numbers_imageprocessing = image_processing_result['area_numbers'][j]
        ecc_values_imageprocessing = image_processing_result['ecc_values'][j]
        ecc_numbers_imageprocessing = image_processing_result['ecc_numbers'][j]
        angle_values_imageprocessing = image_processing_result['angle_values'][j]
        angle_numbers_imageprocessing = image_processing_result['angle_numbers'][j]

        #   Curve fittings
        def fit_function(x, a, b, c, d):
            """
            This function is general form of curve fitted functions over experimental and image processing results. Parameters
            of this function will be compared for experiment and image processing at the end.

            Parameters:
                x (float): variable
                a, b, c, d, ... (float): constants of fitting function

            Return:
                f (float): Values of the fitted function
            """
            f = a * x ** 4 + b * x ** 3 + c * x ** 2 + d * x
            return f

        param_experiment, _ = curve_fit(fit_function, area_values_exp, area_numbers_exp, maxfev=10000000, method='trf')
        param_image_processing, _ = curve_fit(fit_function, area_values_imageprocessing, area_numbers_imageprocessing,
                                              maxfev=10000000, method='trf')
        var_exp_smooth = np.linspace(0.0001, area_values_exp[-1], 300)
        num_exp_smooth = fit_function(var_exp_smooth, *param_experiment)
        var_proc_smooth = np.linspace(0.0001, area_values_imageprocessing[-1], 300)
        num_proc_smooth = fit_function(var_proc_smooth, *param_image_processing)
        plt.plot(var_exp_smooth, num_exp_smooth, label='Manual Measurements')
        plt.plot(var_proc_smooth, num_proc_smooth, label='Image Processing')
        plt.xlabel('Variable Sizes')
        plt.ylabel('Variable Counts')
        plt.title(sem_name_exp + ' \nvs\n ' + sem_name_imageprocessing)
        plt.legend()
        plt.show()