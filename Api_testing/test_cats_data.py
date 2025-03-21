import allure
import assertpy
import requests
from GD_QA_Portfolio2025.Api_testing.api_client import ApiClient


@allure.suite("Testing cats data")
class TestCatData:
    @allure.title("Testing cats breeds")
    @allure.issue("https://catfact.ninja/", "Here can be jira task")
    def test_get_data(self, api_client_cats: ApiClient):
        cat_data = api_client_cats.find_cats_data(json_data={})
        with allure.step("Assert the first breed"):
            assert cat_data.data[0].breed == "Abyssinian"

        with allure.step("Assert pages are sorted"):
            assertpy.assert_that(cat_data.current_page).is_less_than(cat_data.last_page)
        with allure.step("Assert data doesn't contain duplicates"):
            assertpy.assert_that(cat_data.data[0].model_dump().values()).does_not_contain_duplicates()
        with allure.step("Assert all breeds have required attributes"):
            for cat in cat_data.data:
                assertpy.assert_that(cat.breed).is_not_empty()
                assertpy.assert_that(cat.country).is_not_empty()
                assertpy.assert_that(cat.origin).is_not_empty()
                assertpy.assert_that(cat.coat).is_not_empty()
                assertpy.assert_that(cat.pattern).is_not_empty()
        with allure.step("Assert all breed names are unique"):
            breed_names = [cat.breed for cat in cat_data.data]
            assertpy.assert_that(breed_names).does_not_contain_duplicates()

        with allure.step("Assert all page links have valid attributes"):
            for link in cat_data.links:
                assertpy.assert_that(link.label).is_not_empty()
                assertpy.assert_that(link.active).is_instance_of(bool)
                if link.url:
                    assertpy.assert_that(str(link.url)).starts_with("http")


