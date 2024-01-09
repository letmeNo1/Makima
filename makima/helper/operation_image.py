from apollo_makima.helper.find_ui_element import find_element_by_image
from apollo_makima.openCV.image_object import ImageObject


class Init_App_Ref_For_Image:
    def __call__(self, ath, distance=0.7, algorithms_name="SIFT") -> ImageObject:
        return find_element_by_image(ath, distance, algorithms_name)
