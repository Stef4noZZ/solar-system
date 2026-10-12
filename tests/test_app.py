import math
import os
import unittest
from unittest.mock import patch

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame

from solar_system.app import (
    ASTEROID_BELT,
    EARTH_YEAR_DAYS,
    MOONS,
    PLANETS,
    SMALL_BODIES,
    SIMULATION_TIME_SCALES,
    TOUR_FACTS,
    SolarSystemApp,
)


class SolarSystemAppTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        pygame.init()

    @classmethod
    def tearDownClass(cls) -> None:
        pygame.quit()

    def setUp(self) -> None:
        self.app = SolarSystemApp()

    def tearDown(self) -> None:
        pygame.display.quit()
        pygame.font.quit()

    def test_all_bodies_can_be_selected_and_drawn(self) -> None:
        selections = [None, *range(len(PLANETS)), ASTEROID_BELT]
        selections.extend(moon.identifier for moon in MOONS)
        selections.extend(body.identifier for body in SMALL_BODIES)

        for selection in selections:
            with self.subTest(selection=selection):
                self.app._select(selection)
                self.app._draw()
                self.assertEqual(self.app.selected, selection)

    def test_sidebar_categories_filter_and_select_bodies(self) -> None:
        self.app._draw()
        categories = {
            category: rect for rect, category in self.app.category_rects
        }

        self.app._handle_click(categories["moons"].center)
        self.app._draw()
        moon_entries = {
            entry for _, entry in self.app.list_rects
            if isinstance(entry, str)
        }
        self.assertEqual(moon_entries, {moon.identifier for moon in MOONS})

        current_moon_category = next(
            rect
            for rect, category in self.app.category_rects
            if category == "moons"
        )
        self.app._handle_click(current_moon_category.center)
        self.assertEqual(self.app.sidebar_category, None)
        self.app._draw()
        small_bodies_rect = next(
            rect
            for rect, category in self.app.category_rects
            if category == "small_bodies"
        )
        self.app._handle_click(small_bodies_rect.center)
        self.app._draw()
        self.assertEqual(
            [entry for _, entry in self.app.list_rects],
            ["ceres", "pluto", "halley", ASTEROID_BELT],
        )
        self.app._handle_click(self.app.list_rects[1][0].center)
        self.assertEqual(self.app.selected, "pluto")
        self.assertEqual(self.app.sidebar_category, "small_bodies")
        self.app._draw()
        self.app._handle_click(self.app.list_rects[-1][0].center)
        self.assertEqual(self.app.selected, ASTEROID_BELT)
        self.assertEqual(self.app.sidebar_category, "small_bodies")

    def test_small_bodies_use_approximate_periods_on_clean_circular_paths(self) -> None:
        halley = next(body for body in SMALL_BODIES if body.identifier == "halley")
        self.app.time_scale_index = 2
        initial_anomaly = self.app.small_body_mean_anomalies["halley"]

        self.app._advance_orbits(1.0)

        expected_anomaly = (
            initial_anomaly
            + math.tau * EARTH_YEAR_DAYS / halley.orbital_period_days
        ) % math.tau
        self.assertAlmostEqual(
            self.app.small_body_mean_anomalies["halley"],
            expected_anomaly,
        )
        for mean_anomaly in (0.0, math.pi / 2, math.pi, math.tau - 0.1):
            position = self.app._small_body_position(halley, mean_anomaly)
            self.assertAlmostEqual(math.hypot(*position), halley.orbit_radius)

    def test_sun_glow_leaves_clearance_inside_mercurys_orbit(self) -> None:
        for width, height in ((900, 700), (1280, 800), (1600, 1000)):
            self.app._layout((width, height))
            scene_scale = (
                min(self.app.scene_rect.size) * 0.43 / 318
            )
            for zoom in (1.0, 2.2, 3.2):
                scale = scene_scale * zoom
                mercury_radius = max(
                    4,
                    round(PLANETS[0].radius * max(scale, 0.72)),
                )
                glow_radius = self.app._sun_glow_radius(scale, mercury_radius)
                clearance = (
                    PLANETS[0].orbit_radius * scale
                    - mercury_radius
                    - glow_radius
                )
                with self.subTest(size=(width, height), zoom=zoom):
                    self.assertGreaterEqual(clearance, 8)

    def test_small_body_details_are_available_in_both_languages(self) -> None:
        self.app._select("pluto")
        english_facts = self.app._facts_for_selection()
        self.assertTrue(any("Dwarf planet" in fact for fact in english_facts))
        self.assertTrue(any("248 Earth years" in fact for fact in english_facts))

        self.app._toggle_language()
        greek_facts = self.app._facts_for_selection()
        self.assertTrue(any("Νάνος πλανήτης" in fact for fact in greek_facts))
        self.assertTrue(any("248 γήινα έτη" in fact for fact in greek_facts))
        self.assertTrue(any("0,249" in fact for fact in greek_facts))

    def test_category_visibility_toggles_hide_scene_objects_without_removing_menu(self) -> None:
        self.app._select(4)
        self.app._draw()
        self.assertTrue(any(index == "io" for _, _, _, index in self.app.hit_targets))

        moon_category = next(
            rect for rect, category in self.app.category_rects
            if category == "moons"
        )
        self.app._handle_click(moon_category.center)
        self.app._draw()
        visibility = {
            category: rect for rect, category in self.app.visibility_rects
        }
        self.app._handle_click(visibility["moons"].center)
        self.app._draw()
        self.assertFalse(self.app.show_moons)
        self.assertEqual(self.app.sidebar_category, "moons")
        self.assertFalse(any(index in {moon.identifier for moon in MOONS}
                             for _, _, _, index in self.app.hit_targets))
        self.assertTrue(any(entry == "io" for _, entry in self.app.list_rects))

        visibility = {
            category: rect for rect, category in self.app.visibility_rects
        }
        self.app._handle_click(visibility["small_bodies"].center)
        self.app._draw()
        self.assertFalse(self.app.show_small_bodies)
        self.assertEqual(self.app.sidebar_category, "moons")
        self.assertFalse(any(index in {body.identifier for body in SMALL_BODIES}
                             for _, _, _, index in self.app.hit_targets))
        self.assertEqual(self.app.asteroid_belt_hit_area, (0.0, 0.0, 0.0, 0.0))

        small_body_category = next(
            rect for rect, category in self.app.category_rects
            if category == "small_bodies"
        )
        self.app._handle_click(small_body_category.center)
        self.app._draw()
        self.assertTrue(any(entry == "pluto" for _, entry in self.app.list_rects))

    def test_jason_mission_uses_simulation_time_and_can_pause_resume_reset(self) -> None:
        self.app._draw()
        mission_category = next(
            rect
            for rect, category in self.app.category_rects
            if category == "mission"
        )
        self.app._handle_click(mission_category.center)
        self.app._draw()
        self.assertIn("toggle", self.app.mission_control_rects)

        self.app.phases[3] = (
            self.app.phases[2] + self.app._mission_required_phase()
        ) % math.tau
        self.app._handle_click(self.app.mission_control_rects["toggle"].center)
        self.assertTrue(self.app.mission_started)
        self.assertTrue(self.app.mission_active)
        self.assertTrue(self.app.mission_launched)
        self.assertAlmostEqual(self.app.mission_launch_wait_days, 0.0)
        self.assertEqual(self.app._mission_progress(), 0.0)
        self.assertEqual(self.app._mission_stage(), "Departure")
        start_earth_phase = self.app.mission_earth_phase
        start_mars_arrival_phase = self.app.mission_mars_arrival_phase
        route = self.app._mission_route_points(0.0, 0.0, 1.0)
        self.assertEqual(len(route), 41)
        self.assertNotEqual(route[0], route[-1])
        self.assertEqual(self.app.mission_earth_phase, start_earth_phase)
        self.assertEqual(self.app.mission_mars_arrival_phase, start_mars_arrival_phase)

        self.app.time_scale_index = 1
        self.app._advance_orbits(2.0)
        self.assertEqual(self.app.mission_elapsed_days, 60.0)
        self.assertAlmostEqual(
            self.app._mission_progress(),
            60 / self.app._mission_transfer_days(),
        )
        self.assertEqual(self.app._mission_stage(), "Cruise")
        self.app._draw()
        self.app._handle_click(self.app.mission_control_rects["toggle"].center)
        self.assertFalse(self.app.mission_active)
        self.app._advance_orbits(1.0)
        self.assertEqual(self.app.mission_elapsed_days, 60.0)

        self.app._draw()
        self.app._handle_click(self.app.mission_control_rects["toggle"].center)
        self.assertTrue(self.app.mission_active)
        self.app._advance_orbits(7.0)
        self.assertAlmostEqual(
            self.app.mission_elapsed_days,
            self.app._mission_transfer_days(),
        )
        self.assertFalse(self.app.mission_active)
        self.assertEqual(self.app._mission_progress(), 1.0)
        self.assertEqual(self.app._mission_stage(), "Mission complete")
        self.app._draw()
        self.assertEqual(self.app._tr("Mission complete"), "Mission complete")

        self.app._handle_click(self.app.mission_control_rects["reset"].center)
        self.assertFalse(self.app.mission_started)
        self.assertEqual(self.app.mission_elapsed_days, 0.0)
        self.assertFalse(self.app.mission_launched)

    def test_hohmann_mission_waits_for_launch_window_and_predicts_arrival(self) -> None:
        transfer_days = self.app._mission_transfer_days()
        self.assertAlmostEqual(transfer_days, 259.0, delta=1.0)
        self.assertAlmostEqual(
            self.app._mission_required_phase_degrees(),
            44.0,
            delta=1.0,
        )
        wait_days = self.app._mission_days_to_launch_window()
        self.assertGreater(wait_days, 0.0)

        earth_phase_now = self.app.phases[2]
        mars_phase_now = self.app.phases[3]
        self.app._toggle_mission()

        self.assertFalse(self.app.mission_launched)
        self.assertEqual(self.app._mission_stage(), "Waiting for launch window")
        self.assertAlmostEqual(self.app.mission_launch_wait_days, wait_days)
        earth_phase_at_launch = (
            earth_phase_now
            + math.tau * wait_days / PLANETS[2].orbital_period_days
        ) % math.tau
        mars_phase_at_arrival = (
            mars_phase_now
            + math.tau
            * (wait_days + transfer_days)
            / PLANETS[3].orbital_period_days
        ) % math.tau
        self.assertAlmostEqual(
            (mars_phase_at_arrival - earth_phase_at_launch) % math.tau,
            math.pi,
            places=7,
        )

        self.app._advance_mission(wait_days - 1)
        self.assertFalse(self.app.mission_launched)
        self.assertAlmostEqual(self.app.mission_launch_wait_days, 1.0)
        self.app._advance_mission(1.0)
        self.assertTrue(self.app.mission_launched)
        self.assertEqual(self.app.mission_elapsed_days, 0.0)
        self.assertEqual(self.app._mission_stage(), "Departure")

    def test_hohmann_route_starts_and_ends_on_planet_orbits(self) -> None:
        self.app.mission_earth_phase = 0.4
        route = self.app._mission_route_points(400, 300, 1.0)

        self.assertEqual(len(route), 41)
        self.assertAlmostEqual(
            math.dist(route[0], (400, 300)),
            PLANETS[2].orbit_radius,
            delta=1.0,
        )
        self.assertAlmostEqual(
            math.dist(route[-1], (400, 300)),
            PLANETS[3].orbit_radius,
            delta=1.0,
        )
        self.assertGreater(
            math.dist(route[20], (400, 300)),
            math.dist(route[0], (400, 300)),
        )

    def test_mission_alignment_gap_and_target_marker_follow_planet_phases(self) -> None:
        required_phase = self.app._mission_required_phase()
        self.app.phases[2] = 0.7
        self.app.phases[3] = (self.app.phases[2] + required_phase + math.radians(12)) % math.tau
        self.assertAlmostEqual(self.app._mission_alignment_gap_degrees(), 12.0)

        surface = pygame.Surface((800, 600))
        target_position = self.app._mission_alignment_target_position(
            400, 300, 1.0
        )
        with patch("pygame.draw.circle", wraps=pygame.draw.circle) as draw_circle:
            self.app._draw_mission_alignment(surface, 400, 300, 1.0)

        self.assertTrue(
            any(
                call.args[1] == (255, 196, 112)
                and call.args[2] == target_position
                for call in draw_circle.call_args_list
            )
        )

        self.app.phases[3] = (
            self.app.phases[2] + required_phase
        ) % math.tau
        self.assertAlmostEqual(self.app._mission_alignment_gap_degrees(), 0.0)

    def test_argo_disappears_on_arrival_and_arrival_is_shown(self) -> None:
        self.app.sidebar_category = "mission"
        self.app.mission_started = True
        self.app.mission_launched = True
        self.app.mission_elapsed_days = self.app._mission_transfer_days()
        self.app.mission_active = False

        rendered_text: list[str] = []
        original_draw_text = self.app._draw_text

        def capture_text(
            text: str,
            position: tuple[int, int],
            color: tuple[int, int, int] = (232, 240, 251),
            font: pygame.font.Font | None = None,
        ) -> None:
            rendered_text.append(text)
            original_draw_text(text, position, color, font)

        self.app._draw_text = capture_text
        with patch("pygame.draw.polygon", wraps=pygame.draw.polygon) as draw_polygon:
            self.app._draw()
        self.app._draw_text = original_draw_text

        self.assertEqual(draw_polygon.call_count, 0)
        self.assertIn("Argo has reached Mars orbit", rendered_text)
        self.assertEqual(self.app._mission_stage(), "Mission complete")

    def test_mission_orbit_overlays_follow_orbits_toggle(self) -> None:
        self.app.sidebar_category = "mission"
        self.app.mission_started = True

        with patch.object(
            self.app,
            "_draw_mission_alignment",
            wraps=self.app._draw_mission_alignment,
        ) as draw_alignment:
            self.app.show_orbits = False
            self.app._draw()
            draw_alignment.assert_not_called()

            self.app.show_orbits = True
            self.app._draw()
            draw_alignment.assert_called_once()

        self.app.mission_launched = True
        self.app.mission_elapsed_days = 60.0
        with (
            patch("pygame.draw.lines", wraps=pygame.draw.lines) as draw_lines,
            patch("pygame.draw.polygon", wraps=pygame.draw.polygon) as draw_ship,
        ):
            self.app.show_orbits = False
            self.app._draw()
            draw_lines.assert_not_called()
            self.assertEqual(draw_ship.call_count, 1)

            self.app.show_orbits = True
            self.app._draw()
            self.assertGreater(draw_lines.call_count, 0)
            self.assertEqual(draw_ship.call_count, 2)

        self.app.mission_elapsed_days = self.app._mission_transfer_days()
        with patch(
            "pygame.draw.ellipse", wraps=pygame.draw.ellipse
        ) as draw_ellipse:
            self.app.show_orbits = False
            self.app._draw()
            self.assertFalse(
                any(
                    call.args[1] == (61, 121, 165)
                    for call in draw_ellipse.call_args_list
                )
            )

            self.app.show_orbits = True
            self.app._draw()
            self.assertTrue(
                any(
                    call.args[1] == (61, 121, 165)
                    for call in draw_ellipse.call_args_list
                )
            )

    def test_mission_stage_and_progress_are_localized(self) -> None:
        self.app.mission_started = True
        self.app.mission_launched = True
        self.app.mission_elapsed_days = 230.0
        self.assertEqual(self.app._mission_stage(), "Mars approach")
        self.assertAlmostEqual(
            self.app._mission_progress(),
            230 / self.app._mission_transfer_days(),
        )

        self.app.language = "el"
        self.assertEqual(self.app._tr(self.app._mission_stage()), "Προσέγγιση Άρη")
        self.assertEqual(
            self.app._tr("Waiting for launch window"),
            "Αναμονή παραθύρου εκτόξευσης",
        )
        self.assertEqual(
            self.app._tr("Mars ~{angle}° ahead").format(angle=44),
            "Άρης ~44° μπροστά",
        )
        self.assertEqual(
            self.app._tr("Argo has reached Mars orbit"),
            "Η Αργώ έφτασε σε τροχιά γύρω από τον Άρη",
        )

    def test_mission_visibility_hides_route_and_controls(self) -> None:
        self.app._draw()
        mission_visibility = next(
            rect
            for rect, category in self.app.visibility_rects
            if category == "mission"
        )
        self.app._handle_click(mission_visibility.center)
        self.assertFalse(self.app.show_mission)

        self.app.sidebar_category = "mission"
        self.app.mission_started = True
        self.app.mission_active = True
        self.app.mission_launched = True
        self.app._advance_orbits(1.0)
        self.assertEqual(self.app.mission_elapsed_days, 1.0)
        with patch("pygame.draw.lines", wraps=pygame.draw.lines) as draw_lines:
            self.app._draw()
            self.assertEqual(draw_lines.call_count, 0)
            self.assertFalse(self.app.mission_control_rects)

            mission_visibility = next(
                rect
                for rect, category in self.app.visibility_rects
                if category == "mission"
            )
            self.app._handle_click(mission_visibility.center)
            self.app._draw()
            self.assertTrue(self.app.show_mission)
            self.assertIn("toggle", self.app.mission_control_rects)
            self.assertGreater(draw_lines.call_count, 0)

    def test_mission_controls_fit_minimum_sidebar_in_both_languages(self) -> None:
        self.app._layout((900, 700))
        self.app.sidebar_category = "mission"
        original_draw_text = self.app._draw_text
        for language in ("en", "el"):
            with self.subTest(language=language):
                self.app.language = language
                rendered_lines: list[tuple[str, int, int]] = []

                def capture_text(
                    text: str,
                    position: tuple[int, int],
                    color: tuple[int, int, int] = (232, 240, 251),
                    font: pygame.font.Font | None = None,
                ) -> None:
                    selected_font = font or self.app.font
                    if (
                        76 <= position[1] < self.app.sidebar_rect.bottom
                        and position[0] < self.app.sidebar_rect.right
                    ):
                        rendered_lines.append(
                            (
                                text,
                                position[0],
                                selected_font.size(self.app._tr(text))[0],
                            )
                        )
                    original_draw_text(text, position, color, font)

                self.app._draw_text = capture_text
                self.app._draw()
                self.app._draw_text = original_draw_text
                for text, x, width in rendered_lines:
                    self.assertLessEqual(
                        x + width,
                        self.app.sidebar_rect.right - 12,
                        f"{text!r} exceeds sidebar in {language}",
                    )
                for label in (
                    "Schedule mission",
                    "Pause mission",
                    "Resume mission",
                    "Reset mission",
                ):
                    self.assertLessEqual(
                        self.app.tiny_font.size(self.app._tr(label))[0] + 8,
                        max(rect.width for rect in self.app.mission_control_rects.values()),
                        f"{label} does not fit in {language}",
                    )
                for rect in self.app.mission_control_rects.values():
                    self.assertTrue(self.app.sidebar_rect.contains(rect))

    def test_selecting_moon_opens_grouped_moons_category(self) -> None:
        self.app._select("europa")
        self.app._draw()

        self.assertEqual(self.app.sidebar_category, "moons")
        self.assertEqual(
            [entry for _, entry in self.app.list_rects],
            ["moon", "io", "europa", "ganymede", "callisto", "titan"],
        )

    def test_language_switch_preserves_selection_and_can_be_reversed(self) -> None:
        self.app._select("europa")
        self.app._toggle_language()
        self.assertEqual(self.app.language, "el")
        self.assertEqual(self.app.selected, "europa")
        self.assertEqual(self.app._tr("Europa"), "Ευρώπη")

        self.app._toggle_language()
        self.assertEqual(self.app.language, "en")
        self.assertEqual(self.app._tr("Europa"), "Europa")

    def test_sun_is_named_in_scene_and_introduced_in_guided_tour(self) -> None:
        self.app._select(None)
        self.assertEqual(self.app._tr("The Sun"), "The Sun")
        self.app._draw()

        self.app._toggle_tour()
        self.assertIsNone(self.app.selected)
        self.assertIn("Sun", TOUR_FACTS[self.app.tour_index])
        self.app.language = "el"
        self.assertIn("Ήλιος", self.app._tr(TOUR_FACTS[self.app.tour_index]))

    def test_time_scale_cycles_from_day_to_month_to_year(self) -> None:
        self.assertEqual(self.app.time_scale_index, 0)
        time_button = self.app.buttons["time_scale"]

        for expected_index in (1, 2, 0):
            self.app._handle_click(time_button.center)
            self.assertEqual(self.app.time_scale_index, expected_index)

        self.app._handle_key(pygame.K_t)
        self.assertEqual(self.app.time_scale_index, 1)

    def test_realistic_periods_preserve_earth_moon_orbit_ratio(self) -> None:
        self.app.time_scale_index = 2
        initial_earth_phase = self.app.phases[2]
        self.app._advance_orbits(1.0)

        self.assertAlmostEqual(
            self.app.phases[2],
            initial_earth_phase,
            places=10,
        )
        expected_moon_phase = (
            math.tau * EARTH_YEAR_DAYS / MOONS[0].orbital_period_days
        ) % math.tau
        self.assertAlmostEqual(
            self.app.moon_phases["moon"],
            expected_moon_phase,
            places=10,
        )
        self.assertAlmostEqual(
            EARTH_YEAR_DAYS / MOONS[0].orbital_period_days,
            13.37,
            places=2,
        )

    def test_time_scale_button_fits_header_in_both_languages(self) -> None:
        self.app._layout((900, 700))
        time_button = self.app.buttons["time_scale"]
        self.assertFalse(
            time_button.colliderect(self.app.buttons["language"])
        )

        for language in ("en", "el"):
            self.app.language = language
            for label, _ in SIMULATION_TIME_SCALES:
                with self.subTest(language=language, label=label):
                    self.assertLessEqual(
                        self.app.small_font.size(self.app._tr(label))[0],
                        time_button.width,
                    )
            speed_readout = f"{self.app.speed:.1f}× {self.app.speed * self.app._simulated_days_per_second():.4g}d/s"
            self.assertLessEqual(
                self.app.tiny_font.size(speed_readout)[0],
                90,
            )

    def test_bottom_speed_buttons_change_simulation_rate(self) -> None:
        initial_phase = self.app.phases[2]
        self.app._handle_click(self.app.buttons["faster"].center)
        self.assertEqual(self.app.speed, 1.2)
        self.app._advance_orbits(1.0)
        self.assertAlmostEqual(
            self.app.phases[2],
            (initial_phase + math.tau * 1.2 / EARTH_YEAR_DAYS)
            % math.tau,
        )

    def test_layout_has_no_overlapping_bottom_controls(self) -> None:
        control_keys = ("play", "reset", "orbits", "focus", "view", "slower", "faster")

        for size in ((1280, 800), (1024, 768), (960, 720), (900, 700)):
            with self.subTest(size=size):
                self.app._layout(size)
                self.app._draw()
                for index, first in enumerate(control_keys):
                    for second in control_keys[index + 1 :]:
                        self.assertFalse(
                            self.app.buttons[first].colliderect(
                                self.app.buttons[second]
                            ),
                            f"{first} overlaps {second} at {size}",
                        )

    def test_planet_cards_draw_in_minimum_layout_in_both_languages(self) -> None:
        self.app._layout((900, 700))

        for language in ("en", "el"):
            self.app.language = language
            for index in range(len(PLANETS)):
                with self.subTest(language=language, planet=PLANETS[index].name):
                    self.app._select(index)
                    self.app._draw()

    def test_planet_card_text_stays_inside_sidebar_at_minimum_size(self) -> None:
        self.app._layout((900, 700))
        original_draw_text = self.app._draw_text

        for language in ("en", "el"):
            self.app.language = language
            for index, planet in enumerate(PLANETS):
                with self.subTest(language=language, planet=planet.name):
                    self.app._select(index)
                    rendered_lines: list[tuple[int, int, int, int]] = []
                    self.app._draw()
                    details_top = self.app.sidebar_details_top

                    def capture_text(
                        text: str,
                        position: tuple[int, int],
                        color: tuple[int, int, int] = (232, 240, 251),
                        font: pygame.font.Font | None = None,
                    ) -> None:
                        selected_font = font or self.app.font
                        if details_top + 10 <= position[1] < self.app.sidebar_rect.bottom:
                            width = selected_font.size(self.app._tr(text))[0]
                            rendered_lines.append(
                                (
                                    position[0],
                                    position[1],
                                    width,
                                    selected_font.get_height(),
                                )
                            )
                        original_draw_text(text, position, color, font)

                    self.app._draw_text = capture_text
                    self.app._draw()
                    self.app._draw_text = original_draw_text

                    self.assertTrue(rendered_lines)
                    for x, y, width, height in rendered_lines:
                        self.assertLessEqual(
                            x + width,
                            self.app.sidebar_rect.right - 12,
                            f"card text exceeds sidebar width at {language}",
                        )
                        self.assertLessEqual(
                            y + height,
                            self.app.sidebar_rect.bottom - 6,
                            f"card text exceeds sidebar height at {language}",
                        )

    def test_reset_restores_simulation_defaults(self) -> None:
        self.app.speed = 3.8
        self.app.zoom = 3.6
        self.app.show_moons = False
        self.app.show_small_bodies = False
        self.app.phases[0] = 1.234
        self.app._select(4)
        self.app.camera_focus_x = 120.0
        self.app.camera_focus_y = -45.0
        self.app.camera_zoom = 2.7
        self.app._toggle_tour()

        self.app._reset()

        self.assertEqual(self.app.speed, 1.0)
        self.assertEqual(self.app.time_scale_index, 0)
        self.assertEqual(self.app.zoom, 1.0)
        self.assertFalse(self.app.focus_mode)
        self.assertTrue(self.app.show_moons)
        self.assertTrue(self.app.show_small_bodies)
        self.assertFalse(self.app.tour_active)
        self.assertEqual(self.app.tour_message, "Tour stopped")
        self.assertEqual(self.app.camera_focus_x, 0.0)
        self.assertEqual(self.app.camera_focus_y, 0.0)
        self.assertEqual(self.app.camera_zoom, 1.0)
        self.assertEqual(
            self.app.phases,
            [index * 0.73 for index in range(len(PLANETS))],
        )

    def test_planet_cards_include_orbital_year_in_both_languages(self) -> None:
        for index, planet in enumerate(PLANETS):
            with self.subTest(planet=planet.name):
                self.app._select(index)
                facts = self.app._facts_for_selection()
                self.assertTrue(
                    any(fact.startswith("Year:") for fact in facts)
                )
                self.app._toggle_language()
                localized_facts = self.app._facts_for_selection()
                self.assertTrue(
                    any(fact.startswith("Διάρκεια έτους:") for fact in localized_facts)
                )
                self.assertTrue(
                    any(self.app._tr(planet.year_length) in fact for fact in localized_facts)
                )
                self.app._toggle_language()

    def test_confirmed_moon_counts_match_documented_reference_snapshot(self) -> None:
        self.assertEqual(PLANETS[4].moons, "115")
        self.assertEqual(PLANETS[5].moons, "293")
        self.assertEqual(PLANETS[6].moons, "29")

    def test_guided_tour_completes(self) -> None:
        self.app._toggle_tour()
        self.assertTrue(self.app.tour_active)
        self.app.tour_index = len(TOUR_FACTS) - 1
        self.app._advance_tour()
        self.assertFalse(self.app.tour_active)
        self.assertEqual(self.app.tour_message, "Tour complete")

    def test_event_loop_exits_on_window_close(self) -> None:
        pygame.event.clear()
        pygame.event.post(pygame.event.Event(pygame.QUIT))

        self.app.run()

        self.assertFalse(self.app.running)


if __name__ == "__main__":
    unittest.main()
