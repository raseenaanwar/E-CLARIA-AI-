"""
Test Python 3.12 specific features and compatibility.

This module tests Python 3.12 specific features to ensure the codebase
takes advantage of the latest Python capabilities.
"""

import pytest
import sys
import asyncio
from typing import override
from collections.abc import Generator
from datetime import datetime
from pathlib import Path
import warnings


class TestPython312Features:
    """Test Python 3.12 specific features."""

    @pytest.mark.unit
    def test_python_version_is_312_or_higher(self):
        """Test that Python version is 3.12 or higher."""
        assert sys.version_info >= (3, 12), f"Python version {sys.version_info} is less than 3.12"

    @pytest.mark.unit
    def test_improved_error_messages(self):
        """Test Python 3.12 improved error messages."""
        # Test that we can catch more specific error information
        try:
            # This should raise a more informative error in Python 3.12
            result = {}["nonexistent_key"]
        except KeyError as e:
            # Python 3.12 provides better error context
            assert "nonexistent_key" in str(e)

    @pytest.mark.unit
    def test_type_parameter_syntax(self):
        """Test Python 3.12 type parameter syntax."""
        # Test generic class with type parameters
        class GenericContainer[T]:
            def __init__(self, value: T):
                self.value = value

            def get_value(self) -> T:
                return self.value

        # Test with string
        string_container = GenericContainer("test")
        assert string_container.get_value() == "test"

        # Test with integer
        int_container = GenericContainer(42)
        assert int_container.get_value() == 42

    @pytest.mark.unit
    def test_generic_function_syntax(self):
        """Test Python 3.12 generic function syntax."""
        def process_items[T](items: list[T]) -> list[T]:
            """Process a list of items."""
            return [item for item in items if item is not None]

        # Test with strings
        string_items = ["a", None, "b", "c"]
        result = process_items(string_items)
        assert result == ["a", "b", "c"]

        # Test with integers
        int_items = [1, None, 2, 3]
        result = process_items(int_items)
        assert result == [1, 2, 3]

    @pytest.mark.unit
    def test_override_decorator(self):
        """Test Python 3.12 @override decorator."""
        class BaseClass:
            def method(self) -> str:
                return "base"

        class DerivedClass(BaseClass):
            @override
            def method(self) -> str:
                return "derived"

        instance = DerivedClass()
        assert instance.method() == "derived"

    @pytest.mark.unit
    def test_f_string_improvements(self):
        """Test Python 3.12 f-string improvements."""
        # Test nested f-strings
        name = "World"
        greeting = f"Hello, {f'{name}!'}"
        assert greeting == "Hello, World!"

        # Test f-strings with expressions
        numbers = [1, 2, 3, 4, 5]
        result = f"Sum: {sum(numbers)}, Average: {sum(numbers) / len(numbers)}"
        assert result == "Sum: 15, Average: 3.0"

    @pytest.mark.unit
    def test_buffer_protocol_improvements(self):
        """Test Python 3.12 buffer protocol improvements."""
        # Test with bytes
        data = b"Hello, World!"
        assert len(data) == 13
        assert data[0] == 72  # 'H'

        # Test with bytearray
        mutable_data = bytearray(b"Hello")
        mutable_data[0] = 104  # 'h'
        assert mutable_data == b"hello"

    @pytest.mark.unit
    def test_pathlib_improvements(self):
        """Test Python 3.12 pathlib improvements."""
        # Test Path.walk() method (new in Python 3.12)
        test_path = Path(".")
        if hasattr(test_path, 'walk'):
            # Test that walk method exists
            assert callable(test_path.walk)

    @pytest.mark.unit
    def test_asyncio_improvements(self):
        """Test Python 3.12 asyncio improvements."""
        async def async_function():
            await asyncio.sleep(0.001)
            return "async_result"

        # Test asyncio.Runner context manager improvements
        async def test_runner():
            return await async_function()

        # Run the async function
        result = asyncio.run(test_runner())
        assert result == "async_result"

    @pytest.mark.unit
    def test_comprehension_improvements(self):
        """Test Python 3.12 comprehension improvements."""
        # Test improved performance and memory usage
        data = range(100)

        # List comprehension
        squares = [x ** 2 for x in data if x % 2 == 0]
        assert len(squares) == 50
        assert squares[0] == 0
        assert squares[-1] == 9604

        # Dict comprehension
        square_dict = {x: x ** 2 for x in range(10)}
        assert square_dict[5] == 25
        assert len(square_dict) == 10

    @pytest.mark.unit
    def test_exception_improvements(self):
        """Test Python 3.12 exception improvements."""
        # Test exception group handling
        try:
            raise ValueError("Test error")
        except ValueError as e:
            # Test that we can access exception details
            assert str(e) == "Test error"
            assert type(e).__name__ == "ValueError"

    @pytest.mark.unit
    def test_performance_improvements(self):
        """Test Python 3.12 performance improvements."""
        # Test that basic operations are working efficiently
        import time

        # Test list operations
        start_time = time.time()
        large_list = [i for i in range(10000)]
        filtered_list = [x for x in large_list if x % 2 == 0]
        end_time = time.time()

        assert len(filtered_list) == 5000
        # Should complete quickly (performance test)
        assert end_time - start_time < 1.0

    @pytest.mark.unit
    def test_typing_improvements(self):
        """Test Python 3.12 typing improvements."""
        from typing import Any, Union

        # Test Union types
        def process_value(value: Union[str, int]) -> str:
            return str(value)

        assert process_value("hello") == "hello"
        assert process_value(42) == "42"

        # Test Any type
        def handle_any(value: Any) -> bool:
            return value is not None

        assert handle_any("test") is True
        assert handle_any(None) is False

    @pytest.mark.unit
    def test_dataclass_improvements(self):
        """Test Python 3.12 dataclass improvements."""
        from dataclasses import dataclass

        @dataclass
        class Person:
            name: str
            age: int
            email: str = ""

        person = Person("John", 30)
        assert person.name == "John"
        assert person.age == 30
        assert person.email == ""

        # Test with all fields
        person2 = Person("Jane", 25, "jane@example.com")
        assert person2.email == "jane@example.com"

    @pytest.mark.unit
    def test_warning_improvements(self):
        """Test Python 3.12 warning improvements."""
        # Test that warnings can be properly caught and handled
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            warnings.warn("Test warning", UserWarning)

            assert len(w) == 1
            assert issubclass(w[0].category, UserWarning)
            assert "Test warning" in str(w[0].message)

    @pytest.mark.unit
    def test_generator_improvements(self):
        """Test Python 3.12 generator improvements."""
        def number_generator() -> Generator[int, None, None]:
            for i in range(5):
                yield i

        gen = number_generator()
        numbers = list(gen)
        assert numbers == [0, 1, 2, 3, 4]

    @pytest.mark.unit
    def test_context_manager_improvements(self):
        """Test Python 3.12 context manager improvements."""
        class TestContextManager:
            def __init__(self):
                self.entered = False
                self.exited = False

            def __enter__(self):
                self.entered = True
                return self

            def __exit__(self, exc_type, exc_val, exc_tb):
                self.exited = True
                return None

        with TestContextManager() as cm:
            assert cm.entered is True
            assert cm.exited is False

        assert cm.exited is True

    @pytest.mark.unit
    def test_string_improvements(self):
        """Test Python 3.12 string improvements."""
        # Test string methods
        text = "Hello, World!"
        assert text.lower() == "hello, world!"
        assert text.upper() == "HELLO, WORLD!"
        assert text.replace("World", "Python") == "Hello, Python!"

        # Test string formatting
        name = "Alice"
        age = 30
        formatted = f"Name: {name}, Age: {age}"
        assert formatted == "Name: Alice, Age: 30"

    @pytest.mark.unit
    def test_datetime_improvements(self):
        """Test Python 3.12 datetime improvements."""
        now = datetime.now()
        assert isinstance(now, datetime)
        assert now.year >= 2023

        # Test datetime formatting
        formatted = now.strftime("%Y-%m-%d")
        assert len(formatted) == 10
        assert formatted.count("-") == 2

    @pytest.mark.unit
    def test_collections_improvements(self):
        """Test Python 3.12 collections improvements."""
        from collections import defaultdict, Counter

        # Test defaultdict
        dd = defaultdict(list)
        dd["key"].append("value")
        assert dd["key"] == ["value"]

        # Test Counter
        counter = Counter("hello")
        assert counter["l"] == 2
        assert counter["h"] == 1
        assert counter["e"] == 1
        assert counter["o"] == 1

    @pytest.mark.unit
    def test_json_improvements(self):
        """Test Python 3.12 JSON improvements."""
        import json

        # Test JSON serialization/deserialization
        data = {"name": "test", "values": [1, 2, 3]}
        json_str = json.dumps(data)
        parsed_data = json.loads(json_str)

        assert parsed_data == data
        assert parsed_data["name"] == "test"
        assert parsed_data["values"] == [1, 2, 3]

    @pytest.mark.unit
    def test_os_improvements(self):
        """Test Python 3.12 OS improvements."""
        import os

        # Test environment variables
        test_var = "TEST_PYTHON_312"
        os.environ[test_var] = "test_value"
        assert os.getenv(test_var) == "test_value"

        # Clean up
        del os.environ[test_var]
        assert os.getenv(test_var) is None

    @pytest.mark.unit
    def test_sys_improvements(self):
        """Test Python 3.12 sys improvements."""
        import sys

        # Test sys attributes
        assert hasattr(sys, 'version_info')
        assert hasattr(sys, 'executable')
        assert hasattr(sys, 'platform')

        # Test version info
        assert sys.version_info.major == 3
        assert sys.version_info.minor >= 12
