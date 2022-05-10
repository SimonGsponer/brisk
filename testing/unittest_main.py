import pytest

# if __name__ == '__main__':

#     testsuite = unittest.TestLoader().discover('./testing/unittesting')
#     unittest.TextTestRunner(verbosity=1).run(testsuite)

# content of myinvoke.py
import sys


class MyPlugin:

    def pytest_sessionfinish(self):
        print("*** test run reporting finishing")


if __name__ == "__main__":
    sys.exit(pytest.main(["-qq"], plugins=[MyPlugin()]))
