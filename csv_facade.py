import csv
from typing import IO, Any


class CsvFacade:
    def __init__(self):
        self._LICENSE_NAME_INDEX = 3
        self._PACKAGE_NAME_INDEX = 1
        self._VERSION_NUMBER_INDEX = 4
        self._FILE_NAME = "dependency_aggregation.csv"
        self._headers = ["DEPENDENCY_OF", "PACKAGE_NAME", "DEPENDENCIES", "LICENSE_NAME", "VERSION", "DEPENDENCY_LINK"]

    def openInAppend(self) -> IO:
        return self._open("a")

    def openInWrite(self) -> IO:
        return self._open("w")

    def openInRead(self) -> IO:
        return self._open("r")

    def _open(self, operation) -> IO:
        return open(self._FILE_NAME, operation, newline='', encoding="UTF8")

    def writeHeader(self) -> None:
        with self.openInWrite() as csvfile:
            writer = self.getWriter(csvfile)
            writer.writerow(self._headers)

    def getReader(self, file: IO) -> Any:
        return csv.reader(
            file,
            delimiter=',',
            quotechar='|',
            quoting=csv.QUOTE_MINIMAL
        )

    def getWriter(self, file: IO) -> Any:
        return csv.writer(
            file,
            delimiter=',',
            quotechar='|',
            quoting=csv.QUOTE_MINIMAL
        )

    def getLicenseToDependencyMap(self) -> dict[str, list[str]]:
        dependency_map = {}

        with self.openInRead() as csvfile:
            reader = self.getReader(csvfile)

            next(reader)

            for row in reader:
                license_name = row[self._LICENSE_NAME_INDEX]
                key = f"{row[self._PACKAGE_NAME_INDEX]} {row[self._VERSION_NUMBER_INDEX]}"

                if license_name not in dependency_map:
                    dependency_map[license_name] = []

                dependency_map[license_name].append(key)

        return dependency_map
