DROP TABLE IF EXISTS tbl_exame_periodico;

DROP PROCEDURE IF EXISTS exame_periodico;
DELIMITER $$
CREATE PROCEDURE exame_periodico ()
BEGIN

	DECLARE done INT DEFAULT FALSE;
	DECLARE id INT;
	DECLARE id_responsavel INT;
	DECLARE nome VARCHAR(100);
	DECLARE data_ultimo_exame DATE;

	DECLARE TEXTO VARCHAR(1000);
	
	DECLARE id_responsaveis CURSOR FOR 
		SELECT pessoa_fisica_id FROM mensagens_responsavel
		WHERE tag = 'E' AND ativo=TRUE;
	
	DECLARE funcionarios CURSOR FOR 
		SELECT p.nome_razao_social, pf.id, data_ultimo_exame_periodico FROM cadastros_pessoafisica pf
		JOIN cadastros_pessoa p ON (p.id = pf.pessoa_id)
		JOIN cadastros_prestador pr ON (pf.id = pr.pessoa_fisica_id)
		WHERE (pr.data_inicio <= NOW() AND (data_fim >= NOW() OR data_fim IS NULL))
		AND data_ultimo_exame_periodico <= DATE_ADD(DATE_SUB(CURDATE(),INTERVAL 1 YEAR), INTERVAL 1 MONTH);
		
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
	
	DELETE FROM mensagens_mensagem WHERE tag = 'E';
	
	SET TEXTO = "";
	
	OPEN funcionarios;
	
	read_loop: LOOP
	    FETCH funcionarios INTO nome, id, data_ultimo_exame;
	    IF done THEN
	      LEAVE read_loop;
	    END IF;
	    SET TEXTO = CONCAT(nome, ' ',  DATE_FORMAT(data_ultimo_exame, '%d/%m/%Y'), ', ', TEXTO);
	  END LOOP;
	
	SELECT TEXTO;
	
	SET done = FALSE;
	
	CLOSE funcionarios;

	IF NULLIF(TEXTO, '') IS NOT NULL THEN
	
		OPEN id_responsaveis;
		
		read_loop: LOOP
		    FETCH id_responsaveis INTO id_responsavel;
		    IF done THEN
		      LEAVE read_loop;
		    END IF;
		    INSERT INTO mensagens_mensagem(pessoa_fisica_id, data_criacao, origem, texto, lido, tag) 
			VALUES(id_responsavel, CURDATE(), 'SISTEMA', CONCAT('Exames periódicos: ', TEXTO), FALSE, 'E');
		    
		 END LOOP;
		  
		 CLOSE id_responsaveis;
		 
	END IF;

END $$
DELIMITER ;

CALL exame_periodico;

DROP EVENT IF EXISTS exame_periodico_event;
CREATE EVENT exame_periodico_event
  ON SCHEDULE
    EVERY 1 DAY
    STARTS '2017-03-30 01:00:00' ON COMPLETION PRESERVE ENABLE 
  DO
  	CALL exame_periodico;