# NLDSL (c) 2019 by Kevin Kiefer <abc.kiefer@gmail.com>, Heidelberg University
#
# NLDSL is licensed under a
# Creative Commons Attribution-NonCommercial 3.0 Unported License.
#
# You should have received a copy of the license along with this
# work.  If not, see <http://creativecommons.org/licenses/by-nc/3.0/>.

from setuptools import setup




LONG_DESC = "NLDSL is a tool to create domain specific languages (DSLs) for data science, \
which can be translated into executable code. A new DSL is created by deriving from \
the CodeGenerator class and rules are added to it via simple python functions. \
Besides providing code generation NLDSL allows the user to define DSL-level function, \
which are then treated as first-class rules. \
Currently we provide extensions for Pandas and PySpark."


setup(
    name="nldsl",
    version="0.14.0",
    url="https://gitlab.com/Einhornstyle/nldsl",
    project_urls={
        "Documentation": "https://einhornstyle.gitlab.io/nldsl/"
    },
    description="A DSL for data science with a syntax similar to a natural language.",
    long_description=LONG_DESC,
    author="Kevin Kiefer",
    author_email="abc.kiefer@gmail.com",
    install_requires=["textX"],
    packages=["nldsl", "nldsl.core"],
    package_data={"nldsl.core": ["grammar/*.tx"]},
    scripts=["scripts/nldsl-compile.py"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: Free for non-commercial use",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Compilers"
    ],
    python_requires=">=3.4"
)
