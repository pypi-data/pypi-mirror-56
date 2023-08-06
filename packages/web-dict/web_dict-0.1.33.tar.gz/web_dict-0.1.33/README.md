# Parser for Web dictionaries

# Installation
```bash
pip install web-dict
```
# Language Supporting
## Collinsdictionary.com
- class `CollinsDictionary` supports below languages, respectively call method `.en2es` or `.es2en` etc. 

```json
{
    "es": "spanish",
    "zh": "chinese",
    "de": "german",
    "fr": "french",
    "en": "english"
}
```
```python
from web_dict import CollinsDictionary
dict_ = CollinsDictionary()
defs = dict_.es2en(word='hacer')
```

```python
from web_dict import OxfordDictionary
dict_ = OxfordDictionary()
defs = dict_.es(word='hacer')
```

## Lexico.com
    - en-es
    - es-en
    - en
    - es

#### Example Result
```json
{
    "audio": "https://www.collinsdictionary.com/sounds/hwd_sounds/ES-419-W0025780.mp3",
    "defs": [
        {
            "senses": [
                {
                    "senses": [],
                    "examples": [
                        {
                            "sent": "¿qué haces?",
                            "trans": "what are you doing?"
                        },
                        {
                            "sent": "¿qué haces ahí?",
                            "trans": "what are you doing there?"
                        },
                        {
                            "sent": "no sé qué hacer",
                            "trans": "I don’t know what to do"
                        },
                        {
                            "sent": "hace y deshace las cosas a su antojo",
                            "trans": "she does as she pleases"
                        },
                        {
                            "sent": "¡eso no se hace!",
                            "trans": "that’s not done!"
                        },
                        {
                            "sent": "no hizo nada por ayudarnos",
                            "trans": "she didn’t do anything to help us"
                        },
                        {
                            "sent": "haz todo lo posible por llegar a tiempo",
                            "trans": "do everything possible to arrive on time"
                        },
                        {
                            "sent": "no tiene sentido hacer las cosas por hacerlas",
                            "trans": "there’s no point doing things just for the sake of it"
                        }
                    ],
                    "exp": "to do",
                    "syn": {
                        "syn": "",
                        "geo": null
                    },
                    "idioms": [
                        {
                            "orth": "¡qué le vamos a hacer!",
                            "trans": "what can you do?"
                        },
                        {
                            "orth": "hacer algo por hacer",
                            "trans": "there’s no point doing things just for the sake of it"
                        },
                        {
                            "orth": "¡la hemos hecho buena!",
                            "trans": "we’ve really gone and done it now! (informal)"
                        },
                        {
                            "orth": "ya ha hecho otra de las suyas",
                            "trans": "he’s been up to his old tricks again"
                        }
                    ]
                },
                {
                    "senses": [],
                    "examples": [
                        {
                            "sent": "él protestó y yo hice lo mismo",
                            "trans": "he protested and I did the same"
                        },
                        {
                            "sent": "no viene tanto como lo solía hacer",
                            "trans": "he doesn’t come as much as he used to"
                        }
                    ],
                    "exp": "to do",
                    "syn": {
                        "syn": "",
                        "geo": null
                    },
                    "idioms": []
                },
                {
                    "senses": [
                        {
                            "senses": [],
                            "examples": [],
                            "exp": "to make",
                            "syn": {
                                "syn": "",
                                "geo": null
                            },
                            "idioms": []
                        },
                        {
                            "senses": [],
                            "examples": [],
                            "exp": "to build",
                            "syn": {
                                "syn": "",
                                "geo": null
                            },
                            "idioms": []
                        },
                        {
                            "senses": [],
                            "examples": [],
                            "exp": "to do",
                            "syn": {
                                "syn": "",
                                "geo": null
                            },
                            "idioms": []
                        },
                        {
                            "senses": [],
                            "examples": [],
                            "exp": "to write",
                            "syn": {
                                "syn": "",
                                "geo": null
                            },
                            "idioms": []
                        }
                    ],
                    "examples": [
                        {
                            "sent": "hacer dinero",
                            "trans": "to make money"
                        }
                    ],
                    "syn": {
                        "syn": "crear",
                        "geo": null
                    },
                    "idioms": []
                },
                {
                    "senses": [
                        {
                            "senses": [],
                            "examples": [],
                            "exp": "to make",
                            "syn": {
                                "syn": "",
                                "geo": null
                            },
                            "idioms": []
                        },
                        {
                            "senses": [],
                            "examples": [],
                            "exp": "to do",
                            "syn": {
                                "syn": "",
                                "geo": null
                            },
                            "idioms": []
                        },
                        {
                            "senses": [],
                            "examples": [],
                            "exp": "to do",
                            "syn": {
                                "syn": "",
                                "geo": null
                            },
                            "idioms": []
                        },
                        {
                            "senses": [],
                            "examples": [],
                            "exp": "to tie",
                            "syn": {
                                "syn": "",
                                "geo": null
                            },
                            "idioms": []
                        },
                        {
                            "senses": [],
                            "examples": [],
                            "exp": "to ask",
                            "syn": {
                                "syn": "",
                                "geo": null
                            },
                            "idioms": []
                        },
                        {
                            "senses": [],
                            "examples": [],
                            "exp": "to pay",
                            "syn": {
                                "syn": "",
                                "geo": null
                            },
                            "idioms": []
                        },
                        {
                            "senses": [],
                            "examples": [],
                            "exp": "to do; work",
                            "syn": {
                                "syn": "",
                                "geo": null
                            },
                            "idioms": []
                        }
                    ],
                    "examples": [
                        {},
                        {},
                        {
                            "sent": "¿me puedes hacer el nudo de la corbata?",
                            "trans": "could you knot my tie for me?"
                        }
                    ],
                    "syn": {
                        "syn": "realizar",
                        "geo": null
                    },
                    "idioms": []
                },
                {
                    "senses": [
                        {
                            "senses": [],
                            "examples": [],
                            "exp": "to make",
                            "syn": {
                                "syn": "",
                                "geo": null
                            },
                            "idioms": []
                        }
                    ],
                    "examples": [
                        {
                            "sent": "hacer el pelo/las uñas a algn",
                            "trans": "to do sb’s hair/nails"
                        },
                        {
                            "sent": "hacer la barba a algn",
                            "trans": "to trim sb’s beard"
                        }
                    ],
                    "syn": {
                        "syn": "preparar",
                        "geo": null
                    },
                    "idioms": []
                },
                {
                    "senses": [],
                    "examples": [
                        {
                            "sent": "¿qué hace tu padre?",
                            "trans": "what does your father do?"
                        },
                        {
                            "sent": "está haciendo turismo en África",
                            "trans": "he’s gone touring in Africa"
                        }
                    ],
                    "syn": {
                        "syn": "dedicarse a",
                        "geo": null
                    },
                    "idioms": []
                },
                {
                    "senses": [],
                    "examples": [
                        {
                            "sent": "hacer un papel",
                            "trans": "to play a role or part"
                        },
                        {
                            "sent": "hacer el papel de malo",
                            "trans": "to play the (part of the) villain"
                        }
                    ],
                    "syn": {
                        "syn": "actuar",
                        "geo": null
                    },
                    "idioms": []
                },
                {
                    "senses": [],
                    "examples": [
                        {
                            "sent": "6 y 3 hacen 9",
                            "trans": "6 and 3 make 9"
                        },
                        {
                            "sent": "este hace 100",
                            "trans": "this one makes 100"
                        },
                        {
                            "sent": "y cincuenta céntimos, hacen diez euros",
                            "trans": "and fifty cents change, which makes ten euros"
                        },
                        {
                            "sent": "este hace el corredor número 100 en atravesar la meta",
                            "trans": "he’s the 100th runner to cross the finishing line"
                        }
                    ],
                    "exp": "to make",
                    "syn": {
                        "syn": "sumar",
                        "geo": null
                    },
                    "idioms": []
                },
                {
                    "senses": [],
                    "examples": [
                        {}
                    ],
                    "syn": {
                        "syn": "cumplir",
                        "geo": null
                    },
                    "idioms": []
                },
                {
                    "senses": [
                        {
                            "senses": [],
                            "examples": [],
                            "exp": "to make",
                            "syn": {
                                "syn": "",
                                "geo": null
                            },
                            "idioms": []
                        }
                    ],
                    "examples": [
                        {
                            "sent": "les hice venir",
                            "trans": "I made them come"
                        },
                        {
                            "sent": "siempre consigue hacerme reír",
                            "trans": "she always manages to make me laugh"
                        },
                        {
                            "sent": "le gustaba hacerme rabiar",
                            "trans": "he enjoyed making me mad"
                        },
                        {
                            "sent": "yo haré que vengan",
                            "trans": "I’ll make sure they come"
                        }
                    ],
                    "syn": {
                        "syn": "obligar",
                        "geo": null
                    },
                    "idioms": []
                },
                {
                    "senses": [],
                    "examples": [
                        {
                            "sent": "hizo construirse un palacio",
                            "trans": "she had a palace built"
                        },
                        {
                            "sent": "hicieron pintar la fachada del colegio",
                            "trans": "they had the front of the school painted"
                        }
                    ],
                    "syn": {
                        "syn": "mandar",
                        "geo": null
                    },
                    "idioms": []
                },
                {
                    "senses": [
                        {
                            "senses": [],
                            "examples": [],
                            "exp": "to make",
                            "syn": {
                                "syn": "",
                                "geo": null
                            },
                            "idioms": []
                        }
                    ],
                    "examples": [
                        {
                            "sent": "esto lo hará más difícil",
                            "trans": "this will make it more difficult"
                        },
                        {
                            "sent": "hacer feliz a algn",
                            "trans": "to make sb happy"
                        },
                        {
                            "sent": "te hace más delgado",
                            "trans": "it makes you look slimmer"
                        },
                        {
                            "sent": "has hecho de mí un hombre muy feliz",
                            "trans": "you’ve made me a very happy man"
                        }
                    ],
                    "syn": {
                        "syn": "transformar",
                        "geo": null
                    },
                    "idioms": []
                },
                {
                    "senses": [],
                    "examples": [
                        {},
                        {
                            "sent": "te hacíamos en el Perú",
                            "trans": "we thought you were in Peru"
                        }
                    ],
                    "exp": "to think",
                    "syn": {
                        "syn": "pensar",
                        "geo": null
                    },
                    "idioms": []
                },
                {
                    "senses": [],
                    "examples": [
                        {
                            "sent": "hacer el cuerpo al frío",
                            "trans": "to get one’s body used to the cold"
                        }
                    ],
                    "syn": {
                        "syn": "acostumbrar",
                        "geo": null
                    },
                    "idioms": []
                },
                {
                    "senses": [],
                    "examples": [
                        {
                            "sent": "hacer dedos",
                            "trans": "to do finger exercises"
                        },
                        {
                            "sent": "hacer piernas",
                            "trans": "to stretch one’s legs"
                        }
                    ],
                    "syn": {
                        "syn": "ejercitar",
                        "geo": null
                    },
                    "idioms": []
                },
                {
                    "senses": [],
                    "examples": [
                        {
                            "sent": "me hizo con dinero",
                            "trans": "he provided me with money"
                        }
                    ],
                    "syn": {
                        "syn": "proveer",
                        "geo": null
                    },
                    "idioms": []
                }
            ],
            "pos": "transitive verb",
            "misc": "indicando actividad en general"
        },
        {
            "senses": [
                {
                    "senses": [],
                    "examples": [
                        {
                            "sent": "haces bien en esperar",
                            "trans": "you’re right to wait"
                        },
                        {
                            "sent": "haces mal no contestando a sus llamadas",
                            "trans": "it’s wrong of you not to answer his calls"
                        },
                        {},
                        {
                            "sent": "hizo como si me fuera a pegar",
                            "trans": "he made as if to strike me"
                        }
                    ],
                    "syn": {
                        "syn": "comportarse",
                        "geo": null
                    },
                    "idioms": []
                },
                {
                    "senses": [],
                    "examples": [
                        {
                            "sent": "dieron que hacer a la policía",
                            "trans": "they caused or gave the police quite a bit of trouble"
                        }
                    ],
                    "syn": {
                        "syn": "",
                        "geo": null
                    },
                    "idioms": []
                },
                {
                    "senses": [],
                    "examples": [
                        {}
                    ],
                    "syn": {
                        "syn": "importar",
                        "geo": null
                    },
                    "idioms": [
                        {
                            "orth": "¡no le hagas!",
                            "trans": "don’t give me that! (informal)"
                        }
                    ]
                },
                {
                    "senses": [],
                    "examples": [
                        {},
                        {
                            "sent": "la llave hace a todas las puertas",
                            "trans": "the key fits all the doors"
                        },
                        {
                            "sent": "hace a todo",
                            "trans": "he’s good for anything"
                        }
                    ],
                    "syn": {
                        "syn": "ser apropiado",
                        "geo": null
                    },
                    "idioms": []
                },
                {
                    "senses": [],
                    "examples": [
                        {},
                        {}
                    ],
                    "syn": {
                        "syn": "apetecer",
                        "geo": null
                    },
                    "idioms": []
                },
                {
                    "senses": [],
                    "examples": [
                        {
                            "sent": "hacer de malo",
                            "trans": "to play the villain"
                        },
                        {
                            "sent": "haz por verlo si puedes",
                            "trans": "try to get round to seeing him if you can"
                        },
                        {}
                    ],
                    "syn": {
                        "syn": "intentar",
                        "geo": null
                    },
                    "idioms": []
                }
            ],
            "pos": "intransitive verb",
            "misc": "seguido de preposición"
        },
        {
            "senses": [
                {
                    "senses": [],
                    "examples": [
                        {
                            "sent": "hace calor/frío",
                            "trans": "it’s hot/cold"
                        },
                        {
                            "sent": "hizo dos grados bajo cero",
                            "trans": "it was two degrees below zero"
                        },
                        {
                            "sent": "¿qué tiempo hace?",
                            "trans": "what’s the weather like?"
                        },
                        {
                            "sent": "ojalá haga buen tiempo",
                            "trans": "I hope the weather’s nice"
                        }
                    ],
                    "exp": "to be",
                    "syn": {
                        "syn": "",
                        "geo": null
                    },
                    "idioms": []
                },
                {
                    "senses": [],
                    "examples": [
                        {},
                        {},
                        {
                            "sent": "ha estado aquí hasta hace poco",
                            "trans": "he was here only a short while ago"
                        },
                        {
                            "sent": "no hace mucho",
                            "trans": "not long ago"
                        },
                        {
                            "sent": "hace un mes que voy",
                            "trans": "I’ve been going for a month"
                        },
                        {
                            "sent": "¿hace mucho que esperas?",
                            "trans": "have you been waiting long?"
                        },
                        {
                            "sent": "hace de esto varios años",
                            "trans": "it is some years since this happened"
                        },
                        {
                            "sent": "está perdido desde hace 15 días",
                            "trans": "it’s been missing for a fortnight"
                        }
                    ],
                    "syn": {
                        "syn": "",
                        "geo": null
                    },
                    "idioms": []
                },
                {
                    "senses": [],
                    "examples": [
                        {
                            "sent": "hace sed",
                            "trans": "I’m thirsty"
                        },
                        {
                            "sent": "hace sueño",
                            "trans": "I’m sleepy"
                        }
                    ],
                    "syn": {
                        "syn": "haber, tener",
                        "geo": "Latin America"
                    },
                    "idioms": []
                }
            ],
            "pos": "impersonal verb",
            "misc": "con expresiones de tiempo atmosférico"
        }
    ],
    "rank": 5,
    "head_word": "hacer"
}


```
