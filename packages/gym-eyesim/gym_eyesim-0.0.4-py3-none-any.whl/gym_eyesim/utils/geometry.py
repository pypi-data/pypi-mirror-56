import math
import numpy as np


def dist_to_line(p1, p2, p3):
    return abs(np.cross(p2 - p1, p3 - p1)) / np.linalg.norm(p2 - p1)


def side_of_line(p1, p2, p3):
    """Check on which side of a line a point is.

    Args:
        p1 (array): First point of the line.
        p2 (array): Second point of the line.
        p3 (array): Point to check.

    Returns:
        A value larger than 0 if p3 is left of p1 and p2.
    """

    return np.cross(p2 - p1, p3 - p1)


def angle_between_vectors(v1, v2):
    x1, y1 = v1
    x2, y2 = v2
    inner_product = x1 * x2 + y1 * y2
    len1 = math.hypot(x1, y1)
    len2 = math.hypot(x2, y2)
    return math.acos(inner_product / (len1 * len2))
