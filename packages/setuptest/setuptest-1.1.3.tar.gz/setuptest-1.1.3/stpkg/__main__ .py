import sys
import starterclass

def main(args=None):
    if args is None:
        args = sys.argv[1:]

    print("The main routine from __main__.py was triggered. Should import and open starterclass.starterclass() running a fresh cofig file")
    starterclass.startclass()


if __name__ == "__main__":
    main()

