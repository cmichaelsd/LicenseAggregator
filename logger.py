class Logger:
    def logCurrentUrl(self, url: str):
        print("++++++++++++++++")
        print(f"* Current url: {url}")
        print("++++++++++++++++")

    def logDependency(
            self,
            package_name: str,
            dependency_of: str,
            version: str,
            license_name: str,
            dependency_link: str
    ):
        print(package_name)
        print(dependency_of)
        print(version)
        print(license_name)
        print(dependency_link)
        print("----------------")