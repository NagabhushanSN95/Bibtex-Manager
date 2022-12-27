# Shree KRISHNAya Namaha
# Commonly used utility functions
# Author: Nagabhushan S N
# Last Modified: 27/12/22


def get_list_element(list_obj, index, default=None):
    if len(list_obj) > index:
        return list_obj[index]
    else:
        return default
