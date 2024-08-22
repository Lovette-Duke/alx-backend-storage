-- creates an index on the table names on the first letter of names and scores

CREATE INDEX idx_name_first_score ON names(name(1), score);
