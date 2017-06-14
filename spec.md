{
    "title": "Pixels and Their Neighbors",
    "subtitle": "A Finite Volume Tutorial",
    "contributors": {
        "authors": [
            "@bricks:person:rowan",
            "@bricks:person:lindsey",
            {
                "name": "Douglas W. Oldenburg",
                "affiliation": "@bricks:org:ubcgif"
            }
        ],
        "reviewers": [
            "@bricks:person:sgkang"
        ],
        "funders": [
            "@bricks:org:ubc",
            "@bricks:org:ubcgif",
            "@bricks:org:nserc/vanier2016_12345"
        ]
    },
    "date": "11/06/2016",
    "modules": {
        "../include/equations/dc-resistivity.imd": {
            "name":"dc-res",
            "init": {
                "electrode_1.x": 5
            }
        }
    },
    "properties": {
        "include": {
            "@bricks:mason/icare": "*",
            "@bricks:mason/youtube": "*",
            "@bricks:hjkewr234": {
                "import":["sigma", {"x":"lindsey_x"}],
            }
        },
        "icare": {
            "type": "int",
            "default": 3,
            "range": [1, 5]
        },
        "icare_5": {
            "type": "event.trigger",
            "alt": "Show All",
            "trigger": "icare = 5"
        },
        "x": {
            "type": "float",
            "default": 0.0,
            "range": [0.0, 25.0, 2.5]
        },
        "y": {
            "type": "function",
            "args": ["x"],
            "function": "0.2 * x + 5"
        },
        "sigma": {
            "type": "float",
            "doc": "electrical conductivity",
            "ref": "@bricks:hjkewr234",
            "default": 0.0,
            "units": "S/m",
            "format": ".2e"
            "log_range": [-3, 3, 0.5]
        },
        "background": {
            "type": "float",
            "doc": "electrical conductivity of the background",
            "default": 0.0,
            "units": "S/m",
            "log_range": [-3, 3, 0.5]
        },
        "dcimage":{
            "type": "service",
            "url": "https://simpeg.xyz/services/v1/dc/block"
            "ref": [
                "@sgkang",
                "@simpeg2015",
                {
                    "type": "influence",
                    "reason": "color choices",
                    "pointer": "@bricks:org:seaborn#color_pallet5"
                }
            ],
            "parameters": {
                "hx": [[1,100]],
                "hy": [[1,100]],
                "x0": "CC",
                "block_location": [["{{ x }}",-25],[25,25]],
                "block_sigma": "{{ sigma }}",
                "background_sigma": "{{ background }}",
                "return": "phi",
                "size": [200,200],
                "labels": true
            }
            "return": "image"
        }
    },
    "issues":["@bricks:issues:gjashdf7890"],
    "parent":["@bricks:fgh5678mnbv"]
}

This is an interactive document, the variables can be edited in the top right settings menu, or you can define them inline.
For example, try dragging this slider all the way to the right: {{ icare.view.slider }}. I have hooked this up to change the
amount of text that is shown to explain things! if you are a programmer look at the code {{ programmer.view.toggle }}.

[ icare > 3 ]{
    [>anchor("dc")]{
        ### Direct Current Resistivity

        Direct current (DC) resistivity surveys are used to obtain information about subsurface electrical
        conductivity, which can be a diagnostic physical property in, for example, mineral exploration or
        hydrogeologic problems, where the target of interest has a significant electrical conductivity
        contrast from the background. In a DC resistivity survey, steady state currents are set up in the
        subsurface by injecting current through a positive electrode (located at $r_{s^+}$) and completing
        the circuit with a return electrode at ($r_{s^-}$).
        [>]{This is an extra sentence that is just a side note.}

        [ programmer ]{


            [>tabs(language)]{

                [ language == "python" ]{

                    ```python
                    from SimPEG import *
                    ```

                }

                [ language == "javascript" ]{

                    ```javascript


                    ```

                }

            }

            [>warn]{
                This is a warning.
            }

            [>outline]{
                * One
                * two
                    * {{ dc.view.title }}
            }

            [>purpose]{
                I am trying to give a bit of an overview of DC resistivity.
            }

        }
        Conservation of charge (which can be derived by
        taking the divergence of Ampere’s law at steady state) connects the divergence of the current density
        everywhere in space to the source term, consisting of two point sources, essentially charges, one
        positive and one negative.
        [+]{
            Sometimes you want to write more inline.

        }
        The flow of current sets up electric fields according to [Ohm’s law](@bricks:geosci/em#ohms_law), which
        relates current density to electric fields through the subsurface electrical conductivity {{ @cockett2015; @heagySEG }}. From
        static Faraday’s law, we can describe the [electric field](@wikipedia) in terms of a scalar potential, $\phi$,
        which we sample at potential electrodes to obtain data (potential differences).
    }
}

You can see in section {{ dc.view.number }} the explanation!
Please note that you may need to click this button to see all of the text {{ icare_5.view.button }}.

In the figure below we can see that the block is [ sigma <= 1e0 ]{ resistive } [ sigma > 1e0 ]{ conductive } because
$ \sigma = {{ sigma.format }} $. Remember this is an interactive document, so you can set $\sigma$ directly and the image below
will update:

 * Block Conductivity ({{ sigma.units }}): {{ sigma.view.slider }}
 * Background Conductivity ({{ background.units }}): {{ background.view.slider }}

![The potential, $\phi$, of a block in a half space.]({{ dcimage }})

{{ = log(sigma) }}
{{ = mesh.nC + 1 }}

{{ dc-res.electrode_1.x.view.slider }}

<#app>{{ dc-res }}

{{ dc-res#maxwell_time }}

{{ @bricks:gjqsdckj123kl }}


{{ @bricks:gjhasdf234 }}



{{ vid1 }}
[= 25 < vid1.progress < 35 ]{

    The world needs to see EM

}


[+]{

    By functions we mean anything that we can represent on the mesh:

    For example:

        *
}


Define a comment symbol.


Inline references with a reason.


## `[arg]{ content }`

[+]{ more detail }                                      Gives more detail about a certain topic
[>sidenote]{ content }                                  Puts a side-note in the margin
[>comment]{ @bricks:comment:io123b2jnv9 }               Reference to a comment stream
[>command]{ content }                                   Simple command around content
[>command(arg1, arg2, ... )]{ content }                 Argumentative command around content
[= prop > 2 ]{ content }                                Evaluative command to boolean which shows the content


## `{{ insert }}`

{{ property }}                                          Inject the property value
{{ property.attribute }}                                Inject the attribute of the property
{{ @citeKey1, @bricks:cite:789123 }}                    Inject a reference

## Extended markdown
content $ma^{th}$ content                               In-line math


## Examples:

### `>command`:
[>math(name="myeq")]{ma^{th}}                           Equation block
[>image(url="myeq")]{ma^{th}}                           Equation block
[>anchor("my-tag")]{ content }                          Anchors a block of content
[>ref("cockett2015", reason="", name="")]{ content }    This should create a citation annotation
H[>sub]{2}O                                             Subscript
[>sub]{2}                                               Superscript


#### These are pluggable:
[>@bricks:rfm/bio-tagger("uid")]{ Mouse }               For example, creating a biological tag to another service.


