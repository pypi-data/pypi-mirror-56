import sys
from autoupgrade import Package
from .__init__ import dispatch


def main():
    Package('suite_py', index='https://test.pypi.org/simple', verbose=True).smartupgrade()
    return dispatch(sys.argv[1:])


if __name__ == "__main__":
    sys.exit(main())
