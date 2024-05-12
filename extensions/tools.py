
def category_schema(category):

    match category.type:

        case 'main_cat':
            return {
                "id": category.id,
                "title": category.title,
                "parent": None
            }
        case 'mid_cat':
            return {
                "id": category.id,
                "title": category.title,
                "parent": {
                    "id": category.parent.id,
                    "title": category.parent.title,
                    "parent": None
                }
            }
        case 'sub_cat':
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
