import click


class Inclusive(click.Option):
    def __init__(self, *args, **kwargs):
        self.required_with: list = kwargs.pop("required_with")

        assert self.required_with, "'required_with' parameter required"
        kwargs["help"] = (kwargs.get("help", "") + " Must be run with " +
                          ", ".join(self.required_with) + ".").strip()
        super(Inclusive, self).__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        current_opt: bool = self.name in opts
        for inclusive_opt in self.required_with:
            if inclusive_opt not in opts:
                if current_opt:
                    raise click.UsageError(
                        "Illegal usage: '" + str(self.name) + "' must be run with " + str(inclusive_opt) + ".")
                else:
                    self.prompt = None
        return super(Inclusive, self).handle_parse_result(ctx, opts, args)
