# License Aggregation Tool

### Purpose
Creating LTs for 3rd Party Libraries is a very time-consuming task which can take hours or days.

This tool will automatically go through [mvnrepository.com](https://mvnrepository.com) and iterate from the root dependency webpage given down to the bottom of the dependency tree.

This project will produce a CSV file which will list relevant information for an LT request and from this CSV file a second iteration will sort dependencies by license type and compile a single license file listing which dependencies use which license.

### How to use
Open the project in Pycharm and under the menu `Run > Run... > Edit Configurations...`

Then at the menu under `Parameters` input your root dependency as a string, for example:
`"https://mvnrepository.com/artifact/com.azure.resourcemanager/azure-resourcemanager/2.21.0"`

The generated CSV uses Single Table Inheritance if a row has no DEPENDENCY_OF value then it is a root module and if a row references the PACKAGE_NAME of another row then that row is a dependency of the referenced row.

### Extensibility
If you find a license which appears often which isn't in `/licenses` please add it as a .txt file and add the mapping to `LicenseTextGenerator+_license_map` within the program.