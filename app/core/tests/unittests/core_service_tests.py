from app.core.service import calculate_pagination
from app.core.models import PaginationModel


def test_valid_input_values():
    """
    Testing the functionality of the pagination
    Returns:

    """
    # Arrange
    offset = 10
    limit = 5
    total_count = 25

    # Act
    result = calculate_pagination(offset, limit, total_count)

    # Assert
    assert isinstance(result, PaginationModel)
    assert result.offset == offset
    assert result.total_items == total_count
    assert result.total_pages == 5
    assert result.page_number == 3


def test_limit_zero():
    """
    Edge case test, we already have validation on api, but in case fct called from anywhere else we are testing
    Returns:

    """
    # Arrange
    offset = 10
    limit = 0
    total_count = 100

    # Act
    result = calculate_pagination(offset, limit, total_count)

    # Assert
    assert isinstance(result, PaginationModel)
    assert result.offset == offset
    assert result.total_items == total_count
    assert result.total_pages == 0
    assert result.page_number == 1


def test_total_count_zero():
    """
    Testing with 0 count
    Returns:

    """
    # Arrange
    offset = 10
    limit = 5
    total_count = 0

    # Act
    result = calculate_pagination(offset, limit, total_count)

    # Assert
    assert isinstance(result, PaginationModel)
    assert result.offset == offset
    assert result.total_items == total_count
    assert result.total_pages == 0
    assert result.page_number == 1
