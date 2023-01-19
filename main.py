import sys
from license_text_generator import LicenseTextGenerator
from scraper import Scaper
from csv_facade import CsvFacade
from logger import Logger


# Put root dependency url as parameter in run configuration
if __name__ == '__main__':
    root_url = sys.argv[1]

    if root_url is not None:
        # Create dependencies
        logger_instance = Logger()
        csv_facade_instance = CsvFacade()

        # Write header for csv
        csv_facade_instance.writeHeader()

        # Prepare writer for scraper
        with csv_facade_instance.openInWrite() as csvfile:
            writer = csv_facade_instance.getWriter(csvfile)
            scraper_instance = Scaper(logger_instance, writer, root_url)
            scraper_instance.run()

        # From generated csv create a dependency map
        dependency_map = csv_facade_instance.getLicenseToDependencyMap()
        license_text_generator_instance = LicenseTextGenerator(dependency_map)
        license_text_generator_instance.run()
