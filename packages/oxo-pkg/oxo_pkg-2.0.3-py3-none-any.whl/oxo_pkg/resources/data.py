
# Data/Resources

all_move_keys = ["topLeft", "topMid", "topRight", "midLeft", "midMid", "midRight", "bottomLeft", "bottomMid", "bottomRight"]

possible_input = ["tl", "tm", "tr", "ml", "mm", "mr", "bl", "bm", "br"]

# dictionary - key value pairs
moves_map = {
    "tl": "topLeft",
    "tm": "topMid",
    "tr": "topRight",
    "ml": "midLeft",
    "mm": "midMid",
    "mr": "midRight",
    "bl": "bottomLeft",
    "bm": "bottomMid",
    "br": "bottomRight",
}

possible_wins = [
    ["topLeft", "topMid", "topRight"],
    ["midLeft", "midMid", "midRight"],
    ["bottomLeft", "bottomMid", "bottomRight"],
    ["topLeft", "midLeft", "bottomLeft"],
    ["topMid", "midMid", "bottomMid"],
    ["topRight", "midRight", "bottomRight"],
    ["topRight", "midMid", "bottomLeft"],
    ["topLeft", "midMid", "bottomRight"],
]

yes_answers = [ "yes", "y", "yep", "yeah", "yasss", "si", "oui" ]

no_answers = [ "no", "n", "nope", "nah", "na", "non" ]