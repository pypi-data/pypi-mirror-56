# quality-viewer
A simple CLI for rendering [Quality Views](https://blog.colinbreck.com/using-quality-views-to-communicate-software-quality-and-evolution/). Built on [Graphviz](https://www.graphviz.org/).

## Installation
```
pip install quality-viewer
```

## Usage
To use, you need to create a series of JSON documents in a folder. These files define the components in your quality view and the individual scores for each attribute. Scores are out of 10, `quality-viewer` uses the mean to generate the colours in the PDF.

This is an example of the component definition:

```
{
    "component": "my-lovely-component",
    "depends_on": ["my-other-component"],
    "attributes": [
        {
            "name": "code",
            "score": 5,
            "notes": "I wrote this in Uni"
        },
        {
            "name": "tests",
            "score": 2,
            "notes": "I wrote this in Uni"
        }
    ]
}
```

Then you can run the CLI against your folder of component definitions which will generate a PDF in that folder named `quality_view.gv.pdf`:

```
quality-viewer ./my_components
```

If you run these regularly, you probably want to label each PDF. Customise the label on the graph with the `--label` argument:

```
quality-viewer --label "Quality Views - Christmas 2019" ./my_components
```

A fairly elaborate example, which uses dated quality views can be found at (other repo)[more work]. This is a good repo to get started from.

## Development
This repository is setup to validate your work easily, running tests is as simple as:

```
make test
```

And checking your coding style is:

```
make check
```

To automagically conform to the above, run:

```
make format
```
