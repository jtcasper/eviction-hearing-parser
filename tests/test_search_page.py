import pytest

import hearing


class TestSearchPage:
    @pytest.mark.parametrize(
        "index, expected",
        [(0, "Final Status"), (1, "Final Status"), (2, "Trial/Hearing Set"),],
    )
    def test_get_case_status(self, index, expected):
        soup = hearing.get_test_search_page(index)
        status = hearing.get_status(soup)
        assert expected in status

    @pytest.mark.parametrize(
        "index, expected",
        [
            (
                0,
                "https://odysseypa.traviscountytx.gov/JPPublicAccess/CaseDetail.aspx?CaseID=2286743",
            ),
            (
                1,
                "https://odysseypa.traviscountytx.gov/JPPublicAccess/CaseDetail.aspx?CaseID=2286703",
            ),
            (
                2,
                "https://odysseypa.traviscountytx.gov/JPPublicAccess/CaseDetail.aspx?CaseID=2270305",
            ),
        ],
    )
    def test_get_url_to_register_of_actions(self, index, expected):
        soup = hearing.get_test_search_page(index)
        url = hearing.get_register_url(soup)
        assert expected == url
