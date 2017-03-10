CREATE ALGORITHM = MERGE VIEW vw_alocacao_previsto_orcado AS
SELECT 
'Alocacao' AS TIPO,
d.id AS DEMANDA_ID,
pj.id AS CLIENTE_ID,
cc.id AS CENTRO_CUSTO_ID,
un.id AS UN_ID,
gestor.id AS GESTOR_ID,
a.id AS ATIVIDADE_ID,
f.id AS FASE_ID,
cr.id AS CENTRO_RESULTADO_ID,
responsavelfase.id AS ID_RESPONSAVEL_TECNICO,
profissional.id AS PROFISSIONAL_ID,
ah.id AS ALOCACAO_HORAS_ID,
cp.id AS CUSTO_PRESTADOR_ID,
sd.descricao AS STATUS_DEMANDA,
0 AS VALOR_DESPESA_ORCADA,
d.data_criacao AS DATA_ABERTURA_DEMANDA,
0 AS HORAS_ORCADAS,
0 AS VALOR_HORAS_ORCADAS,
0 AS VALOR_ADMINISTRATIVO_ORCADO,
0 AS HORAS_PREVISTAS,
0 AS VALOR_HORAS_PREVISTAS,
0 AS VALOR_ADMINISTRATIVO_PREVISTO,
TRUNCATE((ah.horas_alocadas_milisegundos / 1000 / 60 / 60 ), 2) AS HORAS_ALOCADAS,
TRUNCATE((cp.valor * TRUNCATE((ah.horas_alocadas_milisegundos / 1000 / 60 / 60 ), 2)), 2) AS VALOR_HORAS_ALOCADAS,
TRUNCATE((un.custo_operacao_hora * TRUNCATE((ah.horas_alocadas_milisegundos / 1000 / 60 / 60 ), 2)), 2) AS VALOR_ADMINISTRATIVO_ALOCADO,
ah.data_informada AS DATA_INFORMADA_LANCAMENTO,
0 AS VALOR_DESPESA,
0 AS TIPO_DESPESA
FROM demandas_demanda AS d
LEFT OUTER JOIN cadastros_pessoajuridica pj ON (d.cliente_id = pj.id)
LEFT OUTER JOIN cadastros_pessoa p ON (p.id = pj.pessoa_id)
LEFT OUTER JOIN cadastros_apropriacao ca ON (ca.pessoa_id = p.id)
LEFT OUTER JOIN cadastros_centrocusto cc ON (ca.centro_custo_id = cc.id)
LEFT OUTER JOIN cadastros_unidadeadministrativa un ON (d.unidade_administrativa_id = un.id)
LEFT OUTER JOIN cadastros_pessoafisica gestor ON (d.responsavel_id = gestor.id)
LEFT OUTER JOIN demandas_faseatividade fa ON (fa.demanda_id = d.id)
LEFT OUTER JOIN cadastros_pessoafisica responsavelfase ON (responsavelfase.id = fa.responsavel_id)
LEFT OUTER JOIN demandas_atividade a ON (fa.id = a.fase_atividade_id)
LEFT OUTER JOIN cadastros_fase f ON (f.id = fa.fase_id)
LEFT OUTER JOIN cadastros_centroresultado cr ON (f.centro_resultado_id = cr.id)
LEFT OUTER JOIN demandas_atividadeprofissional ap ON (ap.atividade_id = a.id)
LEFT OUTER JOIN cadastros_pessoafisica profissional ON (profissional.id = ap.pessoa_fisica_id)
JOIN demandas_alocacaohoras ah ON (ah.atividade_profissional_id = ap.id)
-- join cadastros_prestador cp on (cp.pessoa_fisica_id = profissional.id)
LEFT OUTER JOIN cadastros_custoprestador cp ON (cp.pessoa_fisica_id = profissional.id)
JOIN STATUS_DEMANDA sd ON (sd.codigo = d.status_demanda)
WHERE cp.data_inicio <= ah.data_informada AND (cp.data_fim IS NULL OR cp.data_fim >= ah.data_informada)
UNION ALL
SELECT 
'Previsto' AS TIPO,
d.id AS DEMANDA_ID,
pj.id AS CLIENTE_ID,
cc.id AS CENTRO_CUSTO_ID,
un.id AS UN_ID,
gestor.id AS GESTOR_ID,
a.id AS ATIVIDADE_ID,
f.id AS FASE_ID,
cr.id AS CENTRO_RESULTADO_ID,
responsavelfase.id AS ID_RESPONSAVEL_TECNICO,
profissional.id AS PROFISSIONAL_ID,
0 AS ALOCACAO_HORAS_ID,
cp.id AS CUSTO_PRESTADOR_ID,
sd.descricao AS STATUS_DEMANDA,
0 AS VALOR_DESPESA_ORCADA,
d.data_criacao AS DATA_ABERTURA_DEMANDA,
0 AS HORAS_ORCADAS,
0 AS VALOR_HORAS_ORCADAS,
0 AS VALOR_ADMINISTRATIVO_ORCADO,
ap.quantidade_horas AS HORAS_PREVISTAS,
TRUNCATE(cp.valor * ap.quantidade_horas, 2) AS VALOR_HORAS_PREVISTAS,
TRUNCATE(un.custo_operacao_hora * ap.quantidade_horas, 2) AS VALOR_ADMINISTRATIVO_PREVISTO,
0 AS HORAS_ALOCADAS,
0 AS VALOR_HORAS_ALOCADAS,
0 AS VALOR_ADMINISTRATIVO_ALOCADO,
d.data_criacao AS DATA_INFORMADA_LANCAMENTO,
0 AS VALOR_DESPESA,
0 AS TIPO_DESPESA
FROM demandas_demanda AS d
LEFT OUTER JOIN cadastros_pessoajuridica pj ON (d.cliente_id = pj.id)
LEFT OUTER JOIN cadastros_pessoa p ON (p.id = pj.pessoa_id)
LEFT OUTER JOIN cadastros_apropriacao ca ON (ca.pessoa_id = p.id)
LEFT OUTER JOIN cadastros_centrocusto cc ON (ca.centro_custo_id = cc.id)
LEFT OUTER JOIN cadastros_unidadeadministrativa un ON (d.unidade_administrativa_id = un.id)
LEFT OUTER JOIN cadastros_pessoafisica gestor ON (d.responsavel_id = gestor.id)
LEFT OUTER JOIN demandas_faseatividade fa ON (fa.demanda_id = d.id)
LEFT OUTER JOIN cadastros_pessoafisica responsavelfase ON (responsavelfase.id = fa.responsavel_id)
LEFT OUTER JOIN demandas_atividade a ON (fa.id = a.fase_atividade_id)
LEFT OUTER JOIN cadastros_fase f ON (f.id = fa.fase_id)
LEFT OUTER JOIN cadastros_centroresultado cr ON (f.centro_resultado_id = cr.id)
LEFT OUTER JOIN demandas_atividadeprofissional ap ON (ap.atividade_id = a.id)
LEFT OUTER JOIN cadastros_pessoafisica profissional ON (profissional.id = ap.pessoa_fisica_id)
-- JOIN demandas_alocacaohoras ah ON (ah.atividade_profissional_id = ap.id)
-- join cadastros_prestador cp on (cp.pessoa_fisica_id = profissional.id)
LEFT OUTER JOIN cadastros_custoprestador cp ON (cp.pessoa_fisica_id = profissional.id)
JOIN STATUS_DEMANDA sd ON (sd.codigo = d.status_demanda)
WHERE cp.data_inicio <= d.data_criacao AND (cp.data_fim IS NULL OR cp.data_fim >= d.data_criacao)
UNION ALL
SELECT 
'Orcado' AS TIPO,
d.id AS DEMANDA_ID,
pj.id AS CLIENTE_ID,
cc.id AS CENTRO_CUSTO_ID,
un.id AS UN_ID,
gestor.id AS GESTOR_ID,
0 AS ATIVIDADE_ID,
f.id AS FASE_ID,
cr.id AS CENTRO_RESULTADO_ID,
0 AS ID_RESPONSAVEL_TECNICO,
0 AS PROFISSIONAL_ID,
0 AS ALOCACAO_HORAS_ID,
0 AS CUSTO_PRESTADOR_ID,
sd.descricao AS STATUS_DEMANDA,
orc.total_despesas AS VALOR_DESPESA_ORCADA,
d.data_criacao AS DATA_ABERTURA_DEMANDA,
SUM(itf.quantidade_horas) AS HORAS_ORCADAS,
SUM((	
	SELECT itf.quantidade_horas * vi.valor FROM cadastros_valorhora vh 
	LEFT JOIN cadastros_vigencia vi ON (vi.valor_hora_id = vh.id) 
	WHERE vi.data_inicio <= d.data_criacao AND (vi.data_fim IS NULL OR vi.data_fim >= d.data_criacao)
	AND itf.valor_hora_id = vh.id
)) AS VALOR_HORAS_ORCADAS,
un.custo_operacao_hora * SUM(itf.quantidade_horas) AS VALOR_ADMINISTRATIVO_ORCADO,
0 AS HORAS_PREVISTAS,
0 AS VALOR_HORAS_PREVISTAS,
0 AS VALOR_ADMINISTRATIVO_PREVISTO,
0 AS HORAS_ALOCADAS,
0 AS VALOR_HORAS_ALOCADAS,
0 AS VALOR_ADMINISTRATIVO_ALOCADO,
d.data_criacao AS DATA_INFORMADA_LANCAMENTO,
0 AS VALOR_DESPESA,
0 AS TIPO_DESPESA
FROM demandas_demanda AS d
LEFT OUTER JOIN cadastros_pessoajuridica pj ON (d.cliente_id = pj.id)
LEFT OUTER JOIN cadastros_pessoa p ON (p.id = pj.pessoa_id)
LEFT OUTER JOIN cadastros_apropriacao ca ON (ca.pessoa_id = p.id)
LEFT OUTER JOIN cadastros_centrocusto cc ON (ca.centro_custo_id = cc.id)
LEFT OUTER JOIN cadastros_unidadeadministrativa un ON (d.unidade_administrativa_id = un.id)
LEFT OUTER JOIN cadastros_pessoafisica gestor ON (d.responsavel_id = gestor.id)
-- LEFT OUTER JOIN demandas_faseatividade fa ON (fa.demanda_id = d.id)
-- LEFT OUTER JOIN demandas_atividade a ON (fa.id = a.fase_atividade_id)

-- LEFT OUTER JOIN demandas_atividadeprofissional ap ON (ap.atividade_id = a.id)
-- LEFT OUTER JOIN cadastros_pessoafisica profissional ON (profissional.id = ap.pessoa_fisica_id)
LEFT OUTER JOIN demandas_orcamento orc ON (d.id = orc.demanda_id)
LEFT OUTER JOIN demandas_orcamentofase orcf ON (orc.id = orcf.orcamento_id)
LEFT OUTER JOIN demandas_itemfase itf ON (orcf.id = itf.orcamento_fase_id)
-- left outer join cadastros_valorhora vh on (itf.valor_hora_id = vh.id)
-- left outer join cadastros_vigencia vi on (vi.valor_hora_id = vh.id)
LEFT OUTER JOIN cadastros_fase f ON (orcf.fase_id = f.id)
LEFT OUTER JOIN cadastros_centroresultado cr ON (f.centro_resultado_id = cr.id)
-- JOIN demandas_alocacaohoras ah ON (ah.atividade_profissional_id = ap.id)
-- join cadastros_prestador cp on (cp.pessoa_fisica_id = profissional.id)
-- LEFT OUTER JOIN cadastros_custoprestador cp ON (cp.pessoa_fisica_id = profissional.id)
JOIN STATUS_DEMANDA sd ON (sd.codigo = d.status_demanda)
-- WHERE vi.data_inicio <= d.data_criacao AND (vi.data_fim IS NULL OR vi.data_fim >= d.data_criacao)
GROUP BY orc.id, d.id