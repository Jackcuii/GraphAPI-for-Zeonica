# GraphAPI for Zeonica
**Pytorch computing graph interface** for Zeonica, a CGRA &amp; Wafer simulator.
(Project by [Sarchlab W&M](https://sarchlab.org/) )

This API is written in Python and its a published packet which could be installed with pip (not for now). It generates a instruction sequence of the forward and backward process from a given Pytorch module.

You are expected to use it under at least Pytorch 2.1

Up to now, this tool is just in experimental stage, so that the generated sequence will be 'fake instrs'.
The `symbol` fields are tensors' names (though it may have the same name with some operator in lower case)
