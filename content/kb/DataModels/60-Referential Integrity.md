title: Object Identifiers and Referential Integrity
publish: 2019-06-15

Even our latest data model contains duplicate data - device names appear in device descriptions and links. For example:

    ---
    hostname: S1
    bgp_as: 65001

CAPTION: Attributes of switch S1

    - prefix: 172.16.0.0/30
      S1: GigabitEthernet0/1
      S2: GigabitEthernet0/1

CAPTION: Link between S1 and S2

Unfortunately it's impossible to remove the last bit of data duplication as we need a mechanism to:

* Uniquely identify an object (what relational database people call *[primary key](https://en.wikipedia.org/wiki/Primary_key)*)
* Refer to an object in another object (what relational database people call *[foreign key](https://en.wikipedia.org/wiki/Foreign_key)*).

The only choice we have is what data we want to use as object identifier. We could:

* Use unique identifiers like numbers or *[Universally Unique Identifiers](https://en.wikipedia.org/wiki/Universally_unique_identifier)* to identify devices and links (*[surrogate key](https://en.wikipedia.org/wiki/Surrogate_key)*)
* Use object attributes like device names or a combination of device and interface names that uniquely identify the object (*[natural key](https://en.wikipedia.org/wiki/Natural_key)*)

You could make *surrogate keys* static - once an object gets a unique identifier, that identifier is never changed. That's harder to do with *natural keys* as object attributes (like node name) can change, forcing you to deal with *[referential integrity](https://en.wikipedia.org/wiki/Referential_integrity)* - making sure that all foreign keys point to valid objects. Relational databases solve the problem automatically assuming that you declared foreign keys in the *[database schema](https://en.wikipedia.org/wiki/Database_schema)*.

You could also decide that you don't want to deal with referential integrity in which case the only chance of remaining consistent is to make sure primary keys never change by either making some object attributes read-only (usually not realistic) or using surrogate keys.

In the end, you have to balance between convenience and consistency. I would usually use unique identifiers (*surrogate keys*) when working with relational databases fronted by business logic (API, GUI, CLI... or all of the above) and hostnames (*natural keys*) when working with text files.

Obviously you have to make sure your data model has referential integrity regardless of how it's implemented. As text files and source code repositories like Git provide no inherent referential integrity mechanism you have to validate input data before using it in your network automation solution. You could perform data validation at multiple points:

* In client-side commit hooks to ensure network operators cannot commit changes that would violate data integrity;
* In CI pipeline to ensure data is checked before a feature branch is merged into the master branch;
* Before data is used by the automation script.

Well-designed systems usually use multiple checkpoints, and I would always validate data just before using it in automation script just to be on the safe side.

We covered data validation and CI/CD pipelines extensively in *[Validation, Error Handling and Unit Tests](https://my.ipspace.net/bin/list?id=NetAutSol&module=5)* part of *[Building Network Automation Solutions](https://www.ipspace.net/Building_Network_Automation_Solutions)* online course.