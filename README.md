# Super Mario Galaxy Object Database
Here, you can find the data for the *Super Mario Galaxy* and *Super Mario Galaxy 2* object database. This project aims to document all objects and classes that can be found in the two *Galaxy* games. This includes information about their setup, properties and occurrences in the games. The database can also be used in level editors, such as [Whitehole Despaghettification](https://github.com/SunakazeKun/Whitehole-Despaghettification).

Everybody can contribute to this project, just contact *Aurum* on the [Luma's Workshop Discord](https://discord.gg/k7ZKzSDsVq) server. That's where the majority of SMG1/2 modding and documentation takes place. However, please make sure that you've read the guideline that can be found in this document.

# Achievements
Below is a table of important achievements earned while working on the project:

|Achievement|Date|
|-|-|
|Project started|8th April 2022|
|All 2446 objects finished|2nd May 2022|
|50% of SMG2 classes finished|20th July 2022|
|100% of SMG2 classes finished|*n/a*|

# Setup
If you want to contribute, you have to set up a few things. You can find several tutorials regarding the setups of Python and PyQt5 on the internet if you're unsure. The required components are:
- **Python 3.10** or newer.
- **PyQt5**, the Qt binding for Python. You can install it with pip: ``pip install PyQt5``.
- **[OPTIONAL] qdarkstyle**, a dark mode theme. Install it using ``pip install qdarkstyle``.

# Guideline
- Always use the editor instead of editing the JSON files! The editor is easier to use, takes care of mistakes and regenerates the HTML pages.
- **Don't mark a config as finished/complete! I still want to verify the information by looking into the game's code and files.**
- There are some parameters that are only usable by specific objects, for example SunakazeKun's Obj_arg0. You can list any exclusive objects in a parameters "Exclusive" list.
- If you want to specify special values for a parameter, you can do that using the "Values" field. Each line corresponds to a different value.
- Game specific terms should be treated like names. Starbit or starbit becomes Star Bit, coins becomes Coins, ground pound becomes Ground Pound and so on.
- Keep the usage of rounded brackets at a minimum. Put this in square brackets instead. Also, keep naming objects like "Version A" or "Section B" at a minimum. Try to be precise.
- For Stage Parts, make sure to include the name of the stage in the object's descriptive name. Examples: "Rightside Down -- Intro Planet", "Rolling Coaster -- Star Ball Opener", "Battle Belt -- Land Urchin Planet", ...