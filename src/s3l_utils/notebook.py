from functools import partial

import IPython.display

print_md = partial(IPython.display.display_markdown, raw=True)
