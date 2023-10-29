from toubib.app.core.models import PaginationModel


def calculate_pagination(offset: int, limit: int, total_count: int) -> PaginationModel:
    current_page = (offset // limit) + 1
    total_pages = -(-total_count // limit)

    pagination_info = {
        "offset": offset,
        "total_items": total_count,
        "total_pages": total_pages,
        "page_number": current_page
    }

    pagination_details = PaginationModel(**pagination_info)

    return pagination_details

