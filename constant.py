VARIABLE_DECLARATION_REGEX = r"(int|double|string|char) ([a-z_A-Z0-9]+)( |)(|=( |)([a-zA-Z0-9\"]+))"
VARIABLE_USED = r"\b({0})"
EXPRESSION_PATTERN = r"=[ ]*[a-zA-Z0-9_\[\]]+[ ]*[*\-+\/%]+[ ]*([ ]*[a-zA-Z0-9_\[\]]*[ ]*[*\-+\/%]*[ ]*){2,}"
REPLACE_EXPRESSION_PATTERN = r".+=[ ]*[a-zA-Z0-9_\[\]]+[ ]*[*\-+\/%]+[ ]*([ ]*[a-zA-Z0-9_\[\]]*[ ]*[*\-+\/%]*[ ]*){2,}"
