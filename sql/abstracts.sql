SELECT issn.id, doi.identifier_value, t.title, abs.paragraph_text 
FROM wos_dynamic_identifiers issn, wos_dynamic_identifiers doi, wos_abstract_paragraphs abs, wos_titles t 
WHERE issn.id = t.id
    AND issn.id = abs.id
    AND t.title_type = 'item'
    AND wdi.identifier_type = 'issn'
    AND wdi.identifier_value IN (
        '1863-2661', '1530-8898', '0022-3077', '0301-0511', '0094-9345', '1573-6792', '1433-0350', '1460-9568', '1662-5129', '1432-1106', '0028-3932'
    )
    AND issn.id = doi.id
    AND doi.identifier_type = 'doi';