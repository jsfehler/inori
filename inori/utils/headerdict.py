from typing import Dict


class HeaderDict(dict):
    """Dict that can store functions via a decorator."""

    def __call__(self, key: str):
        """Decorator to store a function.

        Arguments:
            key: The name for the key to be inserted
        """
        def decorator(function):
            self[key] = function
        return decorator

    def run_functions(self, *args, **kwargs) -> Dict[str, str]:
        """Run all functions with the arguments provided."""
        rv: Dict[str, str] = {}

        for k, v in self.items():
            if callable(v):
                rv[k] = v(*args, **kwargs)
            else:
                rv[k] = v

        return rv
