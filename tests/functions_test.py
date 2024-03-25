import team_task_manager.functions as functions
import pytest

@pytest.mark.parametrize(
    ('user_input', 'expected'),
    (
        (';', True),
        ('str', False),
        (1, False),
        (1.0, False),
        (True, False),
    )
)

def test_semicolon_found(user_input, expected):
    assert functions.semicolon_found(user_input) == expected

@pytest.mark.parametrize(
    ('user_input', 'expected'),
    (
        (('#'*164), True),
        ('#', False),
        (('#'*163), False),
    )
)

def test_character_exceed(user_input, expected):
    assert functions.character_exceed(user_input) == expected
