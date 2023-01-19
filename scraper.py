from typing import Any

import undetected_chromedriver as uc
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from logger import Logger


class Scaper:
    def __init__(self, logger: Logger, writer: Any, root_url: str):
        self._driver = None
        self._logger = logger
        self._writer = writer
        self._visited = set()
        self._queue = [self._createDependencyObject("", root_url)]

    def run(self) -> None:
        self._driver = uc.Chrome()

        while len(self._queue) > 0:
            current_object = self._queue.pop(0)
            parent_name = current_object["parent_name"]
            url = current_object["url"]

            self._logger.logCurrentUrl(url)
            self._driver.get(url)

            rows = self._driver.find_element(By.CLASS_NAME, "version-section").find_elements(By.TAG_NAME, "tr")

            if len(rows) == 0:
                continue

            child_dependencies = []

            child_dependencies.extend(self._iterateTableRows(rows))

            if self._checkForProvidedDependenciesSection():
                provided_dependencies_table = self._driver.find_elements(By.CLASS_NAME, "version-section")[1]
                rows = provided_dependencies_table.find_elements(By.TAG_NAME, "tr")

                child_dependencies.extend(self._iterateTableRows(rows))

            self._writeCurrentDependencyData(parent_name, url, child_dependencies)

        self.quit()

    def _checkForProvidedDependenciesSection(self) -> bool:
        found = False

        try:
            self._driver.find_element(By.XPATH, "// h2[contains(text(), 'Provided Dependencies')]")
            found = True
        except NoSuchElementException:
            pass

        return found

    def _getPackageName(self) -> str:
        breadcrumb = self._driver.find_element(By.CLASS_NAME, "breadcrumb").find_elements(By.TAG_NAME, "a")
        return f"{breadcrumb[1].text} » {breadcrumb[2].text}"

    def _writeCurrentDependencyData(self, parent_name: str, url: str, child_dependencies: list[str]) -> None:
        breadcrumb = self._driver.find_element(By.CLASS_NAME, "breadcrumb")
        package_a_tags = breadcrumb.find_elements(By.TAG_NAME, "a")
        version_span = breadcrumb.find_element(By.TAG_NAME, "span")
        license_row = self._driver.find_element(By.CLASS_NAME, "grid").find_elements(By.TAG_NAME, "tr")[0]
        license_name = " "

        try:
            license_name = license_row.find_element(By.CSS_SELECTOR, "span[class='b lic']").text
        except NoSuchElementException:
            pass

        package_name = f"{package_a_tags[1].text} » {package_a_tags[2].text}"
        version = f"{version_span.text}"
        row_data = [parent_name, package_name, '; '.join(child_dependencies), license_name, version, url]

        self._logger.logDependency(package_name, parent_name, version, license_name, url)
        self._writer.writerow(row_data)

    def _getTableRows(self, source: Any) -> list[WebElement]:
        return source.find_element(By.CLASS_NAME, "version-section").find_elements(By.TAG_NAME, "tr")

    def _iterateTableRows(self, rows: list[WebElement]) -> list[str]:
        child_dependencies = []

        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            current_package = self._getPackageName()

            if len(cols) == 0:
                continue

            child_dependencies.append(self._addChildDependenciesToStack(current_package, cols))

        return child_dependencies

    def _addChildDependenciesToStack(self, current_package: str, cols: list[WebElement]) -> str:
        license_name = " "

        try:
            license_name = cols[0].find_element(By.CSS_SELECTOR, "span[class='b lic']").text
        except NoSuchElementException:
            pass

        package_name = cols[2].text
        version = cols[3].text
        dependency_link = cols[3].find_element(By.TAG_NAME, "a").get_attribute("href")
        key = f'{package_name} {version}'

        self._logger.logDependency(current_package, package_name, version, license_name, dependency_link)

        if key not in self._visited:
            self._queue.append(self._createDependencyObject(current_package, dependency_link))
            self._visited.add(key)

        return package_name

    def _createDependencyObject(self, parent_name: str, url: str) -> dict:
        return {
            "parent_name": parent_name,
            "url": url
        }

    def quit(self) -> None:
        self._driver.quit()
