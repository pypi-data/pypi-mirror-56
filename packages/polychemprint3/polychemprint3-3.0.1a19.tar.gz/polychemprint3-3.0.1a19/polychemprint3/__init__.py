import sys, os
from polychemprint3 import mainMethod

def main():

    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

    for p in sys.path:
        print(p)

    mainMethod.main()
    print("h")


if __name__ == "__main__":
    main()
