# SQLAlchemy-OrderingItem

SQLAlchemy-OrderingItem provides an OrderingItem base for children of [`orderinglist`](https://docs.sqlalchemy.org/en/13/orm/extensions/orderinglist.html) relationships. Children of `orderinglist` relationships will exhibit more intuitive behavior when setting their parent attribute.

## License

Publications which use this software should include the following citation for SQLAlchemy-OrderingItem:

Bowen, D.S. (2019). SQLAlchemy-OrderingItem \[Computer software\]. [https://dsbowen.github.io/sqlalchemy-orderingitem](https://dsbowen.github.io/sqlalchemy-orderingitem).

This project is licensed under the MIT License [LICENSE](https://github.com/dsbowen/sqlalchemy-orderingitem/blob/master/LICENSE).

## Example

Suppose we have a `child` of an `orderinglist` relationship. The `orderinglist` sorts childen on their `index` column.

Ordinary behavior:

```python
child.parent = parent
print(child.index)
```

Outputs:

```
None
```

Behavior with the `OrderingItem` subclass:

```python
child.parent = parent
print(child.index)
```

Outputs:

```
0
```