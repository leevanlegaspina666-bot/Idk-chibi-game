import os
import random

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.resources import resource_add_path
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line


# ============================================================
# VERSION
# ============================================================

__version__ = "1.0.0"


# ============================================================
# APK-SAFE ASSET PATH
# ============================================================

# This makes the game work both:
#
# 1. In Pydroid 3
# 2. Inside the finished Android APK
#
# Your assets folder must be beside main.py:
#
# ChibiSharkPet/
# ├── main.py
# └── assets/
#

APP_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

ASSETS = os.path.join(
    APP_DIR,
    "assets"
)

resource_add_path(ASSETS)


# ============================================================
# ASSETS
# ============================================================

SPRITE_SIZE = 180

LANDSCAPE_SPRITE_SIZE = 120


BACKGROUND_FILE = os.path.join(
    ASSETS,
    "town_map.png"
)


# ============================================================
# CHARACTER SETTINGS
# ============================================================

GURA_SPEED = 80.0

AMELIA_SPEED = 80.0

PLAYER_SPEED = 220.0

JUMP_SPEED = 520.0

GRAVITY = 900.0

WALK_TIME = 0.12

FALL_TIME = 0.12

LAND_TIME = 0.18

DRAG_THRESHOLD = 10


# ============================================================
# ROAD / GROUND
# ============================================================

GROUND_Y_RATIO = 0.38

DRAG_MIN_Y_RATIO = 0.38

DRAG_MAX_Y_RATIO = 0.70


# ============================================================
# CAMERA
# ============================================================

CAMERA_LEFT_MARGIN = 0.35

CAMERA_RIGHT_MARGIN = 0.65


# ============================================================
# REACTIONS
# ============================================================

REACTION_TIME = 5.0

RANDOM_IDLE_DURATION = 5.0

INTERACTION_DISTANCE = 130

INTERACTION_COOLDOWN = 20.0

CHARACTER_INTERACTION_CHANCE = 0.05

INTERACTION_CHECK_MIN = 0.5

INTERACTION_CHECK_MAX = 1.5

GURA_INTERACTION_TIME = 5.0


# ============================================================
# RANDOM MOVEMENT
# ============================================================

RANDOM_TURN_CHECK_MIN = 0.5

RANDOM_TURN_CHECK_MAX = 1.5

RANDOM_TURN_CHANCE = 0.03

RANDOM_SPEED_MIN = 55.0

RANDOM_SPEED_MAX = 100.0

RANDOM_IDLE_MIN = 6.0

RANDOM_IDLE_MAX = 12.0

RANDOM_IDLE_CHANCE = 0.20


# ============================================================
# FIGHT SETTINGS
# ============================================================

FIGHT_DISTANCE = 150.0

FIGHT_APPROACH_SPEED = 110.0

FIGHT_FRAME_TIME = 0.10

FIGHT_ATTACK_COOLDOWN = 1.8

FIGHT_DAMAGE = 10


# ============================================================
# LOAD NORMAL ANIMATION FRAMES
# ============================================================

def load_frames(prefix, amount):

    frames = []

    for i in range(1, amount + 1):

        filename = "{}_{:02d}.png".format(
            prefix,
            i
        )

        full_path = os.path.join(
            ASSETS,
            filename
        )

        if os.path.isfile(full_path):

            frames.append(full_path)

            print(
                "FOUND:",
                filename
            )

        else:

            print(
                "MISSING:",
                filename
            )

    print(
        prefix,
        "=>",
        len(frames),
        "/",
        amount
    )

    return frames


# ============================================================
# WATSON REACTION FRAMES
# ============================================================

def load_watson_reactions():

    reaction_names = [

        "happy",

        "surprised",

        "angry",

        "sad",

        "confused",

        "sleepy",

        "panicked",

        "dizzy",

        "embarrassed",

        "smug"

    ]

    frames = []

    for i, reaction_name in enumerate(
        reaction_names,
        start=1
    ):

        filename = (
            "watson_reaction_{:02d}_{}.png"
            .format(
                i,
                reaction_name
            )
        )

        full_path = os.path.join(
            ASSETS,
            filename
        )

        if os.path.isfile(full_path):

            frames.append(full_path)

            print(
                "FOUND WATSON REACTION:",
                filename
            )

        else:

            print(
                "MISSING WATSON REACTION:",
                filename
            )

    print(
        "Watson reactions =>",
        len(frames),
        "/ 10"
    )

    return frames


# ============================================================
# GURA NORMAL ASSETS
# ============================================================

GURA_LEFT = load_frames(
    "walk_left",
    7
)

GURA_RIGHT = load_frames(
    "walk_right",
    7
)

GURA_FALLING = load_frames(
    "falling",
    12
)

GURA_IDLE = load_frames(
    "front_idle",
    8
)


# ============================================================
# GURA FIGHTING ASSETS
# ============================================================

GURA_FIGHT_FRAMES = []

for i in range(1, 10):

    filename = (
        "gura_row02_frame{:02d}.png"
        .format(i)
    )

    full_path = os.path.join(
        ASSETS,
        filename
    )

    if os.path.isfile(full_path):

        GURA_FIGHT_FRAMES.append(
            full_path
        )

        print(
            "FOUND GURA FIGHT:",
            filename
        )

    else:

        print(
            "MISSING GURA FIGHT:",
            filename
        )


print(
    "Gura fight frames =>",
    len(GURA_FIGHT_FRAMES),
    "/ 9"
)


# Frame 06 = index 5
# Frame 09 = index 8

GURA_TRIDENT_START = 5

GURA_TRIDENT_END = 8


# ============================================================
# WATSON / AMELIA ASSETS
# ============================================================

AMELIA_LEFT = load_frames(
    "amelia_walk_left",
    7
)

AMELIA_RIGHT = load_frames(
    "amelia_walk_right",
    7
)

AMELIA_FALLING = load_frames(
    "amelia_falling",
    12
)

WATSON_REACTIONS = load_watson_reactions()


# ============================================================
# VIRTUAL JOYSTICK
# ============================================================

class VirtualJoystick(Widget):

    def __init__(
        self,
        on_move=None,
        **kwargs
    ):

        super().__init__(**kwargs)

        self.on_move_callback = on_move

        self.active_touch = None

        self.center_x = 0.0

        self.center_y = 0.0

        self.knob_radius = 30

        self.max_distance = 48

        with self.canvas:

            Color(
                0.15,
                0.15,
                0.15,
                0.65
            )

            self.base = Ellipse(
                pos=self.pos,
                size=self.size
            )

            Color(
                0.75,
                0.75,
                0.75,
                0.85
            )

            self.knob = Ellipse(
                size=(
                    self.knob_radius * 2,
                    self.knob_radius * 2
                )
            )

            Color(
                1,
                1,
                1,
                0.5
            )

            self.outline = Line(
                circle=(0, 0, 1),
                width=2
            )

        self.bind(
            pos=self._redraw,
            size=self._redraw
        )

        self._redraw()


    def _redraw(self, *args):

        self.center_x = (
            self.x
            + self.width / 2
        )

        self.center_y = (
            self.y
            + self.height / 2
        )

        self.base.pos = self.pos

        self.base.size = self.size

        self.knob.pos = (
            self.center_x
            - self.knob_radius,

            self.center_y
            - self.knob_radius
        )

        self.outline.circle = (
            self.center_x,

            self.center_y,

            min(
                self.width,
                self.height
            ) / 2 - 3
        )


    def _set_knob(self, dx):

        dx = max(
            -self.max_distance,

            min(
                self.max_distance,
                dx
            )
        )

        self.knob.pos = (
            self.center_x
            + dx
            - self.knob_radius,

            self.center_y
            - self.knob_radius
        )

        if abs(dx) < 10:

            direction = 0

        elif dx < 0:

            direction = -1

        else:

            direction = 1

        if self.on_move_callback:

            self.on_move_callback(
                direction
            )


    def on_touch_down(self, touch):

        if not self.collide_point(
            touch.x,
            touch.y
        ):

            return super().on_touch_down(
                touch
            )

        self.active_touch = touch

        touch.grab(self)

        self.on_touch_move(touch)

        return True


    def on_touch_move(self, touch):

        if touch.grab_current is not self:

            return super().on_touch_move(
                touch
            )

        dx = (
            touch.x
            - self.center_x
        )

        dy = (
            touch.y
            - self.center_y
        )

        distance = (
            dx * dx
            + dy * dy
        ) ** 0.5

        if (
            distance > self.max_distance
            and distance > 0
        ):

            dx = (
                dx
                / distance
                * self.max_distance
            )

        self._set_knob(dx)

        return True


    def on_touch_up(self, touch):

        if touch.grab_current is not self:

            return super().on_touch_up(
                touch
            )

        touch.ungrab(self)

        self.active_touch = None

        self._set_knob(0)

        return True


# ============================================================
# CHIBI
# ============================================================

class Chibi(Image):

    def __init__(
        self,
        world,
        name,
        left_frames,
        right_frames,
        falling_frames,
        idle_frames=None,
        reaction_frames=None,
        world_x=0,
        speed=80,
        **kwargs
    ):

        super().__init__(**kwargs)

        self.world = world

        self.name = name

        self.left_frames = left_frames

        self.right_frames = right_frames

        self.falling_frames = falling_frames

        self.idle_frames = (
            idle_frames or []
        )

        self.reaction_frames = (
            reaction_frames or []
        )

        self.size_hint = (
            None,
            None
        )

        sprite_size = (
            self.world.get_sprite_size()
        )

        self.size = (
            sprite_size,
            sprite_size
        )

        self.keep_ratio = True

        self.allow_stretch = True


        # ====================================================
        # WORLD POSITION
        # ====================================================

        self.world_x = float(
            world_x
        )

        self.y = (
            world.ground_y
        )


        # ====================================================
        # MOVEMENT
        # ====================================================

        self.base_speed = speed

        self.manual_controlled = False

        self.velocity_x = 0.0

        self.velocity_y = 0.0

        self.jumping = False


        # ====================================================
        # DIRECTION
        # ====================================================

        self.direction = 1

        self.walk_frames = (
            self.right_frames
        )


        # ====================================================
        # STATE
        # ====================================================

        self.state = "walking"

        self.frame = 0

        self.timer = 0.0


        # ====================================================
        # RANDOM MOVEMENT
        # ====================================================

        self.speed = 0.0

        self.random_turn_timer = (
            random.uniform(
                RANDOM_TURN_CHECK_MIN,
                RANDOM_TURN_CHECK_MAX
            )
        )

        self.random_idle_timer = (
            random.uniform(
                RANDOM_IDLE_MIN,
                RANDOM_IDLE_MAX
            )
        )


        # ====================================================
        # DRAGGING
        # ====================================================

        self.dragging = False

        self.touch_start_x = 0

        self.touch_start_y = 0

        self.drag_offset_x = 0

        self.drag_offset_y = 0


        # ====================================================
        # REACTION
        # ====================================================

        self.reaction_index = -1

        self.reaction_timer = 0.0


        # ====================================================
        # FIGHTING
        # ====================================================

        self.fighting = False

        self.fight_target = None

        self.fight_frame = 0

        self.fight_timer = 0.0

        self.fight_cooldown = 0.0

        self.trident_formed = False

        self.fight_hit_done = False


        self.set_walk_frame(0)


    # ========================================================
    # RANDOM MOVEMENT RESET
    # ========================================================

    def reset_random_movement(self):

        self.random_turn_timer = random.uniform(
            RANDOM_TURN_CHECK_MIN,
            RANDOM_TURN_CHECK_MAX
        )

        self.random_idle_timer = random.uniform(
            RANDOM_IDLE_MIN,
            RANDOM_IDLE_MAX
        )

        self.speed = random.uniform(
            RANDOM_SPEED_MIN,
            RANDOM_SPEED_MAX
        )


    # ========================================================
    # DIRECTION
    # ========================================================

    def set_direction(self, direction):

        if direction >= 0:

            self.direction = 1

            self.walk_frames = (
                self.right_frames
            )

        else:

            self.direction = -1

            self.walk_frames = (
                self.left_frames
            )

        self.frame = 0

        self.timer = 0.0

        self.set_walk_frame(0)


    # ========================================================
    # WALK FRAME
    # ========================================================

    def set_walk_frame(self, frame):

        if not self.walk_frames:

            return

        frame %= len(
            self.walk_frames
        )

        self.frame = frame

        self.source = (
            self.walk_frames[frame]
        )

        self.reload()


    # ========================================================
    # FALL FRAME
    # ========================================================

    def set_fall_frame(self, frame):

        if not self.falling_frames:

            return

        frame = max(
            0,

            min(
                frame,
                len(
                    self.falling_frames
                ) - 1
            )
        )

        self.frame = frame

        self.source = (
            self.falling_frames[frame]
        )

        self.reload()


    # ========================================================
    # FIGHT FRAME
    # ========================================================

    def set_fight_frame(self, frame):

        if not GURA_FIGHT_FRAMES:

            return

        frame = max(
            0,

            min(
                frame,
                len(
                    GURA_FIGHT_FRAMES
                ) - 1
            )
        )

        self.fight_frame = frame

        self.source = (
            GURA_FIGHT_FRAMES[frame]
        )

        self.reload()


    # ========================================================
    # RANDOM MODE
    # ========================================================

    def set_random_mode(self, enabled):

        self.manual_controlled = False

        self.velocity_x = 0.0

        if enabled:

            self.state = "walking"

            self.jumping = False

            self.reset_random_movement()

            self.timer = 0.0

            self.set_walk_frame(0)

        else:

            self.speed = 0.0


    # ========================================================
    # PLAYER INPUT
    # ========================================================

    def set_horizontal_input(self, direction):

        if self.world.fight_mode:

            return

        self.manual_controlled = True

        self.velocity_x = (
            direction
            * PLAYER_SPEED
        )

        if direction != 0:

            self.set_direction(
                direction
            )

        if (
            self.state in (
                "idle",
                "reaction"
            )
            and not self.jumping
        ):

            self.state = "walking"

            self.timer = 0.0


    # ========================================================
    # JUMP
    # ========================================================

    def jump(self):

        if self.world.fight_mode:

            return

        self.manual_controlled = True

        if (
            self.y
            > self.world.ground_y + 1
        ):

            return

        if self.state == "jumping":

            return

        self.state = "jumping"

        self.jumping = True

        self.velocity_y = JUMP_SPEED

        self.timer = 0.0


    def finish_jump(self):

        self.y = (
            self.world.ground_y
        )

        self.velocity_y = 0.0

        self.jumping = False

        self.state = "walking"

        self.timer = 0.0

        self.set_walk_frame(
            self.frame
        )


    # ========================================================
    # FALLING
    # ========================================================

    def start_falling(self):

        if not self.falling_frames:

            self.y = (
                self.world.ground_y
            )

            self.velocity_y = 0.0

            self.state = "walking"

            return

        self.state = "falling"

        self.velocity_y = -40.0

        self.frame = 0

        self.timer = 0.0

        self.set_fall_frame(0)


    # ========================================================
    # LANDING
    # ========================================================

    def start_landing(self):

        if len(
            self.falling_frames
        ) < 12:

            self.start_walking()

            return

        self.state = "landing"

        self.timer = 0.0

        if self.name == "Amelia":

            self.frame = 3

        else:

            self.frame = 6

        self.set_fall_frame(
            self.frame
        )


    # ========================================================
    # WALKING
    # ========================================================

    def start_walking(self):

        self.state = "walking"

        self.velocity_y = 0.0

        self.y = min(
            self.y,
            self.world.ground_y
        )

        self.frame = 0

        self.timer = 0.0

        self.reset_random_movement()

        self.set_walk_frame(0)


    # ========================================================
    # IDLE
    # ========================================================

    def start_idle(self):

        if not self.idle_frames:

            if self.name == "Amelia":

                self.start_reaction()

            else:

                self.start_walking()

            return

        self.state = "idle"

        self.timer = (
            RANDOM_IDLE_DURATION
        )

        self.source = random.choice(
            self.idle_frames
        )

        self.reload()


    # ========================================================
    # WATSON REACTION
    # ========================================================

    def start_reaction(self):

        if self.name != "Amelia":

            return

        if not self.reaction_frames:

            return

        self.reaction_index += 1

        if (
            self.reaction_index
            >= len(
                self.reaction_frames
            )
        ):

            self.reaction_index = 0

        self.state = "reaction"

        self.reaction_timer = (
            REACTION_TIME
        )

        self.velocity_y = 0.0

        self.source = (
            self.reaction_frames[
                self.reaction_index
            ]
        )

        self.reload()


    # ========================================================
    # FIGHT START
    # ========================================================

    def start_fight(self, target):

        self.fighting = True

        self.fight_target = target

        self.manual_controlled = False

        self.velocity_x = 0.0

        self.state = "fight"

        self.fight_frame = 0

        self.fight_timer = 0.0

        self.fight_cooldown = 0.0

        self.trident_formed = False

        self.fight_hit_done = False

        if target.world_x > self.world_x:

            self.direction = 1

        else:

            self.direction = -1

        if self.name == "Gura":

            self.set_fight_frame(0)


    # ========================================================
    # STOP FIGHT
    # ========================================================

    def stop_fight(self):

        self.fighting = False

        self.fight_target = None

        self.fight_frame = 0

        self.fight_timer = 0.0

        self.fight_cooldown = 0.0

        self.trident_formed = False

        self.fight_hit_done = False

        self.velocity_x = 0.0

        self.start_walking()


    # ========================================================
    # TAKE DAMAGE
    # ========================================================

    def take_fight_damage(self, amount):

        print(
            self.name,
            "takes",
            amount,
            "damage"
        )

        if self.name == "Amelia":

            self.start_reaction()


    # ========================================================
    # FIGHT UPDATE
    # ========================================================

    def update_fight(self, dt):

        if not self.fighting:

            return

        target = self.fight_target

        if target is None:

            return


        # ----------------------------------------------------
        # REDUCE ATTACK COOLDOWN
        # ----------------------------------------------------

        if self.fight_cooldown > 0:

            self.fight_cooldown -= dt

            if self.fight_cooldown < 0:

                self.fight_cooldown = 0


        # ----------------------------------------------------
        # FACE TARGET
        # ----------------------------------------------------

        if target.world_x > self.world_x:

            self.direction = 1

        else:

            self.direction = -1


        # ----------------------------------------------------
        # MOVE TOWARD TARGET
        # ----------------------------------------------------

        distance = abs(
            (
                self.world_x
                + self.width / 2
            )
            -
            (
                target.world_x
                + target.width / 2
            )
        )


        if distance > FIGHT_DISTANCE:

            if (
                target.world_x
                > self.world_x
            ):

                self.world_x += (
                    FIGHT_APPROACH_SPEED
                    * dt
                )

            else:

                self.world_x -= (
                    FIGHT_APPROACH_SPEED
                    * dt
                )

            self.world_x = max(
                0,

                min(
                    self.world_x,
                    self.world.world_width
                    - self.width
                )
            )

            return


        # ----------------------------------------------------
        # GURA ATTACK
        # ----------------------------------------------------

        if self.name == "Gura":

            if not GURA_FIGHT_FRAMES:

                return

            self.fight_timer += dt

            if (
                self.fight_timer
                >= FIGHT_FRAME_TIME
            ):

                self.fight_timer = 0.0

                self.fight_frame += 1


                # --------------------------------------------
                # TRIDENT FORMS
                # --------------------------------------------

                if (
                    self.fight_frame
                    >= GURA_TRIDENT_START
                    and
                    self.fight_frame
                    <= GURA_TRIDENT_END
                ):

                    self.trident_formed = True


                # --------------------------------------------
                # ATTACK HIT
                # --------------------------------------------

                if (
                    self.fight_frame == 6
                    and not self.fight_hit_done
                    and self.fight_cooldown <= 0
                ):

                    current_distance = abs(
                        (
                            self.world_x
                            + self.width / 2
                        )
                        -
                        (
                            target.world_x
                            + target.width / 2
                        )
                    )

                    if (
                        current_distance
                        <= FIGHT_DISTANCE
                    ):

                        target.take_fight_damage(
                            FIGHT_DAMAGE
                        )

                        self.fight_hit_done = True

                        self.fight_cooldown = (
                            FIGHT_ATTACK_COOLDOWN
                        )


                # --------------------------------------------
                # LOOP ATTACK
                # --------------------------------------------

                if (
                    self.fight_frame
                    >= len(
                        GURA_FIGHT_FRAMES
                    )
                ):

                    self.fight_frame = 0

                    self.trident_formed = False

                    self.fight_hit_done = False


                self.set_fight_frame(
                    self.fight_frame
                )

            return


        # ----------------------------------------------------
        # AMELIA
        # ----------------------------------------------------

        if self.name == "Amelia":

            # Amelia uses Watson reaction sprites
            # during the current combat system.
            #
            # The reaction is allowed to finish before
            # returning to combat.

            if self.state == "fight":

                if (
                    self.reaction_timer
                    <= 0
                ):

                    self.start_reaction()


    # ========================================================
    # TAP
    # ========================================================

    def tapped(self):

        if self.world.fight_mode:

            return

        self.random_turn_timer = random.uniform(
            RANDOM_TURN_CHECK_MIN,
            RANDOM_TURN_CHECK_MAX
        )

        self.random_idle_timer = random.uniform(
            RANDOM_IDLE_MIN,
            RANDOM_IDLE_MAX
        )

        if self.name == "Gura":

            if self.idle_frames:

                self.start_idle()

            else:

                self.start_walking()

        elif self.name == "Amelia":

            self.start_reaction()


    # ========================================================
    # CHARACTER INTERACTION
    # ========================================================

    def start_character_interaction(
        self,
        other
    ):

        if self.world_x < other.world_x:

            self.set_direction(1)

        else:

            self.set_direction(-1)

        if self.name == "Gura":

            if self.idle_frames:

                self.state = "idle"

                self.timer = (
                    GURA_INTERACTION_TIME
                )

                self.source = random.choice(
                    self.idle_frames
                )

                self.reload()

        elif self.name == "Amelia":

            self.start_reaction()


    # ========================================================
    # DRAGGING
    # ========================================================

    def on_touch_down(self, touch):

        if self.world.fight_mode:

            return super().on_touch_down(
                touch
            )

        if not self.collide_point(
            touch.x,
            touch.y
        ):

            return super().on_touch_down(
                touch
            )

        touch.grab(self)

        self.touch_start_x = touch.x

        self.touch_start_y = touch.y

        self.drag_offset_x = (
            self.x - touch.x
        )

        self.drag_offset_y = (
            self.y - touch.y
        )

        self.dragging = False

        self.velocity_x = 0.0

        self.velocity_y = 0.0

        self.state = "dragging"

        return True


    def on_touch_move(self, touch):

        if touch.grab_current is not self:

            return super().on_touch_move(
                touch
            )

        dx = (
            touch.x
            - self.touch_start_x
        )

        dy = (
            touch.y
            - self.touch_start_y
        )

        distance = (
            dx * dx
            + dy * dy
        ) ** 0.5

        if (
            distance
            >= DRAG_THRESHOLD
        ):

            self.dragging = True

        if self.dragging:

            self.world_x = (
                touch.x
                + self.drag_offset_x
                + self.world.camera_x
            )

            self.world_x = max(
                0,

                min(
                    self.world_x,
                    self.world.world_width
                    - self.width
                )
            )

            self.y = (
                touch.y
                + self.drag_offset_y
            )

            min_y = (
                self.world.height
                * DRAG_MIN_Y_RATIO
            )

            max_y = (
                self.world.height
                * DRAG_MAX_Y_RATIO
            )

            self.y = max(
                min_y,

                min(
                    self.y,
                    max_y
                )
            )

            self.world.sync_character_positions()

        return True


    def on_touch_up(self, touch):

        if touch.grab_current is not self:

            return super().on_touch_up(
                touch
            )

        touch.ungrab(self)

        was_dragging = self.dragging

        self.dragging = False

        if was_dragging:

            if (
                self.y
                > self.world.ground_y + 1
            ):

                self.start_falling()

            else:

                self.y = (
                    self.world.ground_y
                )

                self.state = "walking"

                self.set_walk_frame(
                    self.frame
                )

            return True

        self.tapped()

        return True


    # ========================================================
    # SCREEN RECT
    # ========================================================

    def screen_rect(self):

        return (
            self.x,

            self.y,

            self.x + self.width,

            self.y + self.height
        )


    # ========================================================
    # UPDATE
    # ========================================================

    def update(self, dt):

        # ----------------------------------------------------
        # DRAGGING
        # ----------------------------------------------------

        if self.state == "dragging":

            return


        # ----------------------------------------------------
        # FIGHTING
        # ----------------------------------------------------

        if self.state == "fight":

            self.update_fight(dt)

            self.world.sync_character_positions()

            return


        # ----------------------------------------------------
        # REACTION
        # ----------------------------------------------------

        if self.state == "reaction":

            self.reaction_timer -= dt

            if (
                self.reaction_timer
                <= 0
            ):

                if self.world.fight_mode:

                    self.state = "fight"

                else:

                    self.start_walking()

            return


        # ----------------------------------------------------
        # JUMPING
        # ----------------------------------------------------

        if self.state == "jumping":

            self.world_x += (
                self.velocity_x
                * dt
            )

            self.velocity_y -= (
                GRAVITY * dt
            )

            self.y += (
                self.velocity_y
                * dt
            )

            self.world_x = max(
                0,

                min(
                    self.world_x,
                    self.world.world_width
                    - self.width
                )
            )

            self.timer += dt

            if (
                self.velocity_x != 0
                and self.walk_frames
            ):

                if (
                    self.timer
                    >= WALK_TIME
                ):

                    self.timer = 0.0

                    self.frame += 1

                    if (
                        self.frame
                        >= len(
                            self.walk_frames
                        )
                    ):

                        self.frame = 0

                    self.set_walk_frame(
                        self.frame
                    )

            if (
                self.y
                <= self.world.ground_y
            ):

                self.finish_jump()

            self.world.sync_character_positions()

            return


        # ----------------------------------------------------
        # FALLING
        # ----------------------------------------------------

        if self.state == "falling":

            self.velocity_y -= (
                GRAVITY * dt
            )

            self.y += (
                self.velocity_y * dt
            )

            if (
                self.y
                <= self.world.ground_y
            ):

                self.y = (
                    self.world.ground_y
                )

                self.start_landing()

            else:

                self.timer += dt

                if (
                    self.timer
                    >= FALL_TIME
                ):

                    self.timer = 0.0

                    self.frame += 1

                    max_frame = (
                        1
                        if self.name == "Amelia"
                        else 4
                    )

                    if (
                        self.frame
                        > max_frame
                    ):

                        self.frame = max_frame

                    self.set_fall_frame(
                        self.frame
                    )

            self.world.sync_character_positions()

            return


        # ----------------------------------------------------
        # LANDING
        # ----------------------------------------------------

        if self.state == "landing":

            self.timer += dt

            if (
                self.timer
                >= LAND_TIME
            ):

                self.timer = 0.0

                self.frame += 1

                if (
                    self.frame >= 12
                ):

                    self.start_walking()

                    return

                self.set_fall_frame(
                    self.frame
                )

            return


        # ----------------------------------------------------
        # IDLE
        # ----------------------------------------------------

        if self.state == "idle":

            self.timer -= dt

            if (
                self.timer <= 0
            ):

                self.start_walking()

            return


        # ----------------------------------------------------
        # WALKING
        # ----------------------------------------------------

        if self.state != "walking":

            return


        # ----------------------------------------------------
        # AUTONOMOUS MODE
        # ----------------------------------------------------

        if not self.manual_controlled:

            self.random_idle_timer -= dt

            if (
                self.random_idle_timer
                <= 0
            ):

                self.random_idle_timer = (
                    random.uniform(
                        RANDOM_IDLE_MIN,
                        RANDOM_IDLE_MAX
                    )
                )

                if (
                    random.random()
                    <= RANDOM_IDLE_CHANCE
                ):

                    self.start_idle()

                    return


            self.random_turn_timer -= dt

            if (
                self.random_turn_timer
                <= 0
            ):

                self.random_turn_timer = (
                    random.uniform(
                        RANDOM_TURN_CHECK_MIN,
                        RANDOM_TURN_CHECK_MAX
                    )
                )

                if (
                    random.random()
                    <= RANDOM_TURN_CHANCE
                ):

                    self.set_direction(
                        -self.direction
                    )

                    self.speed = random.uniform(
                        RANDOM_SPEED_MIN,
                        RANDOM_SPEED_MAX
                    )


            self.world_x += (
                self.direction
                * self.speed
                * dt
            )


            if self.world_x <= 0:

                self.world_x = 0

                self.set_direction(1)

            elif (
                self.world_x
                + self.width
                >= self.world.world_width
            ):

                self.world_x = (
                    self.world.world_width
                    - self.width
                )

                self.set_direction(-1)


            self.timer += dt

            if (
                self.timer
                >= WALK_TIME
            ):

                self.timer = 0.0

                if self.walk_frames:

                    self.frame += 1

                    if (
                        self.frame
                        >= len(
                            self.walk_frames
                        )
                    ):

                        self.frame = 0

                    self.set_walk_frame(
                        self.frame
                    )

            self.world.sync_character_positions()

            return


        # ----------------------------------------------------
        # MANUAL MODE
        # ----------------------------------------------------

        if self.velocity_x == 0:

            self.world.sync_character_positions()

            return


        self.world_x += (
            self.velocity_x
            * dt
        )


        if self.world_x <= 0:

            self.world_x = 0

            if self.velocity_x < 0:

                self.velocity_x = 0

        elif (
            self.world_x
            + self.width
            >= self.world.world_width
        ):

            self.world_x = (
                self.world.world_width
                - self.width
            )

            if self.velocity_x > 0:

                self.velocity_x = 0


        self.timer += dt

        if (
            self.timer
            >= WALK_TIME
        ):

            self.timer = 0.0

            if self.walk_frames:

                self.frame += 1

                if (
                    self.frame
                    >= len(
                        self.walk_frames
                    )
                ):

                    self.frame = 0

                self.set_walk_frame(
                    self.frame
                )

        self.world.sync_character_positions()


# ============================================================
# WORLD
# ============================================================

class PetWorld(FloatLayout):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


        # ====================================================
        # CAMERA
        # ====================================================

        self.camera_x = 0.0

        self.world_width = 0.0

        self.ground_y = 0.0


        # ====================================================
        # FIGHT MODE
        # ====================================================

        self.fight_mode = False


        # ====================================================
        # BACKGROUND
        # ====================================================

        self.background = Image(

            source=(
                BACKGROUND_FILE
                if os.path.isfile(
                    BACKGROUND_FILE
                )
                else ""
            ),

            size_hint=(
                None,
                None
            ),

            keep_ratio=True,

            allow_stretch=True
        )

        self.add_widget(
            self.background,
            index=0
        )


        # ====================================================
        # INITIAL BACKGROUND
        # ====================================================

        self.layout_background()


        # ====================================================
        # GURA
        # ====================================================

        self.gura = Chibi(

            world=self,

            name="Gura",

            left_frames=GURA_LEFT,

            right_frames=GURA_RIGHT,

            falling_frames=GURA_FALLING,

            idle_frames=GURA_IDLE,

            reaction_frames=None,

            world_x=(
                self.world_width
                * 0.15
            ),

            speed=GURA_SPEED
        )

        self.add_widget(
            self.gura
        )


        # ====================================================
        # AMELIA
        # ====================================================

        self.amelia = Chibi(

            world=self,

            name="Amelia",

            left_frames=AMELIA_LEFT,

            right_frames=AMELIA_RIGHT,

            falling_frames=AMELIA_FALLING,

            idle_frames=None,

            reaction_frames=WATSON_REACTIONS,

            world_x=(
                self.world_width
                * 0.75
            ),

            speed=AMELIA_SPEED
        )

        self.amelia.set_direction(-1)

        self.add_widget(
            self.amelia
        )


        # ====================================================
        # START AUTONOMOUS
        # ====================================================

        self.gura.set_random_mode(
            True
        )

        self.amelia.set_random_mode(
            True
        )


        # ====================================================
        # CONTROLLED CHARACTER
        # ====================================================

        self.controlled_character = (
            "Gura"
        )

        self.gura.manual_controlled = True

        self.gura.velocity_x = 0.0


        # ====================================================
        # CHARACTER BUTTON
        # ====================================================

        self.character_button = Button(

            text="GURA",

            size_hint=(
                None,
                None
            ),

            size=(
                150,
                60
            ),

            font_size=20,

            bold=True
        )

        self.character_button.bind(
            on_release=lambda *args:
                self.toggle_controlled_character()
        )

        self.add_widget(
            self.character_button
        )


        # ====================================================
        # FIGHT BUTTON
        # ====================================================

        self.fight_button = Button(

            text="FIGHT: OFF",

            size_hint=(
                None,
                None
            ),

            size=(
                170,
                60
            ),

            font_size=18,

            bold=True
        )

        self.fight_button.bind(
            on_release=lambda *args:
                self.toggle_fight_mode()
        )

        self.add_widget(
            self.fight_button
        )


        # ====================================================
        # JOYSTICK
        # ====================================================

        self.joystick = VirtualJoystick(

            on_move=self.control_character,

            size_hint=(
                None,
                None
            ),

            size=(
                150,
                150
            )
        )

        self.add_widget(
            self.joystick
        )


        # ====================================================
        # JUMP
        # ====================================================

        self.jump_button = Button(

            text="JUMP",

            size_hint=(
                None,
                None
            ),

            size=(
                120,
                70
            ),

            font_size=20,

            bold=True
        )

        self.jump_button.bind(
            on_release=lambda *args:
                self.jump_character()
        )

        self.add_widget(
            self.jump_button
        )


        # ====================================================
        # INTERACTION
        # ====================================================

        self.interaction_cooldown = 0.0

        self.interaction_check_timer = (
            random.uniform(
                INTERACTION_CHECK_MIN,
                INTERACTION_CHECK_MAX
            )
        )


        self.update_control_button_positions()

        self.sync_character_positions()


        # ====================================================
        # GAME LOOP
        # ====================================================

        Clock.schedule_interval(
            self.update,
            1.0 / 60.0
        )


    # ========================================================
    # BACKGROUND
    # ========================================================

    def layout_background(self):

        if not self.background.source:

            return


        self.background.height = max(
            Window.height,
            1
        )

        original_width = 1774.0

        original_height = 887.0

        self.background.width = (
            original_width
            / original_height
            * self.background.height
        )

        self.background.y = 0

        self.world_width = (
            self.background.width
        )


        self.ground_y = (
            Window.height
            * GROUND_Y_RATIO
        )


        self.camera_x = max(
            0.0,

            min(
                self.camera_x,

                max(
                    0.0,
                    self.world_width
                    - Window.width
                )
            )
        )


        self.background.x = (
            -self.camera_x
        )


    # ========================================================
    # SPRITE SIZE
    # ========================================================

    def get_sprite_size(self):

        if (
            Window.width
            > Window.height
        ):

            return LANDSCAPE_SPRITE_SIZE

        return SPRITE_SIZE


    # ========================================================
    # UPDATE CHARACTER SIZE
    # ========================================================

    def update_character_sizes(self):

        sprite_size = (
            self.get_sprite_size()
        )

        for character in (
            self.gura,
            self.amelia
        ):

            character.size = (
                sprite_size,
                sprite_size
            )


    # ========================================================
    # SYNC POSITIONS
    # ========================================================

    def sync_character_positions(self):

        for character in (
            self.gura,
            self.amelia
        ):

            character.x = (
                character.world_x
                - self.camera_x
            )


    # ========================================================
    # CAMERA SCROLL
    # ========================================================

    def scroll_camera(self, amount):

        max_camera = max(
            0.0,

            self.world_width
            - Window.width
        )

        old_camera = (
            self.camera_x
        )

        self.camera_x = max(
            0.0,

            min(
                self.camera_x + amount,
                max_camera
            )
        )

        if (
            self.camera_x
            != old_camera
        ):

            self.background.x = (
                -self.camera_x
            )

            self.sync_character_positions()


    # ========================================================
    # CAMERA FOLLOW
    # ========================================================

    def update_camera_follow(self):

        character = (
            self.get_controlled_character()
        )

        if character is None:

            return


        if character.state in (
            "dragging",
            "reaction",
            "idle"
        ):

            return


        left_limit = (
            Window.width
            * CAMERA_LEFT_MARGIN
        )

        right_limit = (
            Window.width
            * CAMERA_RIGHT_MARGIN
        )


        if (
            character.x
            > right_limit
        ):

            self.scroll_camera(
                character.x
                - right_limit
            )


        elif (
            character.x
            < left_limit
        ):

            self.scroll_camera(
                character.x
                - left_limit
            )


    # ========================================================
    # CHARACTER SWITCHING
    # ========================================================

    def toggle_controlled_character(self):

        if self.fight_mode:

            return


        current = (
            self.controlled_character
        )


        if current == "Gura":

            next_character = "Amelia"

        elif current == "Amelia":

            next_character = "None"

        else:

            next_character = "Gura"


        self.gura.manual_controlled = False

        self.gura.velocity_x = 0.0

        self.amelia.manual_controlled = False

        self.amelia.velocity_x = 0.0


        for character in (
            self.gura,
            self.amelia
        ):

            if character.state in (
                "idle",
                "reaction"
            ):

                character.state = "walking"

                character.timer = 0.0

                character.set_walk_frame(
                    character.frame
                )

            character.reset_random_movement()


        self.controlled_character = (
            next_character
        )


        if next_character == "Gura":

            new = self.gura

            self.character_button.text = (
                "GURA"
            )


        elif next_character == "Amelia":

            new = self.amelia

            self.character_button.text = (
                "AMELIA"
            )


        else:

            new = None

            self.character_button.text = (
                "NONE"
            )


        if new is not None:

            new.manual_controlled = True

            new.velocity_x = 0.0


            if new.state in (
                "idle",
                "reaction"
            ):

                new.state = "walking"

                new.timer = 0.0

                new.set_walk_frame(
                    new.frame
                )


            target_screen_x = (
                Window.width
                * 0.5
            )


            desired_camera = (
                new.world_x
                - target_screen_x
            )


            max_camera = max(
                0.0,

                self.world_width
                - Window.width
            )


            self.camera_x = max(
                0.0,

                min(
                    desired_camera,
                    max_camera
                )
            )


            self.background.x = (
                -self.camera_x
            )

            self.sync_character_positions()


        if next_character == "None":

            if (
                self.joystick.parent
                is self
            ):

                self.remove_widget(
                    self.joystick
                )

            if (
                self.jump_button.parent
                is self
            ):

                self.remove_widget(
                    self.jump_button
                )

        else:

            if self.joystick.parent is None:

                self.add_widget(
                    self.joystick
                )

            if self.jump_button.parent is None:

                self.add_widget(
                    self.jump_button
                )

            self.update_control_button_positions()


    # ========================================================
    # FIGHT TOGGLE
    # ========================================================

    def toggle_fight_mode(self):

        self.fight_mode = (
            not self.fight_mode
        )


        if self.fight_mode:

            self.fight_button.text = (
                "FIGHT: ON"
            )


            # Stop normal movement.

            self.gura.manual_controlled = False

            self.amelia.manual_controlled = False

            self.gura.velocity_x = 0.0

            self.amelia.velocity_x = 0.0


            # Start combat.

            self.gura.start_fight(
                self.amelia
            )

            self.amelia.start_fight(
                self.gura
            )


        else:

            self.fight_button.text = (
                "FIGHT: OFF"
            )


            self.gura.stop_fight()

            self.amelia.stop_fight()


            # Return to autonomous movement.

            self.gura.set_random_mode(
                True
            )

            self.amelia.set_random_mode(
                True
            )


            # Keep Gura selected.

            if (
                self.controlled_character
                == "Gura"
            ):

                self.gura.manual_controlled = (
                    True
                )


    # ========================================================
    # CONTROLS
    # ========================================================

    def get_controlled_character(self):

        if (
            self.controlled_character
            == "Gura"
        ):

            return self.gura


        if (
            self.controlled_character
            == "Amelia"
        ):

            return self.amelia


        return None


    def control_character(self, direction):

        if self.fight_mode:

            return

        character = (
            self.get_controlled_character()
        )

        if character is not None:

            character.set_horizontal_input(
                direction
            )


    def jump_character(self):

        if self.fight_mode:

            return

        character = (
            self.get_controlled_character()
        )

        if character is not None:

            character.jump()


    # ========================================================
    # UI POSITION
    # ========================================================

    def update_control_button_positions(self):

        self.character_button.pos = (
            210,
            Window.height - 80
        )


        self.fight_button.pos = (
            380,
            Window.height - 80
        )


        self.joystick.pos = (
            20,
            25
        )


        self.jump_button.pos = (
            Window.width - 160,
            25
        )


    # ========================================================
    # CHARACTER INTERACTION
    # ========================================================

    def check_character_interaction(self):

        if self.fight_mode:

            return


        if (
            self.interaction_cooldown
            > 0
        ):

            return


        if self.gura.state in (
            "dragging",
            "falling",
            "landing"
        ):

            return


        if self.amelia.state in (
            "dragging",
            "falling",
            "landing"
        ):

            return


        distance = abs(
            (
                self.gura.world_x
                + self.gura.width / 2
            )
            -
            (
                self.amelia.world_x
                + self.amelia.width / 2
            )
        )


        if (
            distance
            > INTERACTION_DISTANCE
        ):

            return


        if (
            random.random()
            > CHARACTER_INTERACTION_CHANCE
        ):

            return


        if (
            abs(
                self.gura.y
                - self.amelia.y
            )
            > 100
        ):

            return


        self.gura.start_character_interaction(
            self.amelia
        )

        self.amelia.start_character_interaction(
            self.gura
        )

        self.interaction_cooldown = (
            INTERACTION_COOLDOWN
        )


    # ========================================================
    # WINDOW RESIZE
    # ========================================================

    def on_size(self, *args):

        old_width = (
            self.world_width
        )

        old_ground = (
            self.ground_y
        )


        self.layout_background()

        self.update_character_sizes()


        if old_width <= 0:

            self.gura.world_x = (
                self.world_width
                * 0.15
            )

            self.amelia.world_x = (
                self.world_width
                * 0.75
            )


        if (
            abs(
                old_ground
                - self.ground_y
            )
            > 0.1
        ):

            for character in (
                self.gura,
                self.amelia
            ):

                if character.state in (
                    "walking",
                    "idle",
                    "reaction"
                ):

                    character.y = (
                        self.ground_y
                    )


        self.update_control_button_positions()

        self.sync_character_positions()


    # ========================================================
    # MAIN UPDATE
    # ========================================================

    def update(self, dt):

        self.gura.update(dt)

        self.amelia.update(dt)


        self.update_camera_follow()


        # ----------------------------------------------------
        # NORMAL INTERACTION COOLDOWN
        # ----------------------------------------------------

        if (
            self.interaction_cooldown
            > 0
        ):

            self.interaction_cooldown -= dt

            if (
                self.interaction_cooldown
                < 0
            ):

                self.interaction_cooldown = 0


        # ----------------------------------------------------
        # NORMAL RANDOM INTERACTION
        # ----------------------------------------------------

        if not self.fight_mode:

            self.interaction_check_timer -= dt

            if (
                self.interaction_check_timer
                <= 0
            ):

                self.interaction_check_timer = (
                    random.uniform(
                        INTERACTION_CHECK_MIN,
                        INTERACTION_CHECK_MAX
                    )
                )

                self.check_character_interaction()


# ============================================================
# APP
# ============================================================

class ChibiPetApp(App):

    def build(self):

        Window.clearcolor = (
            0,
            0,
            0,
            1
        )

        return PetWorld()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    ChibiPetApp().run()