# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['dokusan']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dokusan',
    'version': '0.1.0a0',
    'description': 'Sudoku solver with step-by-step guidance',
    'long_description': '========\nOverview\n========\n\nSudoku solver with step-by-step guidance\n\nThis lib is currently in pre-alpha phase,\nbut already can solve some simple and medium level sudoku.\n\nThe following code displays all steps leading to solution:\n\n.. code-block:: python\n\n    from dokusan import entities, techniques\n\n\n    def list_steps(sudoku: entities.Sudoku):\n        all_techniques = (\n            techniques.LoneSingle,\n            techniques.HiddenSingle,\n            techniques.NakedPair,\n            techniques.NakedTriplet,\n            techniques.Omission,\n            techniques.XYWing,\n            techniques.UniqueRectangle,\n        )\n        i = 1\n        while not sudoku.is_solved() and i == 1:\n            i = 0\n            for technique in all_techniques:\n                try:\n                    result = technique(sudoku).first()\n                except techniques.NotFound as exc:\n                    continue\n                else:\n                    sudoku.update_cells(result.changed_cells)\n                    yield result\n                    i = 1\n                    break\n\n    _ = 0\n\n    sudoku = entities.Sudoku([\n        [_, _, _, _, 9, _, 1, _, _],\n        [_, _, _, _, _, 2, 3, _, _],\n        [_, _, 7, _, _, 1, 8, 2, 5],\n        [6, _, 4, _, 3, 8, 9, _, _],\n        [8, 1, _, _, _, _, _, _, _],\n        [_, _, 9, _, _, _, _, _, 8],\n        [1, 7, _, _, _, _, 6, _, _],\n        [9, _, _, _, 1, _, 7, 4, 3],\n        [4, _, 3, _, 6, _, _, _, 1],\n    ])\n\n    for step in list_steps(sudoku):\n        print(step.combination)\n',
    'author': 'Aleksei Maslakov',
    'author_email': 'lesha.maslakov@gmail.com',
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
