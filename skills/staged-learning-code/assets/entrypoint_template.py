"""
<number>_<element_name> — <one-line description of the element>.

<a declaration that reading just this file makes the behavior clear>
<what is intentionally omitted>

Run: python main.py
"""

# Standard library only. If there are external dependencies, keep them minimal.


# ---------------------------------------------------------------------------
# <the element's lead class>: <one-line description>
#   - <key point 1>
#   - <key point 2>
# ---------------------------------------------------------------------------
class MainClass:
    def __init__(self):
        ...

    def public_method(self, args):
        ...


# ---------------------------------------------------------------------------
# Showcase for verification. Run through success + failure cases lined up in a list.
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    instance = MainClass()

    print("=== Cases ===")
    cases = [
        ("success case 1", {"arg": "..."}),
        ("failure case 1", {"arg": "..."}),  # deliberately break it to show the behavior
    ]
    for name, args in cases:
        result = instance.public_method(args)
        print(f"  {name}: {result}")
