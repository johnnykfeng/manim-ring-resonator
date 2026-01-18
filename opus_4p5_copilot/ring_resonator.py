"""
Photonic Ring Resonator Animation using Manim
Demonstrates resonance phenomena, electric field propagation, and transmission characteristics
"""

from manim import *
import numpy as np

class RingResonatorAnimation(Scene):
    def construct(self):
        # Physical parameters
        self.n_eff = 2.4  # Effective refractive index (silicon)
        self.ring_radius = 10e-6  # 10 micron radius
        self.L = 2 * np.pi * self.ring_radius  # Round-trip length
        self.r = 0.9  # Self-coupling coefficient
        self.a = 0.95  # Round-trip amplitude transmission (accounts for loss)
        self.lambda_center = 1550e-9  # Center wavelength (telecom C-band)
        
        # Title
        title = Text("Photonic Ring Resonator", font_size=40).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)
        
        # Create the ring resonator schematic
        self.create_resonator_schematic()
        
        # Show the physics equations
        self.show_equations()
        
        # Animate the electric field
        self.animate_electric_field()
        
        # Show transmission spectrum
        self.show_transmission_spectrum()
        
        # Final summary
        self.final_summary()
    
    def create_resonator_schematic(self):
        """Create the ring resonator device schematic"""
        
        # Ring
        ring = Circle(radius=1.2, color=BLUE, stroke_width=8)
        ring.shift(UP * 0.5)
        
        # Input waveguide (bus waveguide)
        input_wg = Line(LEFT * 4, RIGHT * 4, color=BLUE, stroke_width=8)
        input_wg.shift(DOWN * 1.0)
        
        # Labels
        input_label = Text("Input", font_size=24, color=GREEN).next_to(input_wg, LEFT)
        through_label = Text("Through", font_size=24, color=RED).next_to(input_wg, RIGHT)
        ring_label = Text("Ring Resonator", font_size=24, color=YELLOW).next_to(ring, UP)
        
        # Coupling region indicator
        coupling_region = DashedLine(
            LEFT * 1.5 + DOWN * 0.7, 
            RIGHT * 1.5 + DOWN * 0.7, 
            color=YELLOW,
            stroke_width=2
        )
        coupling_text = Text("Coupling Region", font_size=18, color=YELLOW)
        coupling_text.next_to(coupling_region, DOWN, buff=0.1)
        
        # Group everything
        self.schematic = VGroup(ring, input_wg, input_label, through_label, 
                                 ring_label, coupling_region, coupling_text)
        self.schematic.scale(0.7).shift(LEFT * 3.5)
        
        self.play(
            Create(ring),
            Create(input_wg),
            run_time=1.5
        )
        self.play(
            Write(input_label),
            Write(through_label),
            Write(ring_label),
            Create(coupling_region),
            Write(coupling_text),
            run_time=1.5
        )
        
        # Store references for later use
        self.ring = ring
        self.input_wg = input_wg
        
        self.wait(0.5)
    
    def show_equations(self):
        """Display the key physics equations"""
        
        equations_title = Text("Resonance Condition & Transmission", font_size=28, color=YELLOW)
        equations_title.to_edge(RIGHT).shift(UP * 3 + LEFT * 0.5)
        
        # Resonance condition
        resonance_eq = MathTex(
            r"\phi = \frac{2\pi n_{eff} L}{\lambda} = 2\pi m",
            font_size=32
        )
        resonance_eq.next_to(equations_title, DOWN, buff=0.3)
        
        # Transmission equation
        transmission_eq = MathTex(
            r"T = \frac{a^2 - 2ar\cos(\phi) + r^2}{1 - 2ar\cos(\phi) + (ar)^2}",
            font_size=30
        )
        transmission_eq.next_to(resonance_eq, DOWN, buff=0.4)
        
        # Parameter definitions
        params = VGroup(
            MathTex(r"r = \text{self-coupling}", font_size=22),
            MathTex(r"a = \text{round-trip loss}", font_size=22),
            MathTex(r"\phi = \text{round-trip phase}", font_size=22),
            MathTex(r"n_{eff} = \text{effective index}", font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        params.next_to(transmission_eq, DOWN, buff=0.4)
        
        self.equations_group = VGroup(equations_title, resonance_eq, transmission_eq, params)
        
        self.play(Write(equations_title))
        self.play(Write(resonance_eq), run_time=1.5)
        self.play(Write(transmission_eq), run_time=1.5)
        self.play(Write(params), run_time=1.5)
        
        self.wait(1)
    
    def animate_electric_field(self):
        """Animate electric field propagation through the resonator"""
        
        # Add E-field animation title
        efield_title = Text("Electric Field Propagation", font_size=24, color=GREEN)
        efield_title.next_to(self.schematic, DOWN, buff=0.5)
        self.play(Write(efield_title))
        
        # Create input wave
        def create_wave_dots(path_points, color, n_dots=15):
            dots = VGroup()
            for i in range(n_dots):
                dot = Dot(radius=0.08, color=color)
                dot.set_opacity(0.8)
                dots.add(dot)
            return dots
        
        # Input waveguide path (left side)
        input_wave = create_wave_dots(None, GREEN, n_dots=8)
        
        # Ring wave
        ring_wave = create_wave_dots(None, YELLOW, n_dots=12)
        
        # Output wave (through port)
        output_wave = create_wave_dots(None, RED, n_dots=8)
        
        # Animation: Wave enters from input
        input_start = self.input_wg.get_left() + RIGHT * 0.5
        coupling_point = self.input_wg.get_center()
        output_end = self.input_wg.get_right() - RIGHT * 0.5
        
        # Position input wave
        for i, dot in enumerate(input_wave):
            dot.move_to(input_start + RIGHT * i * 0.3)
        
        self.play(FadeIn(input_wave))
        
        # Move input wave toward coupling region
        self.play(
            input_wave.animate.shift(RIGHT * 2),
            run_time=1.5,
            rate_func=linear
        )
        
        # Some light couples into ring - show ring circulation
        ring_center = self.ring.get_center()
        ring_radius = 1.2 * 0.7  # Scaled radius
        
        # Position ring wave around the ring
        for i, dot in enumerate(ring_wave):
            angle = i * 2 * np.pi / len(ring_wave)
            pos = ring_center + ring_radius * np.array([np.cos(angle), np.sin(angle), 0])
            dot.move_to(pos)
        
        # Show coupling: some light goes to ring, some continues
        self.play(
            FadeIn(ring_wave),
            input_wave.animate.shift(RIGHT * 1),
            run_time=1
        )
        
        # Animate ring circulation (multiple round trips)
        for _ in range(3):
            self.play(
                Rotate(ring_wave, angle=2*np.pi, about_point=ring_center),
                run_time=1.5,
                rate_func=linear
            )
        
        # Show output wave
        for i, dot in enumerate(output_wave):
            dot.move_to(coupling_point + RIGHT * (i + 1) * 0.3)
        
        self.play(
            FadeIn(output_wave),
            input_wave.animate.shift(RIGHT * 1.5),
            run_time=1
        )
        
        # Continue circulation while output exits
        self.play(
            Rotate(ring_wave, angle=2*np.pi, about_point=ring_center),
            output_wave.animate.shift(RIGHT * 1.5),
            run_time=1.5,
            rate_func=linear
        )
        
        # Add explanation
        resonance_text = Text(
            "At resonance: light builds up in ring",
            font_size=20,
            color=YELLOW
        ).next_to(efield_title, DOWN, buff=0.2)
        
        self.play(Write(resonance_text))
        self.wait(0.5)
        
        # Cleanup
        self.play(
            FadeOut(input_wave),
            FadeOut(ring_wave),
            FadeOut(output_wave),
            FadeOut(efield_title),
            FadeOut(resonance_text)
        )
    
    def transmission_function(self, wavelength):
        """Calculate transmission as function of wavelength"""
        phi = 2 * np.pi * self.n_eff * self.L / wavelength
        r, a = self.r, self.a
        
        numerator = a**2 - 2*a*r*np.cos(phi) + r**2
        denominator = 1 - 2*a*r*np.cos(phi) + (a*r)**2
        
        return numerator / denominator
    
    def show_transmission_spectrum(self):
        """Show the transmission vs wavelength plot"""
        
        # Fade out equations to make room
        self.play(
            self.schematic.animate.scale(0.6).to_edge(LEFT).shift(UP * 0.5),
            FadeOut(self.equations_group)
        )
        
        # Create wavelength array (around 1550 nm)
        lambda_range = np.linspace(1540e-9, 1560e-9, 1000)
        transmission = self.transmission_function(lambda_range)
        
        # Convert to plot coordinates
        lambda_nm = lambda_range * 1e9  # Convert to nm
        transmission_dB = 10 * np.log10(transmission + 1e-10)  # dB scale
        
        # Create axes
        axes = Axes(
            x_range=[1540, 1560, 5],
            y_range=[-30, 5, 5],
            x_length=7,
            y_length=4,
            axis_config={
                "color": WHITE,
                "include_tip": True,
                "include_numbers": True,
            },
            x_axis_config={"numbers_to_include": [1540, 1545, 1550, 1555, 1560]},
            y_axis_config={"numbers_to_include": [-30, -25, -20, -15, -10, -5, 0]},
        )
        axes.shift(RIGHT * 2)
        
        # Axis labels
        x_label = axes.get_x_axis_label(
            MathTex(r"\lambda \text{ (nm)}", font_size=28),
            edge=DOWN, direction=DOWN
        )
        y_label = axes.get_y_axis_label(
            MathTex(r"T \text{ (dB)}", font_size=28),
            edge=LEFT, direction=LEFT
        )
        
        # Title for plot
        plot_title = Text("Transmission Spectrum", font_size=28, color=YELLOW)
        plot_title.next_to(axes, UP)
        
        # Create the transmission curve
        transmission_curve = axes.plot_line_graph(
            x_values=lambda_nm,
            y_values=np.clip(transmission_dB, -30, 5),
            line_color=BLUE,
            add_vertex_dots=False,
            stroke_width=2.5
        )
        
        self.play(
            Create(axes),
            Write(x_label),
            Write(y_label),
            Write(plot_title),
            run_time=1.5
        )
        
        # Animate the curve drawing
        self.play(Create(transmission_curve), run_time=2)
        
        # Find and mark resonance dips
        # Find local minima (resonances)
        from scipy.signal import find_peaks
        peaks_idx, _ = find_peaks(-transmission_dB, height=5, distance=20)
        
        resonance_markers = VGroup()
        resonance_labels = VGroup()
        
        for i, idx in enumerate(peaks_idx[:3]):  # Mark first 3 resonances
            wavelength = lambda_nm[idx]
            trans_val = transmission_dB[idx]
            
            point = axes.c2p(wavelength, trans_val)
            marker = Dot(point, color=RED, radius=0.1)
            resonance_markers.add(marker)
            
            # Add FSR annotation between first two peaks
            if i == 0 and len(peaks_idx) > 1:
                fsr_wavelength = lambda_nm[peaks_idx[1]] - lambda_nm[peaks_idx[0]]
                fsr_text = MathTex(
                    rf"\Delta\lambda_{{FSR}} \approx {fsr_wavelength:.2f} \text{{ nm}}",
                    font_size=22,
                    color=GREEN
                )
                fsr_text.next_to(axes, DOWN, buff=0.8)
                self.fsr_text = fsr_text
        
        self.play(Create(resonance_markers))
        
        # Add FSR (Free Spectral Range) annotation
        if hasattr(self, 'fsr_text'):
            # Draw double-headed arrow between two resonances
            if len(peaks_idx) >= 2:
                p1 = axes.c2p(lambda_nm[peaks_idx[0]], -25)
                p2 = axes.c2p(lambda_nm[peaks_idx[1]], -25)
                fsr_arrow = DoubleArrow(p1, p2, color=GREEN, buff=0, stroke_width=2)
                self.play(Create(fsr_arrow), Write(self.fsr_text))
        
        # Add critical coupling explanation
        coupling_info = VGroup(
            Text("Resonance conditions:", font_size=20, color=YELLOW),
            MathTex(r"\bullet \text{ } \phi = 2\pi m \text{ (constructive interference)}", font_size=18),
            MathTex(r"\bullet \text{ Critical coupling: } r = a", font_size=18),
            MathTex(r"\bullet \text{ Q-factor } \propto \frac{1}{1-ar}", font_size=18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        coupling_info.to_edge(LEFT).shift(DOWN * 2)
        
        self.play(Write(coupling_info), run_time=2)
        
        self.wait(2)
        
        # Store for later cleanup
        self.axes = axes
        self.transmission_curve = transmission_curve
        self.resonance_markers = resonance_markers
        self.plot_title = plot_title
        self.x_label = x_label
        self.y_label = y_label
        self.coupling_info = coupling_info
        if hasattr(self, 'fsr_text'):
            self.fsr_arrow = fsr_arrow
    
    def final_summary(self):
        """Show final summary of ring resonator properties"""
        
        # Clear current view
        objects_to_remove = [
            self.axes, self.transmission_curve, self.resonance_markers,
            self.plot_title, self.x_label, self.y_label, self.schematic,
            self.coupling_info
        ]
        if hasattr(self, 'fsr_arrow'):
            objects_to_remove.append(self.fsr_arrow)
            objects_to_remove.append(self.fsr_text)
        
        self.play(*[FadeOut(obj) for obj in objects_to_remove])
        
        # Summary slide
        summary_title = Text("Ring Resonator Summary", font_size=36, color=YELLOW)
        summary_title.to_edge(UP)
        
        summary_points = VGroup(
            Text("Key Properties:", font_size=28, color=GREEN),
            MathTex(r"\bullet \text{ Resonance: } \lambda_m = \frac{n_{eff} L}{m}", font_size=26),
            MathTex(r"\bullet \text{ Free Spectral Range: } FSR = \frac{\lambda^2}{n_g L}", font_size=26),
            MathTex(r"\bullet \text{ Finesse: } \mathcal{F} = \frac{FSR}{\Delta\lambda_{FWHM}}", font_size=26),
            MathTex(r"\bullet \text{ Q-factor: } Q = \frac{\lambda}{\Delta\lambda_{FWHM}}", font_size=26),
            Text(" ", font_size=20),
            Text("Applications:", font_size=28, color=GREEN),
            Text("  - Optical filters & wavelength multiplexers", font_size=22),
            Text("  - Optical modulators & switches", font_size=22),
            Text("  - Biosensors & chemical sensors", font_size=22),
            Text("  - Optical delay lines", font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        summary_points.next_to(summary_title, DOWN, buff=0.5)
        
        self.play(Write(summary_title))
        self.play(Write(summary_points), run_time=4)
        
        self.wait(2)
        
        # Final fade out
        self.play(FadeOut(summary_title), FadeOut(summary_points))


class RingResonatorDetailed(Scene):
    """More detailed animation showing field buildup at resonance vs off-resonance"""
    
    def construct(self):
        title = Text("Ring Resonator: On vs Off Resonance", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Create two ring resonators side by side
        self.create_comparison()
        
    def create_comparison(self):
        """Compare on-resonance vs off-resonance behavior"""
        
        # On-resonance side
        on_res_title = Text("On Resonance", font_size=24, color=GREEN)
        on_res_title.shift(LEFT * 3.5 + UP * 2)
        
        on_ring = Circle(radius=1, color=BLUE, stroke_width=6)
        on_wg = Line(LEFT * 2, RIGHT * 2, color=BLUE, stroke_width=6)
        on_wg.shift(DOWN * 1.3)
        on_group = VGroup(on_ring, on_wg).shift(LEFT * 3.5)
        
        # Off-resonance side
        off_res_title = Text("Off Resonance", font_size=24, color=RED)
        off_res_title.shift(RIGHT * 3.5 + UP * 2)
        
        off_ring = Circle(radius=1, color=BLUE, stroke_width=6)
        off_wg = Line(LEFT * 2, RIGHT * 2, color=BLUE, stroke_width=6)
        off_wg.shift(DOWN * 1.3)
        off_group = VGroup(off_ring, off_wg).shift(RIGHT * 3.5)
        
        self.play(
            Write(on_res_title), Write(off_res_title),
            Create(on_group), Create(off_group),
            run_time=1.5
        )
        
        # Create intensity indicators (glowing rings)
        on_glow = Circle(radius=1, color=YELLOW, stroke_width=15, stroke_opacity=0.6)
        on_glow.move_to(on_ring.get_center())
        
        off_glow = Circle(radius=1, color=YELLOW, stroke_width=3, stroke_opacity=0.3)
        off_glow.move_to(off_ring.get_center())
        
        # Animate field buildup
        on_intensity_text = Text("High field buildup", font_size=18, color=YELLOW)
        on_intensity_text.next_to(on_ring, DOWN, buff=1.8)
        
        off_intensity_text = Text("Low field buildup", font_size=18, color=GRAY)
        off_intensity_text.next_to(off_ring, DOWN, buff=1.8)
        
        # Transmission indicators
        on_trans = Text("T ≈ 0 (at critical coupling)", font_size=16, color=RED)
        on_trans.next_to(on_intensity_text, DOWN, buff=0.2)
        
        off_trans = Text("T ≈ 1", font_size=16, color=GREEN)
        off_trans.next_to(off_intensity_text, DOWN, buff=0.2)
        
        self.play(
            Create(on_glow),
            Create(off_glow),
            run_time=1
        )
        
        # Pulsing animation for on-resonance
        self.play(
            on_glow.animate.set_stroke(width=25, opacity=0.8),
            Write(on_intensity_text),
            Write(off_intensity_text),
            run_time=1
        )
        
        self.play(
            on_glow.animate.set_stroke(width=15, opacity=0.6),
            run_time=0.5
        )
        
        # Multiple pulses to show buildup
        for _ in range(3):
            self.play(
                on_glow.animate.set_stroke(width=30, opacity=0.9),
                run_time=0.4
            )
            self.play(
                on_glow.animate.set_stroke(width=15, opacity=0.6),
                run_time=0.4
            )
        
        self.play(Write(on_trans), Write(off_trans))
        
        # Explanation
        explanation = VGroup(
            MathTex(r"\text{On resonance: } \phi = 2\pi m", font_size=24),
            MathTex(r"\text{Constructive interference in ring}", font_size=22),
            MathTex(r"\text{Destructive interference at output}", font_size=22),
        ).arrange(DOWN, buff=0.2)
        explanation.to_edge(DOWN)
        
        self.play(Write(explanation), run_time=2)
        
        self.wait(2)


# Run with: manim -pql ring_resonator.py RingResonatorAnimation
# For higher quality: manim -pqh ring_resonator.py RingResonatorAnimation
