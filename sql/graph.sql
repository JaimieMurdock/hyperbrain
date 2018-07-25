SELECT article.id, names.name_id, names.seq_no, names.wos_standard, article.sortdate
FROM wos_dynamic_identifiers issn, wos_summary_names names, wos_summary article
WHERE article.id = issn.id
    AND issn.identifier_type = 'issn'
    AND issn.identifier_value IN (
        '0028-3932', '1471-003X', '0006-8950', '1758-8928', '0166-2236'
    )
    AND article.id = names.id
    AND (names.seq_no = 1 OR names.seq_no = article.name_count);