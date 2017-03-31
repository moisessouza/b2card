DROP PROCEDURE IF EXISTS proposta_pendente;
DELIMITER $$
CREATE PROCEDURE proposta_pendente ()
BEGIN

	DECLARE done INT DEFAULT FALSE;
	DECLARE id INT;
	DECLARE nome_demanda VARCHAR(1000);
	DECLARE data_limite DATE;
	DECLARE id_responsavel INT;
	
	DECLARE TEXTO VARCHAR(1000);
	
	DECLARE id_responsaveis CURSOR FOR 
		SELECT pessoa_fisica_id FROM mensagens_responsavel
		WHERE tag = 'P' AND ativo=TRUE;

	DECLARE propostas CURSOR FOR
		SELECT d.id, d.nome_demanda, p.data_limite_entrega FROM demandas_demanda d
			LEFT JOIN demandas_proposta p ON (d.id = p.demanda_id)
			WHERE p.data_real_entrega IS NULL 
			AND (p.data_limite_entrega IS NULL OR CURDATE() >= DATE_SUB(p.data_limite_entrega, INTERVAL 2 DAY));
		
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
	
	DELETE FROM mensagens_mensagem WHERE tag='P';
	
	OPEN propostas;

	SET TEXTO = '';	
	
	read_loop: LOOP
	    FETCH propostas INTO id, nome_demanda, data_limite;
	    IF done THEN
	      LEAVE read_loop;
	    END IF;
	    SET TEXTO = CONCAT(LPAD(id, 5, '0'), ' - ', nome_demanda, ' (', IF(data_limite IS NOT NULL, DATE_FORMAT(data_limite, '%d/%m/%Y'),'Sem data limite'), '), ', TEXTO);
	  END LOOP;
	  
	CLOSE propostas;
	
	SET done = FALSE;	
	
	IF NULLIF(TEXTO, '') IS NOT NULL THEN

		OPEN id_responsaveis;

		read_loop: LOOP
		    FETCH id_responsaveis INTO id_responsavel;
		    IF done THEN
		      LEAVE read_loop;
		    END IF;
		    INSERT INTO mensagens_mensagem(pessoa_fisica_id, data_criacao, origem, texto, lido, tag) 
			VALUES(id_responsavel, CURDATE(), 'SISTEMA', CONCAT('Propostas pendentes: ', TEXTO), FALSE, 'P');
		    
		 END LOOP;
		  
		 CLOSE id_responsaveis;
		
	END IF;	
END $$
DELIMITER ;

CALL proposta_pendente;

DROP EVENT IF EXISTS proposta_pendente_event;
CREATE EVENT proposta_pendente_event
  ON SCHEDULE
    EVERY 1 DAY
    STARTS '2017-03-30 01:00:00' ON COMPLETION PRESERVE ENABLE 
  DO
  	CALL proposta_pendente;