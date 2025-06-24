from typing import Callable

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


class ListView:
    def __init__(self, items, on_click):
        self.items = items
        self.buttons = []
        self.widget = self._build(on_click)

    def _build(self, on_click):
        for i, item in enumerate(self.items):
            btn = widgets.Button(
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
            btn._index = i
            btn.on_click(on_click)
            self.buttons.append(btn)

        box = widgets.VBox(
            self.buttons,
            layout=widgets.Layout(
                grid_gap="4px",
                overflow="scroll",
                width="100%",
                height="100%",
                border="none",
                margin="0",
                padding="0",
            ),
        )
        box.add_class("light-scrollbar")
        return box


class DetailView:
    def __init__(self, on_back, on_prev, on_next):
        self.title = widgets.Label()
        self.prev_button = widgets.Button(
            description="< Prev",
            button_style="info",
            layout=widgets.Layout(width="50%", height="100%"),
        )
        self.next_button = widgets.Button(
            description="Next >",
            button_style="info",
            layout=widgets.Layout(width="50%", height="100%"),
        )
        self.update_text: Callable
        self.widget = self._build(on_back, on_prev, on_next)

    def _scrollable_text_box(self):
        textbox = widgets.HTML(
            value="",
            layout=widgets.Layout(
                height="100%", width="100%", overflow="auto", padding="10px", margin="0"
            ),
        )
        textbox.add_class("light-scrollbar")

        def update_text(new_text: str):
            formatted = new_text.replace("\n", "<br>")
            textbox.value = f"""<div style="width: 100%; word-wrap: break-word;
                word-break: break-word; white-space: normal; font-family: arial; line-height: 1.5;">
                {formatted}</div>"""

        self.update_text = update_text
        return textbox

    def _build(self, on_back, on_prev, on_next):
        back_button = widgets.Button(
            description="<- Back to List",
            button_style="info",
            layout=widgets.Layout(width="auto", height="32px"),
        )
        direction_buttons = widgets.HBox(
            [self.prev_button, self.next_button],
            layout=widgets.Layout(
                width="auto", height="32px%", flex="0 0 auto", overflow="hidden"
            ),
        )
        menu = widgets.HBox(
            [back_button, self.title, direction_buttons],
            layout=widgets.Layout(
                justify_content="space-between",
                align_items="center",
                padding="8px",
                width="100%",
                height="48px",
                flex="0 0 auto",
                overflow="hidden",
            ),
        )

        back_button.on_click(on_back)
        self.prev_button.on_click(on_prev)
        self.next_button.on_click(on_next)

        text_box = self._scrollable_text_box()
        return widgets.VBox([menu, text_box], layout=widgets.Layout(width="100%"))


class ListExplorer:
    def __init__(self, items: list[str], height=400, is_height_max=True):
        self.items = items
        self.current_idx = 0
        self.total = len(items)

        self.list_view = ListView(items, self._open_detail_view)
        self.detail_view = DetailView(
            self._open_list_view, self._on_prev_click, self._on_next_click
        )

        self.main_view = widgets.Stack(
            [self.list_view.widget, self.detail_view.widget],
            selected_index=0,
            layout=widgets.Layout(
                width="100%",
                height=None if not is_height_max else f"{height}px",
                max_height=f"{height}px" if is_height_max else None,
            ),
        )

        app = widgets.VBox(
            [widgets.HTML(SCROLL_BAR_STYLE), self.main_view],
            layout=widgets.Layout(
                padding="10px",
            ),
        )
        display(app)

    def _open_list_view(self, _):
        self.main_view.selected_index = 0

    def _open_detail_view(self, btn):
        idx = btn._index
        self._update_detail_view(idx)
        self.main_view.selected_index = 1

    def _on_prev_click(self, _):
        if self.current_idx > 0:
            self._update_detail_view(self.current_idx - 1)

    def _on_next_click(self, _):
        if self.current_idx < self.total - 1:
            self._update_detail_view(self.current_idx + 1)

    def _update_detail_view(self, idx):
        self.current_idx = idx
        self.detail_view.prev_button.disabled = idx == 0
        self.detail_view.next_button.disabled = idx == self.total - 1
        self.detail_view.title.value = f"Item {idx + 1} of {self.total}"
        self.detail_view.update_text(self.items[idx])
