def main():
    import sys, os

    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

    import polychemprint3


    for p in sys.path:
        print(p)

    from polychemprint3 import mainMethod
    mainMethod.main()
    print("h")


if __name__ == "__main__":
    main()
