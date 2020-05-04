# clide:
#   source: https://raw.githubusercontent.com/qix/clide/master/clide/prompt.py
#   version: 0.9.0
# License under the MIT License.
# See https://github.com/qix/clide/blob/master/LICENSE for details


def prompt(
    message, options=None, default=None, strip=True, lower=False, suggestion=None,
):
    # Sanity check
    if options is not None:
        assert (
            default is None or default in options
        ), "The default value must be an option"

    if default is not None and suggestion is None:
        suggestion = default
    if default:
        message += " [%s]" % suggestion

    try:
        # Loop if the answer is not one of the listed options
        while True:
            result = input(message + " ")
            result = result.strip() if strip else result
            result = result.lower() if lower else result
            if result == "" and default is not None:
                return default
            elif options is None or result in options:
                return result
            else:
                print(red("Could not interpret answer: "), repr(result))

    except EOFError:
        sys.stdout.write("\n")
        print("Could not read prompt from stdin.", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        sys.stdout.write("\n")
        sys.exit(1)


def proceed(message="Are you sure you want to proceed?", *, default=True):
    answers = {
        "y": True,
        "yes": True,
        "n": False,
        "no": False,
    }

    suggestion = " [y/n]"
    result = prompt(
        message,
        options=answers.keys(),
        default="y" if default else "n",
        suggestion="Y/n" if default else "y/N",
        lower=True,
    )
    return answers[result]
