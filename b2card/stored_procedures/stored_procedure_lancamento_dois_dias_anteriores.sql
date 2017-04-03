DROP PROCEDURE IF EXISTS lancamentos_dois_dia_anterior;
DELIMITER $$
CREATE PROCEDURE lancamentos_dois_dia_anterior ()
BEGIN

	DECLARE done INT DEFAULT FALSE;
	DECLARE id INT;
	DECLARE nome VARCHAR(100);
	DECLARE id_responsavel INT;
	
	DECLARE TEXTO VARCHAR(1000);
	
	DECLARE id_responsaveis CURSOR FOR 
		SELECT pessoa_fisica_id FROM mensagens_responsavel
		WHERE tag = 'D' AND ativo=TRUE;
	
	DECLARE funcionarios CURSOR FOR 
		SELECT p.nome_razao_social, pf.id FROM cadastros_pessoafisica pf
		JOIN cadastros_pessoa p ON (p.id = pf.pessoa_id)
		WHERE pf.notificar_alocacao=TRUE 
		AND WEEKDAY(DATE_SUB(CURDATE(), INTERVAL 2 DAY)) <> 5 -- SABADO 
		AND WEEKDAY(DATE_SUB(CURDATE(), INTERVAL 2 DAY)) <> 6 -- DOMINGO
		AND pf.id NOT IN 
		(SELECT pf.id FROM cadastros_pessoafisica pf
			JOIN cadastros_pessoa p ON (p.id = pf.pessoa_id)
			JOIN cadastros_prestador pr ON (pf.id = pr.pessoa_fisica_id)
			JOIN demandas_atividadeprofissional ap ON (ap.pessoa_fisica_id = pf.id)
			JOIN demandas_alocacaohoras ah ON (ah.atividade_profissional_id = ap.id)
			WHERE (pr.data_inicio <= NOW() AND (data_fim >= NOW() OR data_fim IS NULL))
			AND ah.data_informada = DATE_SUB(CURDATE(), INTERVAL 2 DAY)
			GROUP BY PF.ID
			HAVING SUM(ah.horas_alocadas_milisegundos) >= 28200000); 
		
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
	
	OPEN funcionarios;

	SET TEXTO = '';	
	
	read_loop: LOOP
	    FETCH funcionarios INTO nome, id;
	    IF done THEN
	      LEAVE read_loop;
	    END IF;
	    SET TEXTO = CONCAT(nome, ',', TEXTO);
	    -- INSERT INTO mensagens_mensagem(pessoa_fisica_id, data_criacao, origem,texto, lido, tag) 
		--	VALUES(id, CURDATE(), 'SISTEMA', TEXTO , FALSE, 'A');
	  END LOOP;
	  
	CLOSE funcionarios;
	SET done = FALSE;	
	
	IF NULLIF(TEXTO, '') IS NOT NULL THEN

		OPEN id_responsaveis;

		read_loop: LOOP
		    FETCH id_responsaveis INTO id_responsavel;
		    IF done THEN
		      LEAVE read_loop;
		    END IF;
		    INSERT INTO mensagens_mensagem(pessoa_fisica_id, data_criacao, origem, texto, lido, tag) 
			VALUES(id_responsavel, CURDATE(), 'SISTEMA', CONCAT('Não alocacões na data ', DATE_FORMAT(DATE_SUB(CURDATE(), INTERVAL 2 DAY), '%d/%m/%Y'),': ', TEXTO), FALSE, 'D');
		    
		 END LOOP;
		  
		 CLOSE id_responsaveis;
		
		
	END IF;
	
END $$
DELIMITER ;

CALL lancamentos_dois_dia_anterior;

DROP EVENT IF EXISTS lancamentos_dois_dia_anterior_event;
CREATE EVENT lancamentos_dois_dia_anterior_event
  ON SCHEDULE
    EVERY 1 DAY
    STARTS '2017-03-30 01:00:00' ON COMPLETION PRESERVE ENABLE 
  DO
  	CALL lancamentos_dois_dia_anterior;