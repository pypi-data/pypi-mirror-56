# flake8: noqa
import unittest
import numpy as np
import matplotlib.pyplot as plt

from modelbase.ode import Model, Simulator


class SimulatorSetupTests(unittest.TestCase):
    """Description"""

    def test_get_full_concentration_dict(self):
        m = Model()
        m.add_compounds(["x"])
        m.add_algebraic_module("am", lambda p, x: [x + 1], ["x"], ["A"])
        self.assertEqual(m.get_full_concentration_dict([1]), {"x": 1, "A": 2})

    def test_get_full_concentration_dict_two_der_vars(self):
        m = Model()
        m.add_compounds(["x"])
        m.add_algebraic_module("am", lambda p, x: [x + 1, x + 2], ["x"], ["A", "B"])
        self.assertEqual(m.get_full_concentration_dict([1]), {"x": 1, "A": 2, "B": 3})

    def test_get_full_concentration_dict_two_vars_two_der_vars(self):
        m = Model()
        m.add_compounds(["x", "y"])
        m.add_algebraic_module(
            "am", lambda p, x, y: [x + 1, y + 1], ["x", "y"], ["A", "B"]
        )
        self.assertEqual(
            m.get_full_concentration_dict([1, 2]), {"x": 1, "y": 2, "A": 2, "B": 3}
        )

    def test_get_full_concentration_dict_two_vars_two_der_vars_two_time_points(self):
        m = Model()
        m.add_compounds(["x", "y"])
        m.add_algebraic_module(
            "am", lambda p, x, y: [x + 1, y + 1], ["x", "y"], ["A", "B"]
        )

        C = m.get_full_concentration_dict(np.array([[1, 2], [2, 4]]))
        C_sol = {
            "x": np.array([1, 2]),
            "y": np.array([2, 4]),
            "A": np.array([2, 3]),
            "B": np.array([3, 5]),
        }
        self.assertTrue(
            np.sum(
                (C["x"] + C["y"] + C["A"] + C["B"])
                - (C_sol["x"] + C_sol["y"] + C_sol["A"] + C_sol["B"])
            )
            == 0
        )

    # Get right hand side
    def test_get_rhs(self):
        m = Model()
        m.add_compounds(["x", "y"])
        m.add_algebraic_module(
            "am", lambda p, x, y: [x * 2, y * 2], ["x", "y"], ["A", "B"]
        )
        m.add_reaction("v1", lambda p, x: x, {"x": 1}, ["A"])
        m.add_reaction("v2", lambda p, y: y, {"y": 1}, ["B"])
        self.assertEqual(np.sum(m._get_rhs(0, [1, 2])), 6)


class SimulationAssimuloTests(unittest.TestCase):
    def test_simulation(self):
        m = Model()
        m.add_compounds(["x"])
        m.add_reaction("v1", lambda p, x: 1 * x, {"x": 1}, ["x"])

        s = Simulator(m)
        s.set_initial_conditions([1])
        t, y = s.simulate(10)
        self.assertTrue(np.isclose(y[-1][0], np.exp(10)))

    def test_simulation_steps(self):
        m = Model()
        m.add_compounds(["x"])
        m.add_reaction("v1", lambda p, x: 1 * x, {"x": 1}, ["x"])
        s = Simulator(m)
        s.set_initial_conditions([1])
        t, y = s.simulate(10, 10)
        self.assertTrue(np.isclose(y, np.exp(range(11)).reshape(-1, 1)).all())

    def test_simulation_time_points_range(self):
        m = Model()
        m.add_compounds(["x"])
        m.add_reaction("v1", lambda p, x: 1 * x, {"x": 1}, ["x"])
        s = Simulator(m)
        s.set_initial_conditions([1])
        t, y = s.simulate(10, None, range(11))
        self.assertTrue(np.isclose(y, np.exp(range(11)).reshape(-1, 1)).all())

    def test_simulation_time_points_list(self):
        m = Model()
        m.add_compounds(["x"])
        m.add_reaction("v1", lambda p, x: 1 * x, {"x": 1}, ["x"])
        s = Simulator(m)
        s.set_initial_conditions([1])
        t, y = s.simulate(10, None, list(range(11)))
        self.assertTrue(np.isclose(y, np.exp(range(11)).reshape(-1, 1)).all())

    def test_simulation_time_points_array(self):
        m = Model()
        m.add_compounds(["x"])
        m.add_reaction("v1", lambda p, x: 1 * x, {"x": 1}, ["x"])
        s = Simulator(m)
        s.set_initial_conditions([1])
        t, y = s.simulate(10, None, np.arange(0, 11))
        self.assertTrue(np.isclose(y, np.exp(range(11)).reshape(-1, 1)).all())

    def test_simulation_time_points_array_without_t_end(self):
        m = Model()
        m.add_compounds(["x"])
        m.add_reaction("v1", lambda p, x: 1 * x, {"x": 1}, ["x"])
        s = Simulator(m)
        s.set_initial_conditions([1])
        t, y = s.simulate(None, None, np.arange(0, 11))
        self.assertTrue(np.isclose(y, np.exp(range(11)).reshape(-1, 1)).all())

    def test_simulation_without_t_end(self):
        m = Model()
        m.add_compounds(["x"])
        m.add_reaction("v1", lambda p, x: 1 * x, {"x": 1}, ["x"])
        s = Simulator(m)
        s.set_initial_conditions([1])
        with self.assertRaises(TypeError):
            t, y = s.simulate()

    def test_continuous_simulation(self):
        m = Model()
        m.add_compounds(["x"])
        m.add_reaction("v1", lambda p, x: 1 * x, {"x": 1}, ["x"])

        s = Simulator(m)
        s.set_initial_conditions([1])
        s.simulate(5)
        s.simulate(10)
        t, y = s.get_results()
        self.assertEqual(t[0], 0.0)
        self.assertEqual(t[-1], 10.0)
        self.assertTrue(np.isclose(y[-1][0], np.exp(10)))


class SimulationScipyTests(unittest.TestCase):
    def test_simulation(self):
        m = Model()
        m.add_compounds(["x"])
        m.add_reaction("v1", lambda p, x: 1 * x, {"x": 1}, ["x"])
        s = Simulator(m, "scipy")
        s.set_initial_conditions([1])
        t, y = s.simulate(10)
        self.assertTrue(np.isclose(y[-1][0], np.exp(10)))

    def test_simulation_steps(self):
        m = Model()
        m.add_compounds(["x"])
        m.add_reaction("v1", lambda p, x: 1 * x, {"x": 1}, ["x"])
        s = Simulator(m, "scipy")
        s.set_initial_conditions([1])
        t, y = s.simulate(10, 10)
        self.assertTrue(np.isclose(y, np.exp(range(11)).reshape(-1, 1)).all())

    def test_simulation_time_points_range(self):
        m = Model()
        m.add_compounds(["x"])
        m.add_reaction("v1", lambda p, x: 1 * x, {"x": 1}, ["x"])
        s = Simulator(m, "scipy")
        s.set_initial_conditions([1])
        t, y = s.simulate(10, None, range(11))
        self.assertTrue(np.isclose(y, np.exp(range(11)).reshape(-1, 1)).all())

    def test_simulation_time_points_list(self):
        m = Model()
        m.add_compounds(["x"])
        m.add_reaction("v1", lambda p, x: 1 * x, {"x": 1}, ["x"])
        s = Simulator(m, "scipy")
        s.set_initial_conditions([1])
        t, y = s.simulate(10, None, list(range(11)))
        self.assertTrue(np.isclose(y, np.exp(range(11)).reshape(-1, 1)).all())

    def test_simulation_time_points_array(self):
        m = Model()
        m.add_compounds(["x"])
        m.add_reaction("v1", lambda p, x: 1 * x, {"x": 1}, ["x"])
        s = Simulator(m, "scipy")
        s.set_initial_conditions([1])
        t, y = s.simulate(10, None, np.arange(0, 11))
        self.assertTrue(np.isclose(y, np.exp(range(11)).reshape(-1, 1)).all())

    def test_simulation_time_points_array_without_t_end(self):
        m = Model()
        m.add_compounds(["x"])
        m.add_reaction("v1", lambda p, x: 1 * x, {"x": 1}, ["x"])
        s = Simulator(m, "scipy")
        s.set_initial_conditions([1])
        t, y = s.simulate(None, None, np.arange(0, 11))
        self.assertTrue(np.isclose(y, np.exp(range(11)).reshape(-1, 1)).all())

    def test_simulation_without_t_end(self):
        m = Model()
        m.add_compounds(["x"])
        m.add_reaction("v1", lambda p, x: 1 * x, {"x": 1}, ["x"])
        s = Simulator(m, "scipy")
        s.set_initial_conditions([1])
        with self.assertRaises(TypeError):
            t, y = s.simulate()

    def test_continuous_simulation(self):
        m = Model()
        m.add_compounds(["x"])
        m.add_reaction("v1", lambda p, x: 1 * x, {"x": 1}, ["x"])
        s = Simulator(m, "scipy")
        s.set_initial_conditions([1])
        s.simulate(5)
        s.simulate(10)
        t, y = s.get_results()
        self.assertEqual(t[0], 0.0)
        self.assertEqual(t[-1], 10.0)
        self.assertTrue(np.isclose(y[-1][0], np.exp(10)))


class SimulationExtraFunctionsTest(unittest.TestCase):
    def test_parameter_scan(self):
        m = Model({"p1": 1})
        m.add_compounds(["x"])
        m.add_reaction("v1", lambda p: p.p1, {"x": 1})
        s = Simulator(m)
        s.set_initial_conditions([0])
        self.assertTrue(
            all(
                np.isclose(
                    s.parameter_scan("p1", [1, 2, 3], 10).values[:, 0], [10, 20, 30]
                )
            )
        )


class PlottingTests(unittest.TestCase):
    def test_plots(self):
        def fast_eq(p, y):
            x = y / (1 + p.K)
            y = y * p.K / (1 + p.K)
            return x, y

        def v0(p):
            return p.v0

        def v2(p, y):
            return p.k2 * y

        m = Model({"v0": 1, "k2": 0.1, "K": 5})
        m.add_compounds(["A"])
        m.add_algebraic_module("fast_eq", fast_eq, ["A"], ["X", "Y"])
        m.add_reaction("v0", v0, {"A": 1})
        m.add_reaction("v2", v2, {"A": -1}, ["Y"])

        s = Simulator(m)
        s.set_initial_conditions({"A": 0})
        s.simulate(100)

        # Standard plot
        fig, ax = s.plot()
        plt.close(fig)

        # All plot
        fig, ax = s.plot_all()
        plt.close(fig)

        # fluxes
        fig, ax = s.plot_fluxes()
        plt.close(fig)

        # against variable
        fig, ax = s.plot_against_variable("A")
        plt.close(fig)


if __name__ == "__main__":
    unittest.main()
