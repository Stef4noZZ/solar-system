import os
import unittest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame

from solar_system.app import (
    ASTEROID_BELT,
    BODY_NAMES,
    MOONS,
    PLANETS,
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

        for selection in selections:
            with self.subTest(selection=selection):
                self.app._select(selection)
                self.app._draw()
                self.assertEqual(self.app.selected, selection)

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
        details_top = 140 + len(BODY_NAMES) * 20 + 6

        for language in ("en", "el"):
            self.app.language = language
            for index, planet in enumerate(PLANETS):
                with self.subTest(language=language, planet=planet.name):
                    self.app._select(index)
                    rendered_lines: list[tuple[int, int, int, int]] = []

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
        self.app.phases[0] = 1.234
        self.app._select(4)
        self.app.camera_focus_x = 120.0
        self.app.camera_focus_y = -45.0
        self.app.camera_zoom = 2.7
        self.app._toggle_tour()

        self.app._reset()

        self.assertEqual(self.app.speed, 1.0)
        self.assertEqual(self.app.zoom, 1.0)
        self.assertFalse(self.app.focus_mode)
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
