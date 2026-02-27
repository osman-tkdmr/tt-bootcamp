import duckdb
data = duckdb.execute("select * from read_json('../Data/*.jsonl')").df()
query ="""
SELECT 
    *,
    (CASE WHEN 'İzleGo' = ANY(apps) THEN 1 ELSE 0 END) AS İzleGo,
    (CASE WHEN 'RitimGo' = ANY(apps) THEN 1 ELSE 0 END) AS RitimGo,
    (CASE WHEN 'CüzdanX' = ANY(apps) THEN 1 ELSE 0 END) AS CüzdanX,
    (CASE WHEN 'HızlıPazar' = ANY(apps) THEN 1 ELSE 0 END) AS HızlıPazar,
    (CASE WHEN 'Konuşalım' = ANY(apps) THEN 1 ELSE 0 END) AS Konuşalım
FROM data
"""
unpacked_apps = duckdb.execute(query).df()
unpacked_apps.drop("apps", axis=1, inplace=True)
unpacked_apps.replace({True: 1, False: 0}, inplace=True)
unpacked_apps.to_csv("../Data/all_data.csv", index=False)