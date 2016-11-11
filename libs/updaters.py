from libs import constants, helpers

def update_summary(summary):
    return summary

def update_description(description):
    return helpers.parse_description(description)

def update_type(tipoDefeito):
    return constants.type_map[tipoDefeito]

def update_priority(prioridade):
    return constants.priority_map[prioridade], constants.severity_map[prioridade]

def update_componente(LT, componente):
    return helpers.get_component(LT, componente)

def update_platform(platform):
    return helpers.get_platform(platform)

update_functions = {
    "summary": update_summary,
    "description": update_description,
    "tipoDefeito": update_type,
    "prioridade": update_priority,
    "componente": update_componente,
    "platform": update_platform
}