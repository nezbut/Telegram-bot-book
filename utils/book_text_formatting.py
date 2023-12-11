from math import ceil

class BookTextFormatting:

    def __init__(self) -> None:
        self.ready_text: dict[int, str] | None = None
        self.last_text_page: int | None = None
        self.book_name: str | None = None

    def format_book_text(self, text: str, book: str) -> None:
        if len(text) <= 1150:
            self.ready_text = {1: text}
            self.last_text_page = 1
            self.book_name = book
            return

        result_dict = {}
        number = ceil(len(text) / 1150)

        for page in range(1, number + 1):
            page_text = text[:1150]

            if page == 1:
                result_dict[page] = page_text + "..."

            elif page == number:
                result_dict[page] = "..." + page_text

            else:
                result_dict[page] = "..." + page_text + "..."

            text = text[1150:]

        self.ready_text = result_dict
        self.last_text_page = list(self.ready_text.keys())[-1]
        self.book_name = book

__all__ = (
    'BookTextFormatting',
)
