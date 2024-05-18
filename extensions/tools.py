
def category_schema(category) -> dict:

    # match category.type:
    #
    #     case 'main_cat':
    #         return {
    #             "id": category.id,
    #             "title": category.title,
    #             "active": category.is_active,
    #             "parent": None
    #         }
    #     case 'mid_cat':
    #         category = MidCat.objects.get(id=category.id)
    #
    #         return {
    #             "id": category.id,
    #             "title": category.title,
    #             "active": category.is_active,
    #             "parent": {
    #                 "id": category.parent.id,
    #                 "title": category.parent.title,
    #                 "active": category.parent.is_active,
    #                 "parent": None
    #             }
    #         }
    #     case 'sub_cat':
    #         category = SubCat.objects.get(id=category.id)
    #         return {
    #             'id': category.id,
    #             'title': category.title,
    #             "active": category.is_active,
    #             'parent': {
    #                 'id': category.parent.id,
    #                 'title': category.parent.title,
    #                 "active": category.parent.is_active,
    #                 'parent': {
    #                     'id': category.parent.parent.id,
    #                     'title': category.parent.parent.title,
    #                     "active": category.parent.parent.is_active,
    #                     "parent": None
    #                 }
    #             }
    #         }

    if category.parent:
        if category.parent.parent:
            return {
                        'id': category.id,
                        'title': category.title,
                        "active": category.is_active,
                        'parent': {
                            'id': category.parent.id,
                            'title': category.parent.title,
                            "active": category.parent.is_active,
                            'parent': {
                                'id': category.parent.parent.id,
                                'title': category.parent.parent.title,
                                "active": category.parent.parent.is_active,
                                "parent": None
                            }
                        }
                    }
        else:
            return {
                        "id": category.id,
                        "title": category.title,
                        "active": category.is_active,
                        "parent": {
                            "id": category.parent.id,
                            "title": category.parent.title,
                            "active": category.parent.is_active,
                            "parent": None
                        }
                    }
    else:
        return {
                    "id": category.id,
                    "title": category.title,
                    "active": category.is_active,
                    "parent": None
                }
