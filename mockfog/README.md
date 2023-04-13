# MockFog 2.0 Infrastructure Specification

This directory contains the MockFog 2.0 specification for our fog data processing benchmark.
Copy the infrastructure specification `infrastructure.jsonc` to `node-manager/run/config/i` (create if it does not exist) of your local MockFog 2.0 copy.
A copy of MockFog 2.0 can be obtained from [GitHub](https://github.com/OpenFogStack/MockFog2).
Follow the instructions in the MockFog 2.0 repository to configure the other configuration options.

In order to save resources, we recommend locating all sensors of a location on one virtual cloud instance.

Please make sure to configure the `aws` settings in the infrastructure configuration.
