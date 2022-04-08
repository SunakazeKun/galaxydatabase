# Super Mario Galaxy Object Database
Welcome to the public object database for *Super Mario Galaxy* and *Super Mario Galaxy 2*. Here, we document all objects and classes that can be found in the *Galaxy* games. This includes information about their setup, properties and usage in the game. Everybody can contribute to this project. Please make sure that you've joined the [Luma's Workshop Discord](https://discord.gg/k7ZKzSDsVq) server. That's where major Galaxy modding and documentation takes place.
All information about objects and classes are stored in the respective JSON files to keep things organized. For editing, please use the editor instead. It's easier and takes care of potential mistakes. XML files for use with Whitehole can be easily generated as well!
Here's a short overview of its features:
- Information about all objects and classes
- Dumps of all object occurrences in the levels
- Generator for Whitehole's (outdated) Object Database format

# How can I contribute?
Everybody can contribute through pull requests. Trusted contributors may also get direct push access in the future. The tools are programmed in Python, so there are a couple of things that you'll have to set up first:
- **Python 3.9**.
- **PyQt5**, the Qt binding for Python. Install it using ``pip install PyQt5``.
- **qdarkstyle**, the dark mode interface. Install it using ``pip install qdarkstyle``.

Once you've installed everything. Just launch the **editor.py** file. You should always use the editor to make changes.

# Editing Guideline
- As you can see, information is split between objects and classes. The main information about setups, functionality and parameters belong to the class specification. Additional information, like a proper name for an object and brief descriptions belong to the object information.
- As of now, we document the objects from Super Mario Galaxy 2 only. Some objects and classes differ from their SMG1 counterparts. It will be hard to keep track of these differences if we mix in the research for both games at once. Therefore, we'll have to finish the SMG2 stuff first. But SMG1's objects and classes will definitely be added in the future.
- There are some class parameters that are only usable by specific objects, for example SunakazeKun's Obj_arg0. You can list any exclusive objects in a parameters "Exclusive" list.
- If you want to specify special values for a parameter, you can do that using the "Values" field. Each line corresponds to a different value.


# Okay, but I just want the XML file for Whitehole.
Sure thing. Just download the ``objectdb.xml`` from the repository and place it in Whitehole's folder.

# Why is it not web-based?
Previous object databases for the games were in-browser. Due to past events, those were taken down and we were left with nothing. Therefore, a quick solution had to be implemented. As I don't have the free time to invest into learning web development and respective languages, I had to improvise a bit. It was much easier for me to create a small Python application instead. I also think it's more helpful to keep this open source so that we'll never loose track or any data again.