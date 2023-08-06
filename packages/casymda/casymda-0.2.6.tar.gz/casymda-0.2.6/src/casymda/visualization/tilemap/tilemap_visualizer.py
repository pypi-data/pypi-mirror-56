"""
2D visualization of positions on a ScaledCanvas
"""
# TODO: could become the super class for the process visualizer? -> since it does nothing but plain updates of entity positions
# TODO: declare interface
# self.tilemap_visualizer.animate(entity, current_position, current_time)
# self.tilemap_visualizer.destroy(entity)
import datetime
from typing import List

from casymda.visualization.canvas.scaled_canvas import ScaledCanvas


class TilemapVisualizer:
    """visualizes entity positions at a given canvas"""

    def __init__(
        self,
        canvas: ScaledCanvas,
        background_image_path: str = "",
        default_entity_icon_path: str = "",
    ):

        self.canvas = canvas
        self.background_image_path = background_image_path
        self.default_entity_icon_path = default_entity_icon_path

        self.background_image_file = self.canvas.load_image_file(
            self.background_image_path
        )

        self.background_image = self.canvas.create_image(
            0, 0, self.background_image_file, anchor="nw"
        )

        time_text = "Time:  " + str(0)
        self.time_label = self.canvas.create_text(
            self.canvas.get_width() - 5,
            self.canvas.get_height() - 5,
            font="Helvetica 10",
            fill="black",
            anchor="se",
            text=time_text,
        )

        self.entity_animations: List[EntityAnimation] = []

    def animate(self, entity, x: float, y: float, current_time: float):
        """ change entity position """

        # find / create entity animation
        entity_anim = next(
            (x for x in self.entity_animations if x.entity is entity), None
        )  # existing
        if entity_anim is None:
            entity_anim = self.create_entity_animation(entity, (x, y))  # new
        entity_icon = entity_anim.canvas_image

        # set position
        self.canvas.set_coords(entity_icon, (x, y))
        entity_anim.x_y = (x, y)
        self.updatetime_label(current_time)

    def updatetime_label(self, now):
        """updates the own time_label with the given time"""
        text = "Time:  " + str(datetime.timedelta(seconds=int(now)))
        self.canvas.set_text_value(self.time_label, text=text)

    def create_entity_animation(self, entity, x_y):
        """creates entity animation"""

        # possibility to look for entity file path if defined
        if entity.process_animation_icon_path is not None:
            file_path = entity.process_animation_icon_path
        else:
            file_path = self.default_entity_icon_path
        image_file = self.canvas.load_image_file(file_path)
        icon = self.canvas.create_image(*x_y, image_file=image_file, anchor="c")

        entity_animation = EntityAnimation(entity, icon, image_file, x_y)
        self.entity_animations.append(entity_animation)

        return entity_animation

    def destroy(self, entity):
        """destroy entity animation"""
        entity_animation = next(
            (x for x in self.entity_animations if x.entity is entity), None
        )  # existing
        if entity_animation is not None:
            self.canvas.delete(entity_animation.canvas_image)
            self.entity_animations.remove(entity_animation)
            entity_animation = None


class EntityAnimation:
    """class to hold animation related info of an entity"""

    def __init__(self, entity, canvas_image, image_file, x_y):
        self.entity = entity
        self.canvas_image = canvas_image
        self.image_file = image_file
        self.x_y = x_y
