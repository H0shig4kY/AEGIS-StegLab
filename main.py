#PROJECT AEGIS - STEGLAB
#Version 1.0.0

from aegis.cli import initialize_cli

def main():
    initialize_cli()

from aegis.cli import Main

if __name__ == "__main__":
    try:
        Main()

    except KeyboardInterrupt:
        print("\n\nExiting StegLab...")