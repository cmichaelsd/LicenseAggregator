from typing import IO


class LicenseTextGenerator:
    def __init__(self, dependency_map: dict[str, list[str]]):
        self._FILE_NAME = "license.txt"
        self.WARNING = "THESE FILES NEED ATTENTION THEIR LICENSE WAS NOT FOUND IN THE SYSTEM!\n\n"
        self._dependency_map = dependency_map
        self._visited = set()
        self._license_map = {
            "MIT": "mit.txt",
            "Apache 2.0": "apache_2.txt",
            "Apache": "apache_2.txt",
            "BSD": "bsd.txt",
            "BSD 2-clause": "bsd_2_clause.txt",
            "BSD 3-clause": "bsd.txt",
            "BouncyCastle": "bouncy_castle.txt",
            "GPL 2.0": "gpl_2.txt",
            "CDDL": "cddl.txt",
            "CDDL 1.0": "cddl.txt",
            "UPL": "upl.txt",
            "CC0 1.0": "cc0_1.txt",
            "EDL 1.0": "edl_1.txt",
            "MPL 2.0": "mpl_2.txt",
            "LGPL 2.1": "lgpl_2_1.txt"
        }

    def _writeUnknownLicenseDependencies(self) -> None:
        with open(self._FILE_NAME, "a", newline='', encoding="UTF8") as compiled_license_file:
            # Iterate dependency map, key are license name
            for license_name in self._dependency_map:
                # If license name is not known or Public
                if license_name not in self._license_map and license_name != "Public":
                    was_found = False

                    # For each dependency under currently observed license
                    for dependency in self._dependency_map[license_name]:

                        # If dependency has not been seen
                        if dependency not in self._visited:
                            was_found = True
                            # Write each dependency with currently observed license
                            compiled_license_file.write(f"{license_name} {dependency}\n")
                            self._visited.add(dependency)

                    if was_found:
                        compiled_license_file.write(self.WARNING)

    def _writeKnownLicenseDependencies(self) -> None:
        with open(self._FILE_NAME, "w", newline='', encoding="UTF8") as compiled_license_file:
            for license_name in self._license_map:
                was_found = False

                # If license is known and exists in dependency map
                if license_name in self._dependency_map and license_name in self._dependency_map:
                    for dependency in self._dependency_map[license_name]:
                        if dependency not in self._visited:
                            was_found = True
                            compiled_license_file.write(f"{license_name} {dependency}\n")
                            self._visited.add(dependency)

                    # If dependencies were found for the current observed license
                    if was_found:
                        # If license is known
                        if license_name in self._license_map:
                            license_file_name = self._license_map[license_name]

                            # Write license text to file under dependencies list
                            self._writeLicenseToFile(license_file_name, compiled_license_file)
                        # Otherwise if license name is "Public"
                        elif license_name == "Public":

                            # Explicitly declare they are public
                            compiled_license_file.write("These dependencies are for public use and have no license.\n\n")

    def run(self) -> None:
        self._writeKnownLicenseDependencies()
        self._writeUnknownLicenseDependencies()

    def _writeLicenseToFile(self, license_file_name: str, file: IO) -> None:
        with open(f"licenses/{license_file_name}", "r", newline='', encoding="UTF8") as license_file:
            for line in license_file:
                file.write(line)
            file.write("\n\n")
