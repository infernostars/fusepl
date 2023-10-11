from core.executor import run
from colors import colors

if __name__ == '__main__':
    print(f"{colors.CYAN}fuse {colors.BOLD}0.0.1a2{colors.RESET}")
    while True:
        text = input(f"{colors.RESET}fuse > {colors.GREEN}")
        result, error = run("<program entry>", text)

        if error:
            print(f"{colors.RED}{str(error)}")
        else:
            print(f"{colors.BLUE}{result}")
