DROP PROCEDURE IF EXISTS parcela_pagamento;
DELIMITER $$
CREATE PROCEDURE parcela_pagamento ()
BEGIN

	DECLARE done INT DEFAULT FALSE;
	DECLARE id INT;
	DECLARE nome_demanda VARCHAR(1000);
	DECLARE descricao VARCHAR(1000);
	DECLARE data_previsto DATE;
	DECLARE id_responsavel INT;
	
	DECLARE TEXTO VARCHAR(1000);
	
	DECLARE id_responsaveis CURSOR FOR 
		SELECT pessoa_fisica_id FROM mensagens_responsavel
		WHERE tag = 'G' AND ativo=TRUE;

	DECLARE parcela_pagamento CURSOR FOR
		SELECT d.id, d.nome_demanda, p.descricao, p.data_previsto_pagamento FROM faturamento_parcela p
			JOIN demandas_demanda d ON (d.id = p.demanda_id)	
			WHERE p.data_pagamento IS NULL AND p.data_previsto_pagamento <= CURDATE();
		
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
	
	DELETE FROM mensagens_mensagem WHERE tag='G';
	
	OPEN parcela_pagamento;

	SET TEXTO = '';	
	
	read_loop: LOOP
	    FETCH parcela_pagamento INTO id, nome_demanda, descricao, data_previsto;
	    IF done THEN
	      LEAVE read_loop;
	    END IF;
	    SET TEXTO = CONCAT(LPAD(id, 5, '0'), ' - ', nome_demanda, ' - ', descricao, ' (', IF(data_previsto IS NOT NULL, DATE_FORMAT(data_previsto, '%d/%m/%Y'),'Sem data previsto'), '), ', TEXTO);
	  END LOOP;
	  
	CLOSE parcela_pagamento;
	
	SET done = FALSE;	
	
	IF NULLIF(TEXTO, '') IS NOT NULL THEN

		OPEN id_responsaveis;

		read_loop: LOOP
		    FETCH id_responsaveis INTO id_responsavel;
		    IF done THEN
		      LEAVE read_loop;
		    END IF;
		    INSERT INTO mensagens_mensagem(pessoa_fisica_id, data_criacao, origem, texto, lido, tag) 
			VALUES(id_responsavel, CURDATE(), 'SISTEMA', CONCAT('Pagamentos de nota: ', TEXTO), FALSE, 'G');
		    
		 END LOOP;
		  
		 CLOSE id_responsaveis;
		
	END IF;	
END $$
DELIMITER ;

CALL parcela_pagamento;

DROP EVENT IF EXISTS parcela_pagamento_event;
CREATE EVENT parcela_pagamento_event
  ON SCHEDULE
    EVERY 1 DAY
    STARTS '2017-03-30 01:00:00' ON COMPLETION PRESERVE ENABLE 
  DO
  	CALL parcela_pagamento;