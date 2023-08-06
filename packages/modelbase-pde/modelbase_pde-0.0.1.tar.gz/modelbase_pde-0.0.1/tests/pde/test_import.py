# flake8: noqa

import unittest


class DummyTests(unittest.TestCase):
    """Tests for compound methods"""

    def test_base_import(self):
        import modelbase.pde as pde

        self.assertTrue(True)

    def test_level1_import(self):
        import modelbase.pde.basemodels
        import modelbase.pde.leafmodels
        import modelbase.pde.utils

    def test_level2_import(self):
        import modelbase.pde.utils.coordinates
        import modelbase.pde.utils.perffuncs
        import modelbase.pde.utils.plotting

    def test_from_import(self):
        from modelbase.pde.basemodels import HexGridModel
        from modelbase.pde.leafmodels import HexLeafModel
