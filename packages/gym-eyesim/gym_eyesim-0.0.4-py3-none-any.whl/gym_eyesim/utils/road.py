import cv2
import numpy as np

from pathlib import Path
from sklearn.cluster import DBSCAN

from .geometry import dist_to_line, side_of_line, angle_between_vectors
from .coordinates import img_to_world


def binarize_img(img, thresh=127):
    """Create binary image from grayscale image.

    Args:
        img (array): grayscale image.
        thresh (int, optional): threshold for binarization.

    Returns:
        A binary image.
    """

    binary_img = np.zeros_like(img)
    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            value = img[y, x]
            if value > thresh:
                binary_img[y, x] = 255
    return binary_img


class RoadMark():
    def __init__(self, points):
        """Road mark

        Can be constructed from single point or list of points.

        Args:
            points (list or array): Point(s) belonging to this road mark
        """

        if points.ndim == 1:
            self.size = 1
            self.center = points
        else:
            self.size = len(points)
            self.center = np.mean(np.array(points), axis=0)

    def dist(self, other):
        """Distance to point or other road mark.

        Args:
            other (array or RoadMark): point or road mark.

        Returns:
            The distance between this road mark and the point or other road
            mark.
        """

        if isinstance(other, RoadMark):
            other = other.center
        return np.sqrt((self.center[0] - other[0])**2 +
                       (self.center[1] - other[1])**2)


def detect_road_marks(img):
    """Detect road marks from binary image.

    Use DBSCAN to cluster points belonging to road marks.

    Args:
        img (array): binary image of road mark/non-road mark points.

    Returns:
        A list of RoadMark objects.
    """

    # Find points belonding to road marks
    road_mark_points = []
    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            value = img[y, x]
            if value > 0:
                road_mark_points.append([y, x])

    # Convert to numpy array
    road_mark_points = np.array(road_mark_points)

    # Cluster points belonging to road marks
    dbscan = DBSCAN(eps=4).fit(road_mark_points)
    labels = dbscan.labels_
    unique_labels = set(labels)
    core_samples_mask = np.zeros_like(labels, dtype=bool)
    core_samples_mask[dbscan.core_sample_indices_] = True

    # Accumulate road marks
    road_marks = []
    for label in unique_labels:
        if label == -1:
            continue
        class_member_mask = (label == labels)
        points = road_mark_points[class_member_mask & core_samples_mask]
        road_marks.append(RoadMark(points))

    return road_marks


def filter_road_marks(road_marks):
    """Filter road marks by the number of points they contain to find road
    marks that form the center line.

    Args:
        road_marks (list): list of road marks.

    Returns:
        A list of filtered road marks.
    """

    filtered_road_marks = []
    for road_mark in road_marks:
        if road_mark.size > 70 or road_mark.size < 30:
            continue

        filtered_road_marks.append(road_mark)

    return filtered_road_marks


def sort_road_marks(road_marks):
    """Sort road marks

    Starting at the first road mark find the closest one to it. If no road mark
    is found in a small region check a larger region with angle constraint.

    Args:
        road_marks (list): list of road marks forming the center line.

    Returns:
        A list of sorted road marks.
    """

    sorted_road_marks = [road_marks[0]]
    unused_road_marks = road_marks[1:]
    done = False

    while not done:
        index = None
        shortest_dist = 50
        for i, road_mark in enumerate(unused_road_marks):
            dist = sorted_road_marks[-1].dist(road_mark)
            if dist < shortest_dist:
                shortest_dist = dist
                index = i

        if index is None:
            shortest_dist = 150
            max_angle = 25 / 180 * np.pi
            for i, road_mark in enumerate(unused_road_marks):
                dist = sorted_road_marks[-1].dist(road_mark)
                v1 = sorted_road_marks[-1].center - sorted_road_marks[-2].center
                v2 = road_mark.center - sorted_road_marks[-1].center
                angle = abs(angle_between_vectors(v1, v2))
                if angle < max_angle:
                    if dist < shortest_dist:
                        shortest_dist = dist
                        index = i

        if index is not None:
            sorted_road_marks.append(unused_road_marks[index])
            del unused_road_marks[index]
            # print(
            #     f"{sorted_road_marks[-2].center} -> {sorted_road_marks[-1].center}, {shortest_dist}"
            # )
        else:
            print(f"Remaining road marks: {len(unused_road_marks)}")
            break

        done = len(unused_road_marks) == 0

    return sorted_road_marks


def transform_road_marks(road_marks):
    for road_mark in road_marks:
        road_mark.center = img_to_world(road_mark.center)

    return road_marks


def fill_gaps(road_marks, max_gap=300):
    """Fill gaps

    For each pair of road marks insert additional road marks in between if the
    distance between them is too large.

    Args:
        road_marks (list): list of road marks forming the center line.

    Returns:
        List of complete road marks.
    """

    complete_road_marks = []
    dist_to_next = np.linalg.norm(road_marks[0].center - road_marks[-1].center)

    # Fill gap
    n_missing = int(dist_to_next // max_gap)
    for n in range(n_missing):
        complete_road_marks.append(
            RoadMark(road_marks[-1].center +
                     (road_marks[0].center - road_marks[-1].center) * (n + 1) /
                     (n_missing + 1)))

    for i in range(len(road_marks) - 1):
        dist_to_next = np.linalg.norm(road_marks[i + 1].center -
                                      road_marks[i].center)
        n_missing = int(dist_to_next // max_gap)
        complete_road_marks.append(road_marks[i])
        for n in range(n_missing):
            # print(
            #     road_marks[i].center, road_marks[i + 1].center,
            #     road_marks[i].center +
            #     (road_marks[i + 1].center - road_marks[i].center) * (n + 1) /
            #     (n_missing + 1))
            complete_road_marks.append(
                RoadMark(road_marks[i].center +
                         (road_marks[i + 1].center - road_marks[i].center) *
                         (n + 1) / (n_missing + 1)))

    complete_road_marks.append(road_marks[-1])
    return complete_road_marks


def determine_road_width(img, road_marks):
    """Determine road width.

    Args:
        img (array): binary image of road mark/non-road mark points
        road_marks (list): list of road marks forming the center line.

    Returns:
        The average width of the road in pixel coordinates.
    """
    def _determine_road_witdh(p1, p2):
        """Nested function for road width.

        Calculates road width at the location of a pair of road marks by going
        orthogonal to the direction until encountering a non-zero pixel.

        Args:
            p1 (array): center of first road mark.
            p2 (array): center of second road mark.

        Returns:
            The approximated road width at this point of the road.
        """

        average = (p1 + p2) / 2
        direction = (p2 - p1) / np.linalg.norm(p2 - p1)
        orthogonal = np.array([-direction[1], direction[0]])
        left_found = False
        right_found = False
        i = 1
        left_pixel = None
        right_pixel = None
        done = False
        while not done:
            if not left_found:
                left_pixel_pos = (np.rint(average +
                                          orthogonal * i)).astype(int)
                left_pixel = img[left_pixel_pos[0], left_pixel_pos[1]]
                if left_pixel > 0:
                    left_found = True

            if not right_found:
                right_pixel_pos = (np.rint(average -
                                           orthogonal * i)).astype(int)
                right_pixel = img[right_pixel_pos[0], right_pixel_pos[1]]
                if right_pixel > 0:
                    right_found = True

            done = left_found and right_found
            i += 1

        road_width = np.linalg.norm(left_pixel_pos - right_pixel_pos)
        return road_width

    road_widths = [
        _determine_road_witdh(
            road_marks[-1].center,
            road_marks[0].center,
        )
    ]

    for i in range(len(road_marks) - 1):
        road_widths.append(
            _determine_road_witdh(
                road_marks[i].center,
                road_marks[i + 1].center,
            ))

    return sum(road_widths) / len(road_widths)


class Road():
    def __init__(self, road_marks, width):
        self._road_marks = road_marks
        self._width = width

    @property
    def width(self):
        return self._width

    def dist(self, point):
        """The distance of a point to the closest pair of neightboring road marks.

        Args:
            point (array): point in world coordinates.

        Returns:
            The distance of a point to the closest pair of neightboring road marks.
        """

        # Find closest road mark
        index, _, _ = self.closest(point)

        # Compute distance to previous and next road mark
        prev_index = (index - 1) % len(self._road_marks)
        next_index = (index + 1) % len(self._road_marks)
        shortest_dist = min(
            dist_to_line(
                self._road_marks[prev_index].center,
                self._road_marks[index].center,
                point,
            ),
            dist_to_line(
                self._road_marks[index].center,
                self._road_marks[next_index].center,
                point,
            ),
        )

        return shortest_dist

    def angle(self, point):
        # Find closest road mark
        index, _, _ = self.closest(point)

        # Compute distance to previous and next road mark
        prev_index = (index - 1) % len(self._road_marks)
        next_index = (index + 1) % len(self._road_marks)

        direction = self._road_marks[next_index].center - self._road_marks[
            prev_index].center
        return np.arctan2(direction[1], direction[0])

    def side(self, point):
        """Determine on which side of the road a point lies.

        Args:
            point (array): Point to check.

        Returns:
             A value larger than 0 if p3 is left of p1 and p2.
        """

        first_index, second_index = self.closest_pair(point)

        # Determine side of line
        return side_of_line(
            self._road_marks[first_index].center,
            self._road_marks[second_index].center,
            point,
        )

    def closest(self, point):
        """Find closest road mark to given point.

        Args:
            point (array): Point to check.

        Returns:
            Index, coordinate and distance of closest road mark.
        """

        shortest_dist = None
        index = None
        for i, road_mark in enumerate(self._road_marks):
            dist = road_mark.dist(point)
            if index is None:
                shortest_dist = dist
                index = i
                continue

            if dist < shortest_dist:
                shortest_dist = dist
                index = i

        return index, self._road_marks[i], shortest_dist

    def closest_pair(self, point):
        # Find closest road mark
        first_index, _, _ = self.closest(point)

        # Find closest neighbor
        prev_index = (first_index - 1) % len(self._road_marks)
        dist_to_prev = self._road_marks[prev_index].dist(point)
        next_index = (first_index + 1) % len(self._road_marks)
        dist_to_next = self._road_marks[next_index].dist(point)
        second_index = prev_index if dist_to_prev < dist_to_next else next_index

        # Swap indices if second is smaller
        if second_index % len(self._road_marks) < first_index % len(
                self._road_marks):
            first_index, second_index = second_index, first_index

        return first_index, second_index

    def random_pose(self):
        """Generate a random pose on the road.

        Returns:
            Tuple of position array and orientation.
        """

        first_index = np.random.randint(len(self._road_marks))
        second_index = (first_index + 1) % len(self._road_marks)
        first_position = self._road_marks[first_index].center
        second_position = self._road_marks[second_index].center
        scale = np.random.rand(1)
        direction = second_position - first_position
        position = first_position + scale * direction
        orientation = np.arctan2(direction[1], direction[0])
        return position, orientation


def detect_road(path_to_sim):
    path_to_floor_texture = Path(
        path_to_sim).parents[0] / "worlds" / "carolo.png"
    img = cv2.imread(str(path_to_floor_texture))

    # Convert to grayscale image
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Rotate by 180 degree
    center = tuple(value / 2 for value in gray_img.shape)
    angle = 180
    scale = 1
    rot = cv2.getRotationMatrix2D(center, angle, scale)
    rotated_img = cv2.warpAffine(gray_img, rot, gray_img.shape)

    # Create binary image (road mark/non-road mark)
    binary_img = binarize_img(rotated_img)

    # Detect road marks
    road_marks = detect_road_marks(binary_img)

    # Filter road marks
    filtered_road_marks = filter_road_marks(road_marks)

    # Sort road marks
    sorted_road_marks = sort_road_marks(filtered_road_marks)

    # Determine road width
    road_width = determine_road_width(binary_img, sorted_road_marks)
    road_width = img_to_world(road_width)

    # Transform to from image to world coordinates
    transformed_road_marks = transform_road_marks(sorted_road_marks)

    complete_road_marks = fill_gaps(transformed_road_marks)

    return Road(complete_road_marks, road_width)
