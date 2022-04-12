# Super Mario Galaxy Object Database
Welcome to the public object database for *Super Mario Galaxy* and *Super Mario Galaxy 2*. Here, we document all objects and classes that can be found in the *Galaxy* games. This includes information about their setup, properties and usage in the game. Everybody can contribute to this project. Please make sure that you've joined the [Luma's Workshop Discord](https://discord.gg/k7ZKzSDsVq) server. That's where major Galaxy modding and documentation takes place.
Here's a short overview of all features:
- Contains information about all objects and their classes.
- Viewable dumps of all object occurrences in any stage.
- Generator for Whitehole's (outdated) Object Database format.

All information about objects and classes are stored in the respective JSON files to keep things organized. For editing, please use the editor instead. It's easier and takes care of potential mistakes. XML files for use with Whitehole can be easily generated as well!

# Setup
If you want to contribute, you have to set up some things. You can find plenty of tutorials regarding the setup of these if you are unsure:
- **Python 3.9** or newer. This specific version is needed for the Whitehole XML generator.
- **PyQt5**, the Qt binding for Python. Install it using ``pip install PyQt5``.
- **qdarkstyle**, the dark mode interface. Install it using ``pip install qdarkstyle``.

# Guideline
- As you can see, information is split between objects and classes. The main information about setups, functionality and parameters belong to the class specifications. Additional information, like a proper name for an object and brief descriptions belong to the object information.
- As of now, we document the objects from Super Mario Galaxy 2 only. Some objects and classes differ from their SMG1 counterparts. It will be hard to keep track of these differences if we mix in the research for both games at once. Therefore, we'll have to finish the SMG2 stuff first. But SMG1's objects and classes will definitely be added in the future.
- **Don't mark a class as finished/complete! I still need to verify if the information is correct by looking into the game's code.**
- There are some class parameters that are only usable by specific objects, for example SunakazeKun's Obj_arg0. You can list any exclusive objects in a parameters "Exclusive" list.
- If you want to specify special values for a parameter, you can do that using the "Values" field. Each line corresponds to a different value.
- Game specific terms should be treated like names. Starbit or starbit becomes Star Bit, coins becomes Coins, ground pound becomes Ground Pound and so on.
- Most of the time, categories are pretty straightforward. However, you may get confused about Stage Parts and Level Features. The former includes objects that you can find in *specific* galaxies. The latter includes stuff like the crystal cages, various decorative objects and reusable assets that may not really be specific to a stage. If you are unsure, just ask me.
- Keep the usage of rounded brackets at a minimum. Put this in square brackets instead. Also, keep naming objects like "Version A" or "Section B" at a minimum. Try to be precise.
- For Stage Parts, make sure to include the name of the stage in the object's descriptive name. Examples: "Rightside Down -- Intro Planet", "Rolling Coaster -- Star Ball Opener", "Battle Belt -- Land Urchin Planet", ...