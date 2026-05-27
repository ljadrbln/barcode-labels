from src.label_layouts import LABEL_WIDTH
from src.label_layouts import LABEL_HEIGHT
from src.label_layouts import LAYOUT_MARGIN
from src.label_layouts import LEFT_COLUMN_WIDTH
from src.label_layouts import build_layout


def test_build_layout():
    result = build_layout()

    assert result["inner_x"] == LAYOUT_MARGIN
    assert result["inner_y"] == LAYOUT_MARGIN
    assert result["inner_width"] == LABEL_WIDTH - (LAYOUT_MARGIN * 2)
    assert result["inner_height"] == LABEL_HEIGHT - (LAYOUT_MARGIN * 2)
    assert result["right_x"] == LAYOUT_MARGIN + LEFT_COLUMN_WIDTH
    assert result["right_width"] == result["inner_width"] - LEFT_COLUMN_WIDTH