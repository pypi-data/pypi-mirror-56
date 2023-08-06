import unittest
from .monitor import parse_non_spoilers

INPUT1 = """
He's my favorite person on that ship. Well it goes **spoilers ahead** >!Amos, Alex, Bobby, Naomi, Holden, Peaches. But Amos, Alex and Gunny are nearly tied!<
"""
EXPECTED1 = """
He's my favorite person on that ship. Well it goes **spoilers ahead** 
"""

INPUT2 = """
It really is a funny scene, but I think that line is >!kind of sad in the context of his backstory, especially how old he was when he left Earth.!< There are no throw-away lines in this show, especially from Amos.
"""
EXPECTED2 = """
It really is a funny scene, but I think that line is  There are no throw-away lines in this show, especially from Amos.
"""

# Handle broken spoiler tags
INPUT3 = """
It really is a funny scene, but I think that line is >! kind of sad in the context of his backstory, especially how old he was when he left Earth.!< There are no throw-away lines in this show, especially from Amos.
"""
EXPECTED3 = """
It really is a funny scene, but I think that line is >! kind of sad in the context of his backstory, especially how old he was when he left Earth.!< There are no throw-away lines in this show, especially from Amos.
"""

INPUT4 = """
It really is a funny scene, but I think that line is >!kind of sad in the context of his backstory, especially how old he was when he left Earth. !< There are no throw-away lines in this show, especially from Amos.
"""
EXPECTED4 = """
It really is a funny scene, but I think that line is >!kind of sad in the context of his backstory, especially how old he was when he left Earth. !< There are no throw-away lines in this show, especially from Amos.
"""

INPUT5 = """
hi there >!SPoiler!< and another >!spoiler!< stuff
"""
EXPECTED5 = """
hi there  and another  stuff
"""

INPUT6 = """
All the following comes from the novels and novellas, so spoilers for those ahead.

>!Amos/Timothy grew up in a horrible part of Baltimore where virtually everyone was living on basic subsistence, and was himself completely undocumented.

He was the child of a low-rent prostitute, and got sent out to turn tricks himself by the pimp at around the age of six.

He encountered both traditional and sexual violence nearly every day of his life, and worked as a highly effective mob enforcer, where his emotional detachment only made him better at his job.

He was never a super-soldier, just an abnormally large and strong young man with few if any moral inhibitions. Extreme poverty, abuse, and daily mortal danger created Amos as we know him.!<
"""

# Reddit doesn't handle spoilers across new lines
EXPECTED6 = """
All the following comes from the novels and novellas, so spoilers for those ahead.

>!Amos/Timothy grew up in a horrible part of Baltimore where virtually everyone was living on basic subsistence, and was himself completely undocumented.

He was the child of a low-rent prostitute, and got sent out to turn tricks himself by the pimp at around the age of six.

He encountered both traditional and sexual violence nearly every day of his life, and worked as a highly effective mob enforcer, where his emotional detachment only made him better at his job.

He was never a super-soldier, just an abnormally large and strong young man with few if any moral inhibitions. Extreme poverty, abuse, and daily mortal danger created Amos as we know him.!<
"""

pairs = [
	(INPUT1, EXPECTED1),
	(INPUT2, EXPECTED2),
	(INPUT3, EXPECTED3),
	(INPUT4, EXPECTED4),
	(INPUT5, EXPECTED5),
	(INPUT6, EXPECTED6),
]

class TestStringMethods(unittest.TestCase):
	def test_parse(self):
		for index, value in enumerate(pairs):
			inputval, expected = [x.strip("\n") for x in value]
			self.assertEqual(expected.strip("\n"), parse_non_spoilers(inputval), "Incorrect Prase on test {}".format(index))
