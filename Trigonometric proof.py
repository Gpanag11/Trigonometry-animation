from manim import *
import numpy as np
from manim import X11
from manim import XKCD

class CoordsToPointExample(MovingCameraScene):
    def construct(self):

        # Create axes with a fixed range and unit length
        ax = Axes(
            x_range=[-1, 1, 1],  # Adjusting the x-axis range
            y_range=[-1, 1, 1],  # Adjusting the y-axis range
            axis_config={"include_numbers": True},
            x_length=4,
            y_length=4,
            x_axis_config={
                "include_tip": False,
                "tick_size": 0.05,
                "numbers_with_elongated_ticks": [-1, 1],
                "include_numbers": True,
            },
            y_axis_config={
                "include_tip": False,
                "tick_size": 0.05,
                "numbers_with_elongated_ticks": [-1, 1],
                "include_numbers": True,
            }
        )
        # Create the number plane
        plane = NumberPlane(
            x_range=[-3, 3, 1],  # Adjusting the x-axis range
            y_range=[-3, 3, 1],  # Adjusting the y-axis range
            background_line_style={
                "stroke_color": X11.THISTLE,
                "stroke_width": 2,
                "stroke_opacity": 0.6
            }
        )

        # Create a unit circle centered at the origin of the axes
        circle = Circle(radius=2, color=XKCD.LIGHTPERIWINKLE)
        circle.move_to(ax.c2p(0, 0))

        # Add the axes and number plane
        self.add(plane, ax)

        # Animate the growth of the axes and circle
        self.play(GrowFromCenter(ax))
        self.wait(1)
        self.play(GrowFromCenter(circle), run_time=2)
        self.wait(1)

        # Function to create the triangle lines
        def create_triangle(ax, radius, angle):
            radius_line = Line(ax.c2p(0, 0), ax.c2p(radius * np.cos(angle), radius * np.sin(angle)), color=X11.MEDIUMORCHID1, stroke_width=3)
            horizontal_line = Line(ax.c2p(0, 0), ax.c2p(radius * np.cos(angle), 0), color=X11.MEDIUMPURPLE1, stroke_width=3)
            vertical_line = Line(ax.c2p(radius * np.cos(angle), 0), ax.c2p(radius * np.cos(angle), radius * np.sin(angle)), color=X11.MEDIUMPURPLE1, stroke_width=3)
            return radius_line, horizontal_line, vertical_line

        # Create the initial triangle lines
        radius_line, horizontal_line, vertical_line = create_triangle(ax, 1, np.pi / 4)

        # Add and animate each line separately with waits in between
        self.play(GrowFromCenter(radius_line), run_time=2)
        self.wait(1)
        self.add(radius_line)

        self.play(GrowFromEdge(horizontal_line, LEFT), run_time=2)
        self.wait(1)
        self.add(horizontal_line)

        self.play(GrowFromEdge(vertical_line, DOWN), run_time=2)
        self.wait(1)
        self.add(vertical_line)

        # Group the lines together
        triangle = VGroup(radius_line, horizontal_line, vertical_line)

        self.wait(1)

        self.play(FadeOut(triangle), run_time=2)

        # Function to update the triangle for a given quadrant
        def update_triangle(triangle, ax, radius, angle):
            radius_line, horizontal_line, vertical_line = triangle
            radius_line.put_start_and_end_on(ax.c2p(0, 0), ax.c2p(radius * np.cos(angle), radius * np.sin(angle)))
            horizontal_line.put_start_and_end_on(ax.c2p(0, 0), ax.c2p(radius * np.cos(angle), 0))
            vertical_line.put_start_and_end_on(ax.c2p(radius * np.cos(angle), 0), ax.c2p(radius * np.cos(angle), radius * np.sin(angle)))
            return triangle

        triangle = update_triangle(triangle, ax, 1, 5 * np.pi / 4)
        self.play(FadeIn(triangle), run_time=2)
        self.wait(3)
        self.play(FadeOut(triangle), run_time=2)

        self.wait(2)

        triangle = update_triangle(triangle, ax, 1, 1 * np.pi / 4)
        self.play(FadeIn(triangle), run_time=2)

        # Create the angle arc and labels only for the final triangle
        arc = Arc(radius=0.4, start_angle=0, angle=np.pi / 4, color=X11.CYAN1, stroke_width=2).move_arc_center_to(ax.c2p(0, 0))
        hypotenuse_label = MathTex("Radius = 1").rotate(np.pi / 4).scale(0.5)
        hypotenuse_label.move_to(radius_line.get_center() + np.array([0.002, 0.3, 0]))
        a_label = MathTex("a").next_to(horizontal_line, DOWN, buff=0.1).scale(0.6)
        b_label = MathTex("b").next_to(vertical_line, RIGHT, buff=0.1).scale(0.6)

        # Position theta slightly to the right of the arc
        theta_position = arc.point_from_proportion(0.3) + np.array([0.2, 0.1, 0.0])
        theta_label = MathTex(r"\theta").move_to(theta_position).scale(0.6)


        self.play(Write(hypotenuse_label))
        self.play(Write(a_label))
        self.play(Write(b_label))
        self.play(GrowFromCenter(arc), run_time=2)
        self.add(arc)
        self.play(Write(theta_label))

        # At the end of the animation, shift everything to the left
        all_elements = VGroup(plane, ax, circle, radius_line, horizontal_line, vertical_line, arc, hypotenuse_label, a_label, b_label, theta_label)
        self.play(all_elements.animate.shift(3 * LEFT))
        self.wait(1)

        pythagorean_theorem = MathTex(r"\text{horizontal}^2 + \text{vertical}^2 = \text{hypotenuse}^2").scale(0.7)
        pythagorean_theorem.move_to([3.3, 3.1, 0])
        self.play(Write(pythagorean_theorem))
        self.wait(2)

        # Emphasize 'a' and animate to the right
        self.play(Indicate(a_label), scale_factor=2.5, run_time=2)
        self.wait(1)
        a_squared = MathTex("a^2").move_to([1.4, 2.4, 0]).scale(0.8)
        self.play(TransformFromCopy(a_label, a_squared))
        self.wait(1)

        # Emphasize 'b' and animate to the right
        self.play(Indicate(b_label), scale_factor=2.5, run_time=2)
        self.wait(1)
        b_squared = MathTex("b^2").move_to([2.9, 2.4, 0]).scale(0.8)
        self.play(TransformFromCopy(b_label, b_squared))
        self.wait(1)

        # Emphasize hypotenuse and animate to the right
        self.play(Indicate(hypotenuse_label), scale_factor=1.5, run_time=2)
        self.wait(1)

        c_squared = MathTex("radius^2").move_to([4.6, 2.4, 0]).scale(0.8)
        self.play(TransformFromCopy(hypotenuse_label, c_squared))

        symbol1 = MathTex("+").move_to([2.1, 2.4, 0]).scale(0.8)
        symbol2 = MathTex('=').move_to([3.5, 2.35, 0]).scale(0.8)
        self.play(Write(symbol1))
        self.play(Write(symbol2))
        self.wait(3)

        sin8 = MathTex(r"sin\theta").move_to([1.2, 1.5, 0]).scale(0.8)
        symbol3 = MathTex("=").scale(0.8).next_to(sin8, RIGHT, buff=0.1)
        ratio = MathTex("-").scale(2.7).next_to(symbol3, RIGHT, buff=0.1)
        self.play(Write(sin8))
        self.play(Write(symbol3))
        self.play(Write(ratio))
        self.wait(2)
        self.play(Indicate(b_label), scale_factor=2.0, run_time=2)
        b_label_copy = b_label.copy()
        new_position = [2.35, 1.8, 0]
        self.play(
            b_label_copy.animate.move_to(new_position).scale(0.4 / 0.3)  # Scale down from 0.6 to 0.4
        )
        self.wait(2)

        self.play(Indicate(hypotenuse_label), scale_factor=1.5, run_time=2)
        self.wait(1)

        hypotenuse_label2 = MathTex("Radius").move_to([2.4, 1.2, 0]).scale(0.66)
        self.play(TransformFromCopy(hypotenuse_label, hypotenuse_label2))
        self.wait(3)

        cos8 = MathTex(r"cos\theta").move_to([3.7, 1.5, 0]).scale(0.8)
        symbol3 = MathTex("=").scale(0.8).next_to(cos8, RIGHT, buff=0.1)
        ratio = MathTex("-").scale(2.7).next_to(symbol3, RIGHT, buff=0.1)
        self.play(Write(cos8))
        self.play(Write(symbol3))
        self.play(Write(ratio))
        self.wait(2)
        self.play(Indicate(a_label), scale_factor=2.0, run_time=2)
        a_label_copy = a_label.copy()
        new_position = [4.9, 1.8, 0]
        self.play(
            a_label_copy.animate.move_to(new_position).scale(0.4 / 0.27)  # Scale down from 0.6 to 0.4
        )
        self.wait(2)

        self.play(Indicate(hypotenuse_label), scale_factor=1.5, run_time=2)
        self.wait(1)

        hypotenuse_label2 = MathTex("Radius").move_to([5, 1.2, 0]).scale(0.66)
        self.play(TransformFromCopy(hypotenuse_label, hypotenuse_label2))
        self.wait(3)

        diagonal_line_sin = Line(start=[2.0, 1.3, 0], end=[2.6, 1.1, 0], color=RED)
        equals_one_sin = MathTex("= 1").next_to(diagonal_line_sin, DOWN * 0.2, buff=0.1).scale(0.65)

        diagonal_line_cos = Line(start=[4.7, 1.3, 0], end=[5.3, 1.1, 0], color=RED)
        equals_one_cos = MathTex("= 1").next_to(diagonal_line_cos, DOWN * 0.2, buff=0.1).scale(0.65)

        self.play(Write(diagonal_line_sin), Write(equals_one_sin))
        self.play(Write(diagonal_line_cos), Write(equals_one_cos))
        self.wait(3)

        sin_label = MathTex(r"\sin\theta = b").move_to([1.65, 0.4, 0]).scale(0.8)
        self.play(Write(sin_label))

        cos_label = MathTex(r"\cos\theta = a").move_to([4.35, 0.4, 0]).scale(0.8)
        self.play(Write(cos_label))

        # Create and transform a new label from the existing sin_label
        sin_label_new = MathTex(r"\sin^2\theta = b^2").move_to([1.6, -0.35, 0]).scale(0.8)
        self.play(TransformFromCopy(sin_label, sin_label_new))
        self.wait(2)
        cos_label_new = MathTex(r"\cos^2\theta = a^2").move_to([4.3, -0.35, 0]).scale(0.8)
        self.play(TransformFromCopy(cos_label, cos_label_new))
        self.wait(5)

        formula1 = VGroup(a_squared, symbol1, b_squared, symbol2, c_squared)
        self.play(Transform(formula1, formula1.copy()))
        self.wait(2)

        # Transform into trigonometric identity
        new_1 = MathTex(r"\sin^2\theta + \cos^2\theta = 1").move_to([2.9,-1.2,0]).scale(0.8)
        self.play(TransformFromCopy(formula1, new_1),run_time=1.5)
        self.wait(3)
        

