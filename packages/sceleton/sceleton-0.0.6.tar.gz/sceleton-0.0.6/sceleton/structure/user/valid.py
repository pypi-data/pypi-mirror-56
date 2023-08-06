# Checks if a given user choice is valid in the given collection of classifiers.


def range(uinput, collection):
    if uinput == "":
        return True

    try:
        return all(
            map(lambda choice: 1 <= int(choice) <= len(collection), uinput.split(" "))
        )
    except:
        return False
