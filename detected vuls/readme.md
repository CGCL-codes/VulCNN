We select three widely used open-source products as our test objects: Libav, Xen, and Seamonkey.
The versions of these products include both several old versions and the latest version.
By this, we can report whether vulnerabilities in old versions have been 'silently' patched in the latest version or not.
Table presents the summary of our collected products, the total number of functions that can be successfully analyzed by Joern in these products is 600,233.
In other words, VulCNN analyzes a total of 600,233 functions, with a total of more than 25 million lines of code.

| OpenSource Software | #Files  | #Functions | #Lines of Code |
|---------------------|---------|------------|----------------|
| Libav-0.8.21        | 996     | 8,198      | 437,857        |
| Libav-9.21          | 1,135   | 8,917      | 471,691        |
| Libav-11.12         | 1,343   | 9,807      | 552,768        |
| Libav-12.3          | 1,509   | 10,760     | 625,034        |
| Xen-4.12.0          | 4,225   | 61,693     | 2,464,062      |
| Xen-4.13.0          | 4,988   | 68,400     | 2,783,561      |
| Xen-4.14.0          | 5,151   | 71,230     | 2,872,957      |
| Seamonkey-2.32      | 11,600  | 153,122    | 6,495,189      |
| Seamonkey-2.53.4    | 15,369  | 208,106    | 8,798,738      |
| Total               | 46,316  | 600,233    | 25,501,857     |
