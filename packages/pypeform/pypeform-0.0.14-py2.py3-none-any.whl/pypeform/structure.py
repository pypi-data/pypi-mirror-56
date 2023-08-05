from .models import Answer, Field, ActionGraph, Category
from typing import List, Dict


def _depth_first_search(field: Field):
    stack = [field]

    while stack:
        field = stack.pop()

        if not field.has_sub_fields():
            continue

        num = 0

        prev_field = None
        for sub_field_raw in field.properties['properties']['fields']:
            index_letter = chr(ord('a') + num)
            if sub_field_raw['type'] != 'statement':
                num += 1
            else:
                index_letter = f'statement-{index_letter}'

            sub_field = Field(f'{field.index}.{index_letter}', **sub_field_raw)

            if prev_field:
                prev_field.next_within_group = sub_field

            prev_field = sub_field
            field.children.append(sub_field)
            stack.append(sub_field)


def parse_fields(fields_raw: dict):
    num = 1
    for field_raw in fields_raw:
        if field_raw['type'] != 'statement':
            index = num
            num += 1
        else:
            index = f'statement-{num}'
        _depth_first_search(Field(f'{index}', **field_raw))

    return Field.lookup


def _parse_logic(logic_raw: dict):
    for logic in logic_raw:
        source_ref = logic['ref']

        for action in logic['actions']:
            action_type = action['action']
            if action_type != 'jump':
                # unsupported if not jump
                continue

            target_ref = action['details']['to']['value']
            condition = action['condition']
            yield source_ref, target_ref, condition


def parse_categories(category_data):
    for category_info in category_data:
        category = Category()
        category.name  = category_info['name']
        category.id = category_info['id']
        category.ids = category_info['ids']
        category.color = category_info['color'] if 'color' in category_info else None
        category.graph = category_info['graph'] if 'graph' in category_info else True


def create_action_graph(logic: dict) -> ActionGraph:
    graph = ActionGraph()

    for source_ref, target_ref, condition in _parse_logic(logic):
        graph.add_by_ref(source_ref, target_ref, condition)

    for category in Category.categories:
        n = len(category.ids)
        for i, j in enumerate(category.ids):
            graph.add_by_index(j, category.ids[(i + 1) % n], 'category')

    return graph


def parse_form_response(form_response: dict):
    Answer.submitted_timestamp = form_response['form_response']['submitted_at']
    answers = []
    for answer_raw in form_response['form_response']['answers']:
        answers.append(Answer(**answer_raw))

    return answers


