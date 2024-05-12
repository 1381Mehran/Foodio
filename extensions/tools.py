from product.models import MainCat, MidCat, SubCat


def category_schema(category):
    if isinstance(category, MainCat):
        return {
            "id": category.id,
            "title": category.title,
            "parent": None
        }
    elif isinstance(category, MidCat):
        return {
            "id": category.id,
            "title": category.title,
            "parent": {
                "id": category.parent.id,
                "title": category.parent.title,
                "parent": None
            }
        }
    elif isinstance(category, SubCat):
        return {
            'id': category.id,
            'title': category.title,
            'parent': {
                'id': category.parent.id,
                'title': category.parent.title,
                'parent': {
                    'id': category.parent.parent.id,
                    'title': category.parent.parent.title,
                    "parent": None
                }
            }
        }
