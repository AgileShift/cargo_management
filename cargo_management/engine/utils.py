def pluck_child_field(child_rows: list | None, fieldname: str) -> list[str]:
	return [value for row in child_rows or [] if (value := row.get(fieldname))]
