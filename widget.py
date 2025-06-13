import ipywidgets as widgets
from IPython.display import display

SCROLL_BAR_STYLE = """<style>
.light-scrollbar::-webkit-scrollbar {
    width: 8px;
    height: 8px;
    background-color: #f1f1f1;
}
.light-scrollbar::-webkit-scrollbar-thumb {
    background-color: #c1c1c1;
    border-radius: 4px;
}
.light-scrollbar::-webkit-scrollbar-thumb:hover {
    background-color: #a0a0a0;
}
.light-scrollbar {
    scrollbar-width: thin;
    scrollbar-color: #c1c1c1 #f1f1f1;
}
</style>
"""


class ListExplorer:
    """List explorer w/ a list view & a detail view"""

    def __init__(self, items: list[str], height=400, is_height_max=False):
        self.items = items
        self.current_idx = 0
        self.total = len(items)
        self.detail_view_title: widgets.Label = widgets.Label()

        # Create the list view & the detail view & stack them together
        list_view = self._create_list_view()
        detail_view = self._create_detail_view()

        self.main_view: widgets.Stack = widgets.Stack(
            [list_view, detail_view],
            selected_index=0,
            layout=widgets.Layout(
                width="100%",
                height=None if is_height_max else f"{height}px",
                max_height=f"{height}px" if is_height_max else None,
                padding="10px",
            ),
        )

        # Add custom CSS
        app = widgets.VBox([widgets.HTML(SCROLL_BAR_STYLE), self.main_view])
        display(app)

    def _scrollable_text_box(self) -> widgets.HTML:
        textbox: widgets.HTML = widgets.HTML(
            value="",
            layout=widgets.Layout(
                height="100%", width="100%", overflow="auto", padding="10px", margin="0"
            ),
        )
        textbox.add_class("light-scrollbar")

        def update_text(new_text: str):
            # Make text html safe
            formatted_text = new_text.replace("\n", "<br>")
            textbox.value = f"""<div style="width: 100%; 
    word-wrap: break-word;
                word-break: break-word; white-space: normal; font-family: arial; line-height: 1.5;">
                {formatted_text}</div>"""

        self.update_text = update_text
        return textbox

    def _create_detail_view(self):
        """The detail view is a menu bar w/ a text box below"""
        back_button: widgets.Button = widgets.Button(
            description="<- Back to List",
            button_style="info",
            layout=widgets.Layout(width="20%", height="100%"),
        )

        prev_button: widgets.Button = widgets.Button(
            description="< Previous",
            button_style="info",
            layout=widgets.Layout(width="50%", height="100%"),
        )
        next_button: widgets.Button = widgets.Button(
            description="Next >",
            button_style="info",
            layout=widgets.Layout(width="50%", height="100%"),
        )

        direction_buttons = widgets.HBox(
            [prev_button, next_button],
            layout=widgets.Layout(width="20%", height="100%", flex="0 0 auto"),
        )

        menu = widgets.HBox(
            [back_button, self.detail_view_title, direction_buttons],
            layout=widgets.Layout(
                justify_content="space-between",
                padding="3px",
                width="100%",
                flex="0 0 auto",
            ),
        )

        back_button.on_click(self._open_list_view)
        prev_button.on_click(self._on_prev_click)
        next_button.on_click(self._on_next_click)

        # These are updated when we change detail view
        self.prev_button = prev_button
        self.next_button = next_button

        text_box = self._scrollable_text_box()
        return widgets.VBox([menu, text_box], layout=widgets.Layout(width="100%"))

    def _create_list_view(self):
        buttons = []
        for i, item in enumerate(self.items):
            btn: widgets.Button = widgets.Button(
                description=f"{i + 1}. {item}",
                layout=widgets.Layout(
                    width="100%",
                    height="30px",
                    flex="0 0 auto",
                    margin="0",
                    display="flex",
                    justify_content="flex-start",
                ),
            )
            btn.index = i  # type: ignore
            btn.on_click(self._open_detail_view)
            buttons.append(btn)

        box: widgets.VBox = widgets.VBox(
            buttons,
            layout=widgets.Layout(
                grid_gap="4px", overflow="scroll", width="100%", height="100%"
            ),
        )
        box.add_class("light-scrollbar")
        return box

    ## Action functions
    def _open_list_view(self, btn):
        self.main_view.selected_index = 0

    # Detail view buttons
    def _on_prev_click(self, btn):
        if self.current_idx > 0:
            self._update_detail_view(self.current_idx - 1)

    def _on_next_click(self, btn):
        if self.current_idx < self.total - 1:
            self._update_detail_view(self.current_idx + 1)

    def _open_detail_view(self, btn):
        "Opens the detail for specific button/list-item"
        idx: int = btn.index
        self.main_view.selected_index = 1
        self._update_detail_view(idx)

    def _update_detail_view(self, idx: int):
        """Update the detail view. Assumes already in detail view"""
        self.current_idx = idx
        self.prev_button.disabled = idx == 0
        self.next_button.disabled = idx == self.total - 1
        self.detail_view_title.value = f"Item {idx + 1} of {self.total}"
        self.update_text(self.items[idx])
