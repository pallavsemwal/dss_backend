import json
from ...models.lawAndOrder import LawAndOrder


def get_arrangement(situation_type, configuration):
    filtered_situations = LawAndOrder.objects.filter(situation_type=situation_type)
    # suggest some good arrangement based on event clustering and all
    # for now its just returning the first database entry
    for situation in filtered_situations:
        return situation.arrangements
    return json.loads('[{"type": "paragraph", "children": [{"bold": true, "text": "We are extremely sorry, ' \
                      'can\'t recommend anything at the moment :("}]}, {"type": "paragraph", "children": [{"text": ' \
                      '""}]}] ')
