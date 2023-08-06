# API Documentation

Sphinx can automatically generate API documentation from your code with [Autodoc](http://www.sphinx-doc.org/en/master/usage/quickstart.html#autodoc).
See the [Sphinx-Napoleon documentation](http://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html) for examples showing how to write compatible docstrings.

## Example

With the following file in `api_example/module.py`:

```python
    class ExampleClass:
        def do_something(self, param1, param2):
            """Example function with PEP 484 type annotations.

            Args:
                param1 (str): The first parameter.
                param2 (int): The second parameter.

            Returns:
                bool: True for success, False otherwise.
            """
```

This markup:

```rst
    ```eval_rst
        .. autoclass:: api_example.module.ExampleClass
           :members:
    ```
```

Will produce:

```eval_rst
    .. autoclass:: api_example.module.ExampleClass
       :members:
```
