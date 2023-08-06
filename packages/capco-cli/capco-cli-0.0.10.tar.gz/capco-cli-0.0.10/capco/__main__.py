"""
Invokes capco commands when the src module is run as a script.
Example: python3 -m capco templates list
"""
import capco.commands.commands


def main():
    capco.commands.commands.commands()


if __name__ == "__main__":
    main()
