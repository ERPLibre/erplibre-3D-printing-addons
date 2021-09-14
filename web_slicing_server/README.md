# SuperSlicer Server Infos

---

![](static/description/icon.png)

### The module for managing the information on the location of the SuperSlicer instance that will do all the slicing operations.

---

You can CREATE, UPDATE, DELETE infos.

## Infos are :

- **Address** : _IP_ or _Domain Name_ of the server (default : localhost)
- **Port** : The port the server is listening to (default : 5000)
- **Name** : The identifier of that instance (Useful for multiple instances)
- **Default server** : In order to provide High availability, this information helps to choose the first server to contact. If failed, we try another one. (default : False) [Not in use]
