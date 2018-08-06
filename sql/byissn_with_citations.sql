
SELECT issn.identifier_value, count(*)
FROM wos_dynamic_identifiers issn, wos_summary_names names, wos_summary article, wos_references citation
WHERE article.id = issn.id
    AND issn.identifier_type = 'issn'
    AND issn.identifier_value IN (
        '1471-003X','0006-8950','1758-8928','0166-2236','1863-2653','0898-929X','0022-3077','0301-0511','0896-0267','0256-7040','0270-6474','0896-6273','1097-6256','1047-3211','0006-8950','1053-8119','1065-9471','0010-9452','0953-816X','1359-5962','0014-4819','0028-3932','0147-006X'
    )
    AND article.id = names.id
    AND (names.seq_no = '1' OR names.seq_no = article.name_count)
    AND article.id = citation.id
    AND citation.ref_id NOT LIKE '%.%'
GROUP BY issn.identifier_value
ORDER BY issn.identifier_value;
