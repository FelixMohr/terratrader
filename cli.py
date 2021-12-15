import terra_sdk

from src.core import get_bluna_for_luna
from src.helpers import create_params, info, create_terra, create_wallet


def main():
    with open("files/greeting.txt") as f:
        content = f.read()
        print(content)

    params = create_params()
    terra = create_terra()
    wallet = create_wallet(terra)

    while True:
        inp = input(' 👽    >>> ').strip()
        split = inp.split()
        if not len(split):
            continue
        command = split[0]
        args = split[1:]
        if command == 'quit':
            terra.session.close()
            break
        try:
            if command == 'supply':
                supply = get_bluna_for_luna(terra)
                print(supply)
            else:
                info('Invalid Command.')
        except terra_sdk.exceptions.LCDResponseError as e:
            print(e)


if __name__ == "__main__":
    main()
