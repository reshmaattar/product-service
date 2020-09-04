product = {
    "type": "object",
    "required": ["name", "qty","price"],
    "properties": {
        "name": {
            "type": "string",
            "maxLength": 255,
            "minLength": 4
        },
        "qty": {
            "type": "integer",
            "minimum": 0
        },"price": {
            "type": "number"
        }
        }
}
